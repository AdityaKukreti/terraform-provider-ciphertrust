package provider

import (
	"fmt"
	"os"
	"testing"

	"github.com/google/uuid"
	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

// TestCckmOCIConnection exercises the full lifecycle of the ciphertrust_oci_connection resource:
// Create, RefreshState, ImportState, and Update (description change).
func TestCckmOCIConnection(t *testing.T) {
	ociKeyFile := os.Getenv("CCKM_OCI_KEY_FILE")
	ociPubKeyFP := os.Getenv("CCKM_OCI_FINGERPRINT")
	ociRegion := os.Getenv("CCKM_OCI_REGION")
	ociTenancyOCID := os.Getenv("CCKM_OCI_CONN_TENANCY")
	ociUserOCID := os.Getenv("CCKM_OCI_USER")
	ok := ociKeyFile != "" && ociPubKeyFP != "" && ociRegion != "" && ociTenancyOCID != "" && ociUserOCID != ""
	if !ok {
		t.Skip("Skipping OCI connection test: required environment variables not set " +
			"(CCKM_OCI_KEY_FILE, CCKM_OCI_FINGERPRINT, CCKM_OCI_REGION, CCKM_OCI_CONN_TENANCY, CCKM_OCI_USER)")
	}

	connectionTemplate := `
		resource "ciphertrust_oci_connection" "connection" {
			key_file = <<-EOT
			%s
			EOT
			name                = "%s"
			pub_key_fingerprint = "%s"
			region              = "%s"
			tenancy_ocid        = "%s"
			user_ocid           = "%s"
			%s
		}`

	name := "tf-" + uuid.New().String()[:8]
	connectionResource := "ciphertrust_oci_connection.connection"

	// Step 1 config - no description
	createConfig := fmt.Sprintf(connectionTemplate,
		ociKeyFile, name, ociPubKeyFP, ociRegion, ociTenancyOCID, ociUserOCID, "")

	// Step 3 config - add description
	updateConfig := fmt.Sprintf(connectionTemplate,
		ociKeyFile, name, ociPubKeyFP, ociRegion, ociTenancyOCID, ociUserOCID,
		`description = "Updated by Terraform test"`)

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			// Step 1: Create and verify core attributes
			{
				Config: createConfig,
				Check: resource.ComposeTestCheckFunc(
					resource.TestCheckResourceAttrSet(connectionResource, "id"),
					resource.TestCheckResourceAttr(connectionResource, "name", name),
					resource.TestCheckResourceAttr(connectionResource, "region", ociRegion),
					resource.TestCheckResourceAttr(connectionResource, "tenancy_ocid", ociTenancyOCID),
					resource.TestCheckResourceAttr(connectionResource, "user_ocid", ociUserOCID),
					resource.TestCheckResourceAttr(connectionResource, "pub_key_fingerprint", ociPubKeyFP),
					resource.TestCheckResourceAttr(connectionResource, "products.#", "1"),
					resource.TestCheckResourceAttr(connectionResource, "products.0", "cckm"),
					resource.TestCheckResourceAttrSet(connectionResource, "created_at"),
					resource.TestCheckResourceAttr(connectionResource, "last_connection_ok", "true"),
				),
			},
			// Step 2: RefreshState - verify state is consistent with the API
			{
				RefreshState: true,
				Check: resource.ComposeTestCheckFunc(
					resource.TestCheckResourceAttrSet(connectionResource, "id"),
					resource.TestCheckResourceAttr(connectionResource, "name", name),
					resource.TestCheckResourceAttr(connectionResource, "region", ociRegion),
				),
			},
			// Step 3: ImportState - verify the resource can be re-imported by ID
			{
				ResourceName:            connectionResource,
				ImportState:             true,
				ImportStateVerify:       true,
				ImportStateVerifyIgnore: []string{"key_file", "key_file_pass_phrase", "skip_connection_params_test"},
			},
			// Step 4: Update - change description and verify it is reflected in state
			{
				Config: updateConfig,
				Check: resource.ComposeTestCheckFunc(
					resource.TestCheckResourceAttrSet(connectionResource, "id"),
					resource.TestCheckResourceAttr(connectionResource, "name", name),
					resource.TestCheckResourceAttr(connectionResource, "description", "Updated by Terraform test"),
					resource.TestCheckResourceAttr(connectionResource, "region", ociRegion),
					resource.TestCheckResourceAttr(connectionResource, "last_connection_ok", "true"),
				),
			},
		},
	})
}
