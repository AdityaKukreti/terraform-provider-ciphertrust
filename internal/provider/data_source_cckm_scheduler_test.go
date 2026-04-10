package provider

import (
	"fmt"
	"strings"
	"testing"

	"github.com/google/uuid"
	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

func TestCckmSchedulersRotationDataSource(t *testing.T) {
	t.Run("aws", func(t *testing.T) {
		createSchedulerParams := `
			resource "ciphertrust_scheduler" "aws_scheduled_rotation_job" {
				cckm_key_rotation_params {
					cloud_name = "aws"
					expiration = "%s"
					expire_in = "%s"
					rotation_after = "6d"
					rotate_material = true
					aws_retain_alias = true
				}
				name       = "%s"
				operation  = "cckm_key_rotation"
				run_at     = "0 9 * * fri"
			}
			data "ciphertrust_scheduler_list" "aws_scheduled_rotation_job" {
				filters = {
					id = ciphertrust_scheduler.aws_scheduled_rotation_job.id
				}

			}`
		resourceName := "ciphertrust_scheduler.aws_scheduled_rotation_job"
		datasourceName := "data.ciphertrust_scheduler_list.aws_scheduled_rotation_job"
		schedulerName := "aws-key-rotation-" + uuid.New().String()[:8]
		expiration := "44d"
		expireIn := "22h"
		rotateMaterialExpectedValue := "true"
		createConfig := fmt.Sprintf(createSchedulerParams, expiration, expireIn, schedulerName)
		if getCipherTrustVersion() < 221 {
			rotateMaterialExpectedValue = "false"
			createConfig = strings.ReplaceAll(createConfig, "rotate_material = true", "")
		}
		resource.Test(t, resource.TestCase{
			ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
			Steps: []resource.TestStep{
				{
					Config: createConfig,
					Check: resource.ComposeTestCheckFunc(
						resource.TestCheckResourceAttrSet(resourceName, "id"),
						resource.TestCheckResourceAttr(resourceName, "cckm_key_rotation_params.0.cloud_name", "aws"),
						resource.TestCheckResourceAttr(resourceName, "cckm_key_rotation_params.0.expiration", expiration),
						resource.TestCheckResourceAttr(resourceName, "cckm_key_rotation_params.0.rotation_after", "6d"),
						resource.TestCheckResourceAttr(resourceName, "cckm_key_rotation_params.0.rotate_material", rotateMaterialExpectedValue),
						resource.TestCheckResourceAttr(resourceName, "cckm_key_rotation_params.0.aws_retain_alias", "true"),
						resource.TestCheckResourceAttr(resourceName, "cckm_key_rotation_params.0.expire_in", expireIn),

						resource.TestCheckResourceAttr(datasourceName, "scheduler.#", "1"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.operation", "cckm_key_rotation"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_key_rotation_params.cloud_name", "aws"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_key_rotation_params.expiration", expiration),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_key_rotation_params.rotation_after", "6d"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_key_rotation_params.expire_in", expireIn),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_key_rotation_params.aws_params.rotate_material", rotateMaterialExpectedValue),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_key_rotation_params.aws_params.retain_alias", "true"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.run_at", "0 9 * * fri"),
					),
				},
			},
		})
	})

	t.Run("XKSCredentialRotation", func(t *testing.T) {
		schedulerConfig := `
			resource "ciphertrust_scheduler" "xks_credential_rotation" {
				cckm_xks_credential_rotation_params = {
					cloud_name = "aws"
				}
				name       = "%s"
				operation  = "cckm_xks_credential_rotation"
				run_at     = "0 9 * * fri"
			}
			data "ciphertrust_scheduler_list" "xks_credential_rotation" {
				filters = {
					id = ciphertrust_scheduler.xks_credential_rotation.id
				}
			}`
		schedulerName := "tf-xks-cred-rotation" + uuid.New().String()[:8]
		schedulerConfigStr := fmt.Sprintf(schedulerConfig, schedulerName)
		resourceName := "ciphertrust_scheduler.xks_credential_rotation"
		datasourceName := "data.ciphertrust_scheduler_list.xks_credential_rotation"
		resource.Test(t, resource.TestCase{
			ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
			Steps: []resource.TestStep{
				{
					Config: schedulerConfigStr,
					Check: resource.ComposeTestCheckFunc(
						resource.TestCheckResourceAttrSet(resourceName, "id"),
						resource.TestCheckResourceAttr(resourceName, "cckm_xks_credential_rotation_params.cloud_name", "aws"),

						resource.TestCheckResourceAttr(datasourceName, "scheduler.#", "1"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_xks_credential_rotation_params.cloud_name", "aws"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.operation", "cckm_xks_credential_rotation"),
					),
				},
			},
		})
	})

	t.Run("oci", func(t *testing.T) {
		createConfig := `
			resource "ciphertrust_scheduler" "oci_rotation_scheduler" {
				cckm_key_rotation_params {
					cloud_name = "oci"
					expiration = "%s"
					expire_in  = "%s"
				}
				name       = "%s"
				operation  = "cckm_key_rotation"
				run_at     = "0 9 * * fri"
			}
			data "ciphertrust_scheduler_list" "oci_rotation_scheduler" {
				filters = {
					id = ciphertrust_scheduler.oci_rotation_scheduler.id
				}
			}`
		expiration := "44d"
		expireIn := "22h"
		name := "tf" + uuid.New().String()[:8]
		resourceName := "ciphertrust_scheduler.oci_rotation_scheduler"
		datasourceName := "data.ciphertrust_scheduler_list.oci_rotation_scheduler"
		createConfigStr := fmt.Sprintf(createConfig, expiration, expireIn, name)
		resource.Test(t, resource.TestCase{
			ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
			Steps: []resource.TestStep{
				{
					Config: createConfigStr,
					Check: resource.ComposeTestCheckFunc(
						resource.TestCheckResourceAttr(resourceName, "cckm_key_rotation_params.0.cloud_name", "oci"),
						resource.TestCheckResourceAttr(resourceName, "cckm_key_rotation_params.0.expiration", expiration),
						resource.TestCheckResourceAttr(resourceName, "cckm_key_rotation_params.0.expire_in", expireIn),

						resource.TestCheckResourceAttr(datasourceName, "scheduler.#", "1"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.operation", "cckm_key_rotation"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_key_rotation_params.cloud_name", "oci"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_key_rotation_params.expiration", expiration),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_key_rotation_params.expire_in", expireIn),
					),
				},
			},
		})
	})
}

