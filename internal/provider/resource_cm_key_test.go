package provider

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"regexp"
	"testing"

	"github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/common"
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

func TestAccCMKey_undeletableDrift(t *testing.T) {
	RequireCM(t)
	client, ok := createCMClient()
	if !ok {
		t.Skip("createCMClient failed")
	}

	suffix := uuid.New().String()[:8]
	keyName := "tf-acc-key-undel-" + suffix

	var capturedID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "k" {
  name        = %q
  algorithm   = "aes"
  key_size    = 256
  unexportable = false
}
`, keyName),
				Check: checkStep(t, "undeletable drift: create",
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.k", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.k", "unexportable", "false"),
					func(s *terraform.State) error {
						capturedID = s.RootModule().Resources["ciphertrust_cm_key.k"].Primary.ID
						return nil
					},
				),
			},
			{
				PreConfig: func() {
					patchPayload, _ := json.Marshal(map[string]interface{}{"unexportable": true})
					_, _ = client.UpdateData(context.Background(), capturedID, common.URL_KEY_MANAGEMENT, patchPayload, "id")
				},
				RefreshState:       true,
				ExpectNonEmptyPlan: true,
			},
		},
	})
}

func TestAccCMKey_xtsDrift(t *testing.T) {
	RequireCM(t)
	client, ok := createCMClient()
	if !ok {
		t.Skip("createCMClient failed")
	}

	suffix := uuid.New().String()[:8]
	keyName := "tf-acc-key-xts-" + suffix

	var capturedID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "k" {
  name      = %q
  algorithm = "aes"
  key_size  = 256
  xts       = false
}
`, keyName),
				Check: checkStep(t, "xts drift: create",
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.k", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.k", "xts", "false"),
					func(s *terraform.State) error {
						capturedID = s.RootModule().Resources["ciphertrust_cm_key.k"].Primary.ID
						return nil
					},
				),
			},
			{
				PreConfig: func() {
					patchPayload, _ := json.Marshal(map[string]interface{}{"xts": true})
					_, _ = client.UpdateData(context.Background(), capturedID, common.URL_KEY_MANAGEMENT, patchPayload, "id")
				},
				RefreshState:       true,
				ExpectNonEmptyPlan: true,
			},
		},
	})
}

func TestAccCMKey_aliasHydration(t *testing.T) {
	RequireCM(t)

	suffix := uuid.New().String()[:8]
	keyName := "tf-acc-key-alias-" + suffix

	var capturedID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "k" {
  name      = %q
  algorithm = "aes"
  key_size  = 256
  aliases   = [
    {
      alias = "test-alias"
      type  = "string"
    }
  ]
}
`, keyName),
				Check: checkStep(t, "alias hydration: create",
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.k", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.k", "aliases.0.alias", "test-alias"),
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.k", "aliases.0.index"),
					func(s *terraform.State) error {
						capturedID = s.RootModule().Resources["ciphertrust_cm_key.k"].Primary.ID
						return nil
					},
				),
			},
			{
				RefreshState:       true,
				ExpectNonEmptyPlan: false,
				Check: checkStep(t, "alias hydration: no drift after refresh",
					resource.TestCheckResourceAttr("ciphertrust_cm_key.k", "aliases.0.alias", "test-alias"),
				),
			},
		},
	})
	_ = capturedID
}

func TestAccCMKey_metaHydration(t *testing.T) {
	RequireCM(t)

	ownerID := os.Getenv("TEST_CM_KEY_OWNER_ID")
	if ownerID == "" {
		t.Skip("TEST_CM_KEY_OWNER_ID not set")
	}

	suffix := uuid.New().String()[:8]
	keyName := "tf-acc-key-meta-" + suffix

	var capturedID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "k" {
  name      = %q
  algorithm = "aes"
  key_size  = 256
  meta = {
    owner_id = %q
  }
}
`, keyName, ownerID),
				Check: checkStep(t, "meta hydration: create",
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.k", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.k", "meta.owner_id", ownerID),
					func(s *terraform.State) error {
						capturedID = s.RootModule().Resources["ciphertrust_cm_key.k"].Primary.ID
						return nil
					},
				),
			},
			{
				RefreshState:       true,
				ExpectNonEmptyPlan: false,
				Check: checkStep(t, "meta hydration: no drift after refresh",
					resource.TestCheckResourceAttr("ciphertrust_cm_key.k", "meta.owner_id", ownerID),
				),
			},
		},
	})
	_ = capturedID
}

