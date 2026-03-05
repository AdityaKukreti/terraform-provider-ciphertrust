package provider

import (
	"fmt"
	"os"
	"testing"

	"github.com/google/uuid"
	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

func TestCiphertrustOCIConnectionDataSource(t *testing.T) {
	ociKeyFile := os.Getenv("CCKM_OCI_KEY_FILE")
	ociPubKeyFP := os.Getenv("CCKM_OCI_FINGERPRINT")
	ociRegion := os.Getenv("CCKM_OCI_REGION")
	ociTenancyOCID := os.Getenv("CCKM_OCI_CONN_TENANCY")
	ociUserOCID := os.Getenv("CCKM_OCI_USER")
	ok := ociKeyFile != "" && ociPubKeyFP != "" && ociRegion != "" && ociTenancyOCID != "" && ociUserOCID != ""
	if !ok {
		t.Skip("Failed to set OCI connection variables")
	}

	connectionConfig := `
		resource "ciphertrust_oci_connection" "connection" {
			key_file = <<-EOT
			%s
			EOT
			name                = "%s"
			pub_key_fingerprint = "%s"
			region              = "%s"
			tenancy_ocid        = "%s"
			user_ocid           = "%s"
		}
		data "ciphertrust_oci_connection_list" "by_name" {
			filters = {
				name = ciphertrust_oci_connection.connection.name
			}
		}
		data "ciphertrust_oci_connection_list" "no_filters" {
			depends_on = [ciphertrust_oci_connection.connection]
		}`

	name := "tf-" + uuid.New().String()[:8]
	connectionConfigStr := fmt.Sprintf(connectionConfig, ociKeyFile, name, ociPubKeyFP, ociRegion, ociTenancyOCID, ociUserOCID)
	byNameDataSource := "data.ciphertrust_oci_connection_list.by_name"
	noFiltersDataSource := "data.ciphertrust_oci_connection_list.no_filters"
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: connectionConfigStr,
				Check: resource.ComposeTestCheckFunc(
					resource.TestCheckResourceAttr(byNameDataSource, "oci.#", "1"),
					resource.TestCheckResourceAttr(byNameDataSource, "oci.0.name", name),
					resource.TestCheckResourceAttr(noFiltersDataSource, "oci.#", "1"),
				),
			},
		},
	})
}
