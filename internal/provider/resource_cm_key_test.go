package provider

import (
	"context"
	"fmt"
	"regexp"
	"testing"

	common "github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/common"
	"github.com/google/uuid"
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/acctest"
	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
	"github.com/hashicorp/terraform-plugin-testing/terraform"
)

// aesKeyConfig returns a minimal ciphertrust_cm_key config for an AES key.
func aesKeyConfig(name string, keySize int) string {
	return providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name      = %q
  algorithm = "aes"
  key_size  = %d
}
`, name, keySize)
}

// TestResourceCMKey is the original integration smoke-test (create + update mutable fields).
func TestResourceCMKey(t *testing.T) {
	keyName := "terraform-" + uuid.New().String()[:8]

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
data "ciphertrust_cm_users_list" "users_list" {
  filters = {
    username = "admin"
  }
}

resource "ciphertrust_cm_key" "cte_key" {
  name=%q
  algorithm="aes"
  key_size=256
  usage_mask=76
  undeletable=false
  unexportable=false
  meta={
    owner_id=tolist(data.ciphertrust_cm_users_list.users_list.users)[0].user_id
    permissions={
      decrypt_with_key=["CTE Clients"]
      encrypt_with_key=["CTE Clients"]
      export_key=["CTE Clients"]
      mac_verify_with_key=["CTE Clients"]
      mac_with_key=["CTE Clients"]
      read_key=["CTE Clients"]
      sign_verify_with_key=["CTE Clients"]
      sign_with_key=["CTE Clients"]
      use_key=["CTE Clients"]
    }
    cte={
      persistent_on_client=true
      encryption_mode="CBC"
      cte_versioned=false
    }
    xts=false
  }
}
`, keyName),
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.cte_key", "id"),
				),
			},
			// Update and Read testing (name is immutable — keep it unchanged)
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "cte_key" {
  name=%q
  algorithm="aes"
  key_size=256
  usage_mask=13
  description="updated via terraform"
}
`, keyName),
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.cte_key", "id"),
				),
			},
			// Delete testing automatically occurs in TestCase
		},
	})
}

// TestCMKeyBasicCRUD creates an AES key, verifies it, then updates a mutable
// field (description) and verifies the update was applied.
func TestCMKeyBasicCRUD(t *testing.T) {
	rName := "tf-key-" + acctest.RandStringFromCharSet(8, acctest.CharSetAlphaNum)
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: aesKeyConfig(rName, 256),
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.test_key", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.test_key", "name", rName),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.test_key", "algorithm", "aes"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.test_key", "key_size", "256"),
				),
			},
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name        = %q
  algorithm   = "aes"
  key_size    = 256
  description = "updated"
}
`, rName),
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttr("ciphertrust_cm_key.test_key", "description", "updated"),
				),
			},
		},
	})
}

// TestCMKeyNameImmutable verifies that attempting to rename a key after creation
// produces a clear, actionable plan-time error rather than silent state drift
// (where Terraform state updates but CM retains the original name).
func TestCMKeyNameImmutable(t *testing.T) {
	rName := "tf-key-" + acctest.RandStringFromCharSet(8, acctest.CharSetAlphaNum)
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: aesKeyConfig(rName, 256),
				Check:  resource.TestCheckResourceAttrSet("ciphertrust_cm_key.test_key", "id"),
			},
			{
				Config:      aesKeyConfig(rName+"-renamed", 256),
				PlanOnly:    true,
				ExpectError: regexp.MustCompile(`cannot be changed`),
			},
		},
	})
}

// TestCMKeyAlgorithmImmutable verifies that attempting to change the 'algorithm'
// field after creation produces a clear, actionable plan-time error.
func TestCMKeyAlgorithmImmutable(t *testing.T) {
	rName := "tf-key-" + acctest.RandStringFromCharSet(8, acctest.CharSetAlphaNum)
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			// Step 1: create.
			{
				Config: aesKeyConfig(rName, 256),
				Check:  resource.TestCheckResourceAttrSet("ciphertrust_cm_key.test_key", "id"),
			},
			// Step 2: attempt to change algorithm — must fail at plan time.
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name      = %q
  algorithm = "rsa"
  key_size  = 2048
}
`, rName),
				PlanOnly:    true,
				ExpectError: regexp.MustCompile(`cannot be changed`),
			},
		},
	})
}

// TestCMKeyKeySizeImmutable verifies that changing 'key_size' after creation
// produces a clear plan-time error.
func TestCMKeyKeySizeImmutable(t *testing.T) {
	rName := "tf-key-" + acctest.RandStringFromCharSet(8, acctest.CharSetAlphaNum)
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: aesKeyConfig(rName, 256),
				Check:  resource.TestCheckResourceAttrSet("ciphertrust_cm_key.test_key", "id"),
			},
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name      = %q
  algorithm = "aes"
  key_size  = 128
}
`, rName),
				PlanOnly:    true,
				ExpectError: regexp.MustCompile(`cannot be changed`),
			},
		},
	})
}

