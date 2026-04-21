package provider

import (
	"testing"

	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

func TestResourceCTEClientGuardPoint(t *testing.T) {
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{

			// Step 1: Create Policy + Client + GuardPoint
			{
				Config: providerConfig + `
resource "ciphertrust_cte_policy" "policy" {
  name = "test-policy"
  policy_type = "Standard"

  security_rules = [{
    effect = "permit,audit"
    action = "all_ops"
  }]
}

resource "ciphertrust_cte_client" "client" {
  name                     = "testClientGP"
  password_creation_method = "GENERATE"
}

resource "ciphertrust_cte_client_guardpoint" "gp" {
  client_id   = ciphertrust_cte_client.client.id

  guard_paths = ["/tmp/testpath1"]

  guard_point_params = {
    guard_point_type = "directory_auto"
    policy_id        = ciphertrust_cte_policy.policy.name
  }
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "id"),
				),
			},

			// Step 2: Update GuardPoint
			{
				Config: providerConfig + `
resource "ciphertrust_cte_policy" "policy" {
  name = "test-policy"
  policy_type = "Standard"

  security_rules = [{
    effect = "permit,audit"
    action = "all_ops"
  }]
}

resource "ciphertrust_cte_client" "client" {
  name                     = "testClientGP"
  password_creation_method = "GENERATE"
}

resource "ciphertrust_cte_client_guardpoint" "gp" {
  client_id   = ciphertrust_cte_client.client.id

  guard_paths = ["/tmp/testpath1"]

  guard_point_params = {
    guard_point_type = "directory_auto"
    policy_id        = ciphertrust_cte_policy.policy.name
    guard_enabled    = false
  }
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "id"),
				),
			},
			// Delete testing automatically occurs in TestCase
		},
	})
}
