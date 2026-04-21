package provider

import (
	"testing"

	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

func TestResourceCTEPolicyLDTKeyRule(t *testing.T) {
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{

			// Step 1: Create LDT Policy
			{
				Config: providerConfig + `
resource "ciphertrust_cm_key" "key1" {
  name         = "ldt-key-initial"
  algorithm    = "aes"
  key_size     = 256
  usage_mask   = 76
  undeletable  = false
  unexportable = false
  xts          = false

  meta = {
    permissions = {
      decrypt_with_key = ["CTE Clients"]
      encrypt_with_key = ["CTE Clients"]
      export_key       = ["CTE Clients"]
      read_key         = ["CTE Clients"]
    }
    cte = {
      persistent_on_client = true
      encryption_mode      = "CBC"
      cte_versioned        = true
    }
  }
}

resource "ciphertrust_cte_policy" "ldt_policy" {
  name        = "LDT_policy"
  policy_type = "LDT"
  never_deny  = true

  ldt_key_rules = [{
    current_key = {
      key_id   = "clear_key"
      key_type = ""
    }

    transformation_key = {
      key_id   = ciphertrust_cm_key.key1.id
      key_type = ""
    }
  }]

  security_rules = [{
    effect        = "permit"
    action        = "all_ops"
    partial_match = false
  }]
}
`,
			},

			// Step 2: Add new LDT key rule (ONLY transformation key changes)
			{
				Config: providerConfig + `
resource "ciphertrust_cm_key" "key1" {
  name         = "ldt-key-initial"
  algorithm    = "aes"
  key_size     = 256
  usage_mask   = 76
  undeletable  = false
  unexportable = false
  xts          = false

  meta = {
    permissions = {
      decrypt_with_key = ["CTE Clients"]
      encrypt_with_key = ["CTE Clients"]
      export_key       = ["CTE Clients"]
      read_key         = ["CTE Clients"]
    }
    cte = {
      persistent_on_client = true
      encryption_mode      = "CBC"
      cte_versioned        = true
    }
  }
}

resource "ciphertrust_cm_key" "key2" {
  name         = "ldt-key-new"
  algorithm    = "aes"
  key_size     = 256
  usage_mask   = 76
  undeletable  = false
  unexportable = false
  xts          = false

  meta = {
    permissions = {
      decrypt_with_key = ["CTE Clients"]
      encrypt_with_key = ["CTE Clients"]
      export_key       = ["CTE Clients"]
      read_key         = ["CTE Clients"]
    }
    cte = {
      persistent_on_client = true
      encryption_mode      = "CBC"
      cte_versioned        = true
    }
  }
}

resource "ciphertrust_cte_resource_set" "rs2" {
  name = "rs2"
}

resource "ciphertrust_cte_policy" "ldt_policy" {
  name        = "LDT_policy"
  policy_type = "LDT"
  never_deny  = true

  ldt_key_rules = [{
    current_key = {
      key_id   = "clear_key"
      key_type = ""
    }

    transformation_key = {
      key_id   = ciphertrust_cm_key.key1.id
      key_type = ""
    }
  }]

  security_rules = [{
    effect        = "permit"
    action        = "all_ops"
    partial_match = false
  }]
}

resource "ciphertrust_cte_policy_ldtkey_rule" "ldt_rule" {
  policy_id = ciphertrust_cte_policy.ldt_policy.id


  rule = [{
    is_exclusion_rule = false

    resource_set_id = ciphertrust_cte_resource_set.rs2.id

    current_key = {
      key_id   = "clear_key"
      key_type = ""
    }

    transformation_key = {
      key_id   = ciphertrust_cm_key.key2.id
      key_type = ""
    }
  }]
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_policy_ldtkey_rule.ldt_rule", "rule_id"),
				),
			},
			// Delete testing automatically occurs in TestCase
		},
	})
}