// TestCMKeyObjectTypeImmutable verifies that changing 'object_type' after
// creation produces a clear plan-time error.
func TestCMKeyObjectTypeImmutable(t *testing.T) {
	rName := "tf-key-" + acctest.RandStringFromCharSet(8, acctest.CharSetAlphaNum)
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name        = %q
  algorithm   = "aes"
  key_size    = 256
  object_type = "Symmetric Key"
}
`, rName),
				Check: resource.TestCheckResourceAttrSet("ciphertrust_cm_key.test_key", "id"),
			},
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name        = %q
  algorithm   = "aes"
  key_size    = 256
  object_type = "Secret Data"
}
`, rName),
				PlanOnly:    true,
				ExpectError: regexp.MustCompile(`cannot be changed`),
			},
		},
	})
}

// TestCMKeyCurveidImmutable verifies that changing 'curveid' after creation
// produces a clear plan-time error.
func TestCMKeyCurveidImmutable(t *testing.T) {
	rName := "tf-key-" + acctest.RandStringFromCharSet(8, acctest.CharSetAlphaNum)
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name      = %q
  algorithm = "ec"
  curveid   = "prime256v1"
}
`, rName),
				Check: resource.TestCheckResourceAttrSet("ciphertrust_cm_key.test_key", "id"),
			},
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name      = %q
  algorithm = "ec"
  curveid   = "secp384r1"
}
`, rName),
				PlanOnly:    true,
				ExpectError: regexp.MustCompile(`cannot be changed`),
			},
		},
	})
}

// TestCMKeyOutOfBandDeletion verifies that when a key is deleted directly on
// CipherTrust Manager (out-of-band), the next terraform plan/refresh removes it
// from state gracefully instead of returning a hard error.
func TestCMKeyOutOfBandDeletion(t *testing.T) {
	rName := "tf-key-" + acctest.RandStringFromCharSet(8, acctest.CharSetAlphaNum)

	// deleteOutOfBand returns a Check function that deletes the resource from
	// CM directly after Terraform has created it, simulating an out-of-band delete.
	deleteOutOfBand := func(resourceName string) resource.TestCheckFunc {
		return func(s *terraform.State) error {
			rs, ok := s.RootModule().Resources[resourceName]
			if !ok {
				return fmt.Errorf("resource %s not found in state", resourceName)
			}
			id := rs.Primary.ID
			client, ok := createCMClient()
			if !ok {
				t.Skip("Skipping out-of-band deletion test: CM client could not be created (check CIPHERTRUST_* env vars)")
			}
			endpoint := common.URL_KEY_MANAGEMENT + "/" + id
			if _, err := client.DeleteByURL(context.Background(), id, endpoint); err != nil {
				return fmt.Errorf("out-of-band delete failed: %s", err)
			}
			return nil
		}
	}

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			// Step 1: Create the key normally, then delete it from CM directly.
			{
				Config: aesKeyConfig(rName, 256),
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.test_key", "id"),
					deleteOutOfBand("ciphertrust_cm_key.test_key"),
				),
			},
			// Step 2: Refresh state — Read() must detect 404 and remove from
			// state cleanly (no error). RefreshState: true runs terraform refresh.
			{
				RefreshState: true,
			},
			// Step 3: Re-apply — Terraform recreates the key from scratch, proving
			// the resource can be recovered after an out-of-band deletion.
			{
				Config: aesKeyConfig(rName, 256),
				Check:  resource.TestCheckResourceAttrSet("ciphertrust_cm_key.test_key", "id"),
			},
		},
	})
}

// TestCMKeyMaterialImmutable verifies that changing 'material' (key material)
// after creation produces a clear plan-time error.
func TestCMKeyMaterialImmutable(t *testing.T) {
	rName := "tf-key-" + acctest.RandStringFromCharSet(8, acctest.CharSetAlphaNum)
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name      = %q
  algorithm = "aes"
  key_size  = 256
  material  = "000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f"
}
`, rName),
				Check: resource.TestCheckResourceAttrSet("ciphertrust_cm_key.test_key", "id"),
			},
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "test_key" {
  name      = %q
  algorithm = "aes"
  key_size  = 256
  material  = "202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f"
}
`, rName),
				PlanOnly:    true,
				ExpectError: regexp.MustCompile(`cannot be changed`),
			},
		},
	})
}
