package provider

import (
	"context"
	"fmt"
	"github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/common"
	"github.com/tidwall/gjson"
	"net/url"
	"os"
	"testing"

	"github.com/google/uuid"
	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

// cleanupCckmAwsKMS lists all CCKM AWS KMS registrations in CipherTrust Manager and deletes each one.
// This is called via PreCheck on every CCKM AWS test to remove any KMS resources left behind by a
// previous failed test run. Only runs when TF_CCKM_CLEANUP=true is set, so that contributors do not
// accidentally wipe their own CM resources. All errors are logged as warnings - the cleanup is
// best-effort and never fails the test.
func cleanupCckmAwsKMS() {
	if os.Getenv("TF_CCKM_CLEANUP") != "true" {
		return
	}
	address := os.Getenv("CIPHERTRUST_ADDRESS")
	username := os.Getenv("CIPHERTRUST_USERNAME")
	password := os.Getenv("CIPHERTRUST_PASSWORD")
	domain := "root"
	if address == "" || username == "" || password == "" {
		fmt.Println("cleanupCckmAwsKMS: CIPHERTRUST_ADDRESS, CIPHERTRUST_USERNAME and CIPHERTRUST_PASSWORD must be set, skipping cleanup")
		return
	}
	ctx := context.Background()
	client, err := common.NewClient(ctx, uuid.NewString(), &address, &domain, &domain, &username, &password, true, 180)
	if err != nil {
		fmt.Printf("** cleanupCckmAwsKMS: failed to create client: %s\n", err.Error())
		return
	}
	filters := url.Values{}
	filters.Add("limit", "1000")
	response, err := client.ListWithFilters(ctx, uuid.NewString(), common.URL_AWS_KMS, filters)
	if err != nil {
		fmt.Printf("** cleanupCckmAwsKMS: failed to list KMS: %s\n", err.Error())
		return
	}
	resources := gjson.Get(response, "resources").Array()
	if len(resources) == 0 {
		return
	}
	for _, r := range resources {
		kmsID := gjson.Get(r.Raw, "id").String()
		kmsName := gjson.Get(r.Raw, "name").String()
		_, err := client.DeleteByURL(ctx, uuid.NewString(), common.URL_AWS_KMS+"/"+kmsID)
		if err != nil {
			fmt.Printf("** cleanupCckmAwsKMS: failed to delete KMS '%s' (%s): %s\n", kmsName, kmsID, err.Error())
		} else {
			fmt.Printf("cleanupCckmAwsKMS: deleted KMS '%s'\n", kmsName)
		}
	}
}

func TestCckmAWSKms(t *testing.T) {
	if os.Getenv("AWS_ACCESS_KEY_ID") == "" || os.Getenv("AWS_SECRET_ACCESS_KEY") == "" {
		t.Skip("AWS credentials not set")
	}
	uid := "tf-" + uuid.New().String()[:8]
	updatedConnName := uid + "-upd"

	createKmsConfig := fmt.Sprintf(`
		resource "ciphertrust_aws_connection" "aws_connection" {
			name = "%s"
		}
		data "ciphertrust_aws_account_details" "account_details" {
			aws_connection = ciphertrust_aws_connection.aws_connection.id
		}
		resource "ciphertrust_aws_kms" "kms" {
			account_id     = data.ciphertrust_aws_account_details.account_details.account_id
			aws_connection = ciphertrust_aws_connection.aws_connection.name
			name           = "%s"
			regions = [
				data.ciphertrust_aws_account_details.account_details.regions[0],
				data.ciphertrust_aws_account_details.account_details.regions[1],
				data.ciphertrust_aws_account_details.account_details.regions[2]
			]
		}`, uid, uid)

	updateKmsRegionsConfig := fmt.Sprintf(`
		resource "ciphertrust_aws_connection" "aws_connection" {
			name = "%s"
		}
		data "ciphertrust_aws_account_details" "account_details" {
			aws_connection = ciphertrust_aws_connection.aws_connection.id
		}
		resource "ciphertrust_aws_kms" "kms" {
			account_id     = data.ciphertrust_aws_account_details.account_details.account_id
			aws_connection = ciphertrust_aws_connection.aws_connection.name
			name           = "%s"
			regions        = [data.ciphertrust_aws_account_details.account_details.regions[0]]
		}`, uid, uid)

	updateKmsConnectionConfig := fmt.Sprintf(`
		resource "ciphertrust_aws_connection" "new_aws_connection" {
			name = "%s"
		}
		resource "ciphertrust_aws_connection" "aws_connection" {
			name = "%s"
		}
		data "ciphertrust_aws_account_details" "account_details" {
			aws_connection = ciphertrust_aws_connection.aws_connection.id
		}
		resource "ciphertrust_aws_kms" "kms" {
			account_id     = data.ciphertrust_aws_account_details.account_details.account_id
			aws_connection = ciphertrust_aws_connection.new_aws_connection.name
			name           = "%s"
			regions        = [data.ciphertrust_aws_account_details.account_details.regions[0]]
		}`, updatedConnName, uid, uid)

	resourceName := "ciphertrust_aws_kms.kms"
	resource.Test(t, resource.TestCase{
		PreCheck:                 func() { cleanupCckmAwsKMS() },
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: createKmsConfig,
				Check: resource.ComposeTestCheckFunc(
					resource.TestCheckResourceAttrSet(resourceName, "arn"),
					resource.TestCheckResourceAttrSet(resourceName, "aws_connection"),
					resource.TestCheckResourceAttr(resourceName, "name", uid),
					resource.TestCheckResourceAttrSet(resourceName, "regions.#"),
				),
			},
			{
				// Import the KMS immediately after creation and verify all computed fields
				// round-trip correctly. updated_at is ignored because the two consecutive
				// Read calls made by ImportStateVerify may observe different timestamps if
				// any background process touches the KMS between them.
				ResourceName:            resourceName,
				ImportState:             true,
				ImportStateVerify:       true,
				ImportStateVerifyIgnore: []string{"updated_at"},
			},
			{
				Config: updateKmsRegionsConfig,
				Check: resource.ComposeTestCheckFunc(
					resource.TestCheckResourceAttr(resourceName, "regions.#", "1"),
				),
			},
			{
				Config: updateKmsConnectionConfig,
				Check: resource.ComposeTestCheckFunc(
					resource.TestCheckResourceAttr(resourceName, "aws_connection", updatedConnName),
					resource.TestCheckResourceAttr(resourceName, "regions.#", "1"),
				),
			},
		},
	})
}