func TestAccCMKey_metaDrift(t *testing.T) {
	RequireCM(t)
	client, ok := createCMClient()
	if !ok {
		t.Skip("createCMClient failed")
	}

	ownerIDA := os.Getenv("TEST_CM_KEY_OWNER_ID_A")
	ownerIDB := os.Getenv("TEST_CM_KEY_OWNER_ID_B")
	if ownerIDA == "" || ownerIDB == "" {
		t.Skip("TEST_CM_KEY_OWNER_ID_A or TEST_CM_KEY_OWNER_ID_B not set")
	}

	suffix := uuid.New().String()[:8]
	keyName := "tf-acc-key-metadrift-" + suffix

	var capturedID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "k" {
  name      = %q
  algorithm = "aes"
  key_size  = 256
  meta = {
    owner_id = %q
  }
}
`, keyName, ownerIDA),
				Check: checkStep(t, "meta drift: create",
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.k", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.k", "meta.owner_id", ownerIDA),
					func(s *terraform.State) error {
						capturedID = s.RootModule().Resources["ciphertrust_cm_key.k"].Primary.ID
						return nil
					},
				),
			},
			{
				PreConfig: func() {
					patchPayload, _ := json.Marshal(map[string]interface{}{
						"meta": map[string]interface{}{
							"owner_id": ownerIDB,
						},
					})
					_, _ = client.UpdateData(context.Background(), capturedID, common.URL_KEY_MANAGEMENT, patchPayload, "id")
				},
				RefreshState:       true,
				ExpectNonEmptyPlan: true,
			},
		},
	})
}

func TestAccCMKey_labelsDrift(t *testing.T) {
	RequireCM(t)
	client, ok := createCMClient()
	if !ok {
		t.Skip("createCMClient failed")
	}

	suffix := uuid.New().String()[:8]
	keyName := "tf-acc-key-labels-" + suffix

	var capturedID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "k" {
  name      = %q
  algorithm = "aes"
  key_size  = 256
  labels    = { "env" = "test" }
}
`, keyName),
				Check: checkStep(t, "labels drift: create",
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.k", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.k", "labels.env", "test"),
					func(s *terraform.State) error {
						capturedID = s.RootModule().Resources["ciphertrust_cm_key.k"].Primary.ID
						return nil
					},
				),
			},
			{
				PreConfig: func() {
					patchPayload, _ := json.Marshal(map[string]interface{}{
						"labels": map[string]interface{}{"env": "prod"},
					})
					_, _ = client.UpdateData(context.Background(), capturedID, common.URL_KEY_MANAGEMENT, patchPayload, "id")
				},
				RefreshState:       true,
				ExpectNonEmptyPlan: true,
			},
		},
	})
}

func TestAccCMKey_aliasDrift(t *testing.T) {
	RequireCM(t)
	client, ok := createCMClient()
	if !ok {
		t.Skip("createCMClient failed")
	}

	suffix := uuid.New().String()[:8]
	keyName := "tf-acc-key-aldrift-" + suffix

	var capturedID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "k" {
  name      = %q
  algorithm = "aes"
  key_size  = 256
  aliases   = [
    {
      alias = "alias-a"
      type  = "string"
    }
  ]
}
`, keyName),
				Check: checkStep(t, "alias drift: create",
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.k", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.k", "aliases.0.alias", "alias-a"),
					func(s *terraform.State) error {
						capturedID = s.RootModule().Resources["ciphertrust_cm_key.k"].Primary.ID
						return nil
					},
				),
			},
			{
				PreConfig: func() {
					patchPayload, _ := json.Marshal(map[string]interface{}{
						"aliases": []map[string]interface{}{
							{"alias": "alias-a", "type": "string"},
							{"alias": "alias-b", "type": "string"},
						},
					})
					_, _ = client.UpdateData(context.Background(), capturedID, common.URL_KEY_MANAGEMENT, patchPayload, "id")
				},
				RefreshState:       true,
				ExpectNonEmptyPlan: true,
			},
		},
	})
}

func TestAccCMKey_readNotFound(t *testing.T) {
	RequireCM(t)
	client, ok := createCMClient()
	if !ok {
		t.Skip("createCMClient failed")
	}

	suffix := uuid.New().String()[:8]
	keyName := "tf-acc-key-notfound-" + suffix

	var capturedID string

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "k" {
  name      = %q
  algorithm = "aes"
  key_size  = 256
}
`, keyName),
				Check: checkStep(t, "read not found: create",
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.k", "id"),
					func(s *terraform.State) error {
						capturedID = s.RootModule().Resources["ciphertrust_cm_key.k"].Primary.ID
						return nil
					},
				),
			},
			{
				PreConfig: func() {
					_, _ = client.DeleteByURL(context.Background(), uuid.New().String(), common.URL_KEY_MANAGEMENT+"/"+capturedID)
				},
				RefreshState:       true,
				ExpectNonEmptyPlan: true,
			},
		},
	})
}

func TestResourceCMKey(t *testing.T) {
	suffix := uuid.New().String()[:8]
	keyName := "terraform-" + suffix

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "cte_key" {
  name        = %q
  algorithm   = "aes"
  key_size    = 256
  usage_mask  = 76
  undeletable = false
  unexportable = false
}
`, keyName),
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.cte_key", "id"),
				),
			},
			// Update and Read testing — same name (immutable), only patch usage_mask + description
			{
				Config: providerConfig + fmt.Sprintf(`
resource "ciphertrust_cm_key" "cte_key" {
  name        = %q
  algorithm   = "aes"
  key_size    = 256
  usage_mask  = 13
  undeletable = false
  unexportable = false
  description = "updated via terraform"
}
`, keyName),
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cm_key.cte_key", "id"),
					resource.TestCheckResourceAttr("ciphertrust_cm_key.cte_key", "description", "updated via terraform"),
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
