package provider

import (
	"fmt"
	"os"
	"testing"

	"github.com/google/uuid"
	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

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

func TestCckmAWSKmsImport(t *testing.T) {
	if os.Getenv("AWS_ACCESS_KEY_ID") == "" || os.Getenv("AWS_SECRET_ACCESS_KEY") == "" {
		t.Skip("AWS credentials not set")
	}
	uid := "tf-" + uuid.New().String()[:8]

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

	resourceName := "ciphertrust_aws_kms.kms"
	resource.Test(t, resource.TestCase{
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
				ResourceName:      resourceName,
				ImportState:       true,
				ImportStateVerify: true,
			},
		},
	})
}
