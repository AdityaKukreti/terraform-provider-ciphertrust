package provider

import (
	"testing"

	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

func TestResourceCTEClientGroupGuardPoint(t *testing.T) {
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{

			// Step 1: Create Policy + ClientGroup + GuardPoint
			{
				Config: providerConfig + `
resource "ciphertrust_cte_policy" "policy" {
  name        = "test-policy-cg"
  policy_type = "Standard"

  security_rules = [{
    effect = "permit,audit"
    action = "all_ops"
  }]
}

resource "ciphertrust_cte_client_group" "cg" {
  name         = "testClientGroupGP"
  cluster_type = "NON-CLUSTER"
}

resource "ciphertrust_cte_clientgroup_guardpoint" "gp" {
  client_group_id = ciphertrust_cte_client_group.cg.id

  guard_paths = ["/tmp/testpathcg"]

  guard_point_params = {
    guard_point_type = "directory_auto"
    policy_id        = ciphertrust_cte_policy.policy.name
  }
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_clientgroup_guardpoint.gp", "id"),
				),
			},

			// Step 2: Update GuardPoint
			{
				Config: providerConfig + `
resource "ciphertrust_cte_policy" "policy" {
  name        = "test-policy-cg"
  policy_type = "Standard"

  security_rules = [{
    effect = "permit,audit"
    action = "all_ops"
  }]
}

resource "ciphertrust_cte_client_group" "cg" {
  name         = "testClientGroupGP"
  cluster_type = "NON-CLUSTER"
}

resource "ciphertrust_cte_clientgroup_guardpoint" "gp" {
  client_group_id = ciphertrust_cte_client_group.cg.id

  guard_paths = ["/tmp/testpathcg"]

  guard_point_params = {
    guard_point_type = "directory_auto"
    policy_id        = ciphertrust_cte_policy.policy.name
    guard_enabled    = false
  }
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_clientgroup_guardpoint.gp", "id"),
				),
			},
			// Delete testing automatically occurs in TestCase
		},
	})
}
