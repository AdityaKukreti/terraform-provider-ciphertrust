package provider

import (
	"testing"

	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

func TestResourceCTEPolicyIDTKeyRule(t *testing.T) {
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{

			// Step 1: Create IDT Policy
			{
				Config: providerConfig + `
resource "ciphertrust_cm_key" "key1" {
  name         = "idt-key-initial"
  algorithm    = "aes"
  key_size     = 256
  usage_mask   = 76
  undeletable  = false
  unexportable = false
  xts          = true
  meta = {
    permissions = {
      decrypt_with_key = ["CTE Clients"]
      encrypt_with_key = ["CTE Clients"]
      export_key       = ["CTE Clients"]
      read_key         = ["CTE Clients"]
    }
    cte = {
      persistent_on_client = true
      encryption_mode      = "XTS"
      cte_versioned        = false
    }
  }
}

resource "ciphertrust_cte_policy" "idt_policy" {
  name        = "IDT_policy"
  policy_type = "IDT"

  idt_key_rules = [{
    current_key             = "clear_key"
    current_key_type        = ""
    transformation_key      = ciphertrust_cm_key.key1.id
    transformation_key_type = ""
  }]

  security_rules = [{
    effect = "permit"
    action = "all_ops"
  }]

 depends_on = [ciphertrust_cm_key.key1]
}
`,
			},

			// Step 2: Update IDT key rule
			{
				Config: providerConfig + `
resource "ciphertrust_cm_key" "key1" {
  name         = "idt-key-initial"
  algorithm    = "aes"
  key_size     = 256
  usage_mask   = 76
  undeletable  = false
  unexportable = false
  xts          = true

  meta = {
    permissions = {
      decrypt_with_key = ["CTE Clients"]
      encrypt_with_key = ["CTE Clients"]
      export_key       = ["CTE Clients"]
      read_key         = ["CTE Clients"]
    }
    cte = {
      persistent_on_client = true
      encryption_mode      = "XTS"
      cte_versioned        = false
    }
  }
}

resource "ciphertrust_cm_key" "key2" {
  name         = "idt-key-new"
  algorithm    = "aes"
  key_size     = 256
  usage_mask   = 76
  undeletable  = false
  unexportable = false
  xts          = true
 

  meta = {
    permissions = {
      decrypt_with_key = ["CTE Clients"]
      encrypt_with_key = ["CTE Clients"]
      export_key       = ["CTE Clients"]
      read_key         = ["CTE Clients"]
    }
    cte = {
      persistent_on_client = true
      encryption_mode      = "XTS"
      cte_versioned        = false
    }
  }
}

resource "ciphertrust_cte_policy" "idt_policy" {
  name        = "IDT_policy"
  policy_type = "IDT"

  idt_key_rules = [{
    current_key             = "clear_key"
    current_key_type        = ""
    transformation_key      = ciphertrust_cm_key.key1.id
    transformation_key_type = ""
  }]

  security_rules = [{
    effect = "permit"
    action = "all_ops"
  }]

  depends_on = [ciphertrust_cm_key.key1, ciphertrust_cm_key.key2]
}

resource "ciphertrust_cte_policy_idt_key_rule" "idt_rule" {
  policy_id = ciphertrust_cte_policy.idt_policy.id

  rule = {
    id = ciphertrust_cte_policy.idt_policy.idt_key_rules[0].id

    current_key        = "clear_key"
    current_key_type   = ""

    transformation_key      = ciphertrust_cm_key.key2.id
    transformation_key_type = ""
  }
  depends_on = [ciphertrust_cm_key.key2]
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_policy_idt_key_rule.idt_rule", "rule.id"),
				),
			},
			// Delete testing automatically occurs in TestCase
		},
	})
}