func TestCckmSchedulersSyncDataSource(t *testing.T) {
	t.Run("aws", func(t *testing.T) {
		connectionResource, ok := initCckmAwsTest()
		if !ok {
			t.Skip()
		}
		createParams := `
			resource "ciphertrust_scheduler" "aws_sync_job" {
				cckm_synchronization_params {
					cloud_name  = "aws"
					kms         = [ciphertrust_aws_kms.kms.id]
				}
				name       = "%s"
				operation  = "cckm_synchronization"
				run_at     = "0 9 * * fri"
			}
			data "ciphertrust_scheduler_list" "aws_sync_job" {
				filters = {
					id = ciphertrust_scheduler.aws_sync_job.id
				}
			}`
		resourceName := "ciphertrust_scheduler.aws_sync_job"
		datasourceName := "data.ciphertrust_scheduler_list.aws_sync_job"
		syncJobName := "tf" + uuid.New().String()[:8]
		createConfig := connectionResource + fmt.Sprintf(createParams, syncJobName)
		resource.Test(t, resource.TestCase{
			ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
			Steps: []resource.TestStep{
				{
					Config: createConfig,
					Check: resource.ComposeTestCheckFunc(
						resource.TestCheckResourceAttrSet(resourceName, "id"),
						resource.TestCheckResourceAttr(resourceName, "cckm_synchronization_params.0.kms.#", "1"),
						resource.TestCheckResourceAttr(resourceName, "cckm_synchronization_params.0.cloud_name", "aws"),
						resource.TestCheckResourceAttr(resourceName, "cckm_synchronization_params.0.synchronize_all", "false"),

						resource.TestCheckResourceAttr(datasourceName, "scheduler.#", "1"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.operation", "cckm_synchronization"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_synchronization_params.cloud_name", "aws"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_synchronization_params.synchronize_all", "false"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_synchronization_params.kms.#", "1"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.run_at", "0 9 * * fri"),
					),
				},
			},
		})
	})
	t.Run("oci", func(t *testing.T) {
		connectionResource := initCckmOCITest(t)
		createConfig := `
			resource "ciphertrust_scheduler" "oci_sync_job" {
				cckm_synchronization_params {
					cloud_name  = "oci"
					oci_vaults  = [ciphertrust_oci_vault.vault.id]
				}
				name       = "%s"
				operation  = "cckm_synchronization"
				run_at     = "0 9 * * fri"
			}
			data "ciphertrust_scheduler_list" "oci_sync_job" {
				filters = {
					id = ciphertrust_scheduler.oci_sync_job.id
				}
			}`
		resourceName := "ciphertrust_scheduler.oci_sync_job"
		datasourceName := "data.ciphertrust_scheduler_list.oci_sync_job"
		syncJobName := "tf" + uuid.New().String()[:8]
		createConfigStr := connectionResource + fmt.Sprintf(createConfig, syncJobName)
		resource.Test(t, resource.TestCase{
			ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
			Steps: []resource.TestStep{
				{
					Config: createConfigStr,
					Check: resource.ComposeTestCheckFunc(
						resource.TestCheckResourceAttrSet(resourceName, "id"),
						resource.TestCheckResourceAttr(resourceName, "cckm_synchronization_params.0.oci_vaults.#", "1"),
						resource.TestCheckResourceAttr(resourceName, "cckm_synchronization_params.0.cloud_name", "oci"),
						resource.TestCheckResourceAttr(resourceName, "cckm_synchronization_params.0.synchronize_all", "false"),

						resource.TestCheckResourceAttr(datasourceName, "scheduler.#", "1"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.operation", "cckm_synchronization"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_synchronization_params.cloud_name", "oci"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_synchronization_params.synchronize_all", "false"),
						resource.TestCheckResourceAttr(datasourceName, "scheduler.0.cckm_synchronization_params.oci_vaults.#", "1"),
					),
				},
			},
		})
	})
}
