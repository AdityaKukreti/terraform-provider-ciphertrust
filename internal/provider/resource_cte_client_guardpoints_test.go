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
  name        = "TF_CTE_Policy_Test"
  policy_type = "Standard"
  description = "Created via TF test"
  never_deny  = true

  security_rules = [{
    effect = "permit,audit"
    action = "all_ops"
  }]
}

resource "ciphertrust_cte_client" "client" {
  name                     = "TF_CTE_Client_Test"
  client_type              = "FS"
  registration_allowed     = true
  communication_enabled    = true
  description              = "Created via TF test"
  password_creation_method = "GENERATE"
  labels = {
    color = "blue"
  }
}

resource "ciphertrust_cte_client_guardpoint" "gp" {
  client_id = ciphertrust_cte_client.client.id

  guard_points = {
    "/tmp/testpath1" = {
      guard_point_params = {
        guard_point_type = "directory_auto"
        policy_id        = ciphertrust_cte_policy.policy.id
      }
    }
  }
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "id"),
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "client_id"),
				),
			},

			// Step 2: Update GuardPoint (disable guard_enabled)
			{
				Config: providerConfig + `
resource "ciphertrust_cte_policy" "policy" {
  name        = "TF_CTE_Policy_Test"
  policy_type = "Standard"
  description = "Created via TF test"
  never_deny  = true

  security_rules = [{
    effect = "permit,audit"
    action = "all_ops"
  }]
}

resource "ciphertrust_cte_client" "client" {
  name                     = "TF_CTE_Client_Test"
  client_type              = "FS"
  registration_allowed     = true
  communication_enabled    = true
  description              = "Created via TF test"
  password_creation_method = "GENERATE"
  labels = {
    color = "blue"
  }
}

resource "ciphertrust_cte_client_guardpoint" "gp" {
  client_id = ciphertrust_cte_client.client.id

  guard_points = {
    "/tmp/testpath1" = {
      guard_point_params = {
        guard_point_type = "directory_auto"
        policy_id        = ciphertrust_cte_policy.policy.id
        guard_enabled    = false
      }
    }
  }
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "id"),
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "client_id"),
				),
			},

			// Step 3: Add a second guard path
			{
				Config: providerConfig + `
resource "ciphertrust_cte_policy" "policy" {
  name        = "TF_CTE_Policy_Test"
  policy_type = "Standard"
  description = "Created via TF test"
  never_deny  = true

  security_rules = [{
    effect = "permit,audit"
    action = "all_ops"
  }]
}

resource "ciphertrust_cte_client" "client" {
  name                     = "TF_CTE_Client_Test"
  client_type              = "FS"
  registration_allowed     = true
  communication_enabled    = true
  description              = "Created via TF test"
  password_creation_method = "GENERATE"
  labels = {
    color = "blue"
  }
}

resource "ciphertrust_cte_client_guardpoint" "gp" {
  client_id = ciphertrust_cte_client.client.id

  guard_points = {
    "/tmp/testpath1" = {
      guard_point_params = {
        guard_point_type = "directory_auto"
        policy_id        = ciphertrust_cte_policy.policy.id
        guard_enabled    = false
      }
    }
    "/tmp/testpath2" = {
      guard_point_params = {
        guard_point_type = "directory_auto"
        policy_id        = ciphertrust_cte_policy.policy.id
      }
    }
  }
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "id"),
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "client_id"),
				),
			},

			// Step 4: Remove first guard path (tests unguard path in Update)
			{
				Config: providerConfig + `
resource "ciphertrust_cte_policy" "policy" {
  name        = "TF_CTE_Policy_Test"
  policy_type = "Standard"
  description = "Created via TF test"
  never_deny  = true

  security_rules = [{
    effect = "permit,audit"
    action = "all_ops"
  }]
}

resource "ciphertrust_cte_client" "client" {
  name                     = "TF_CTE_Client_Test"
  client_type              = "FS"
  registration_allowed     = true
  communication_enabled    = true
  description              = "Created via TF test"
  password_creation_method = "GENERATE"
  labels = {
    color = "blue"
  }
}

resource "ciphertrust_cte_client_guardpoint" "gp" {
  client_id = ciphertrust_cte_client.client.id

  guard_points = {
    "/tmp/testpath2" = {
      guard_point_params = {
        guard_point_type = "directory_auto"
        policy_id        = ciphertrust_cte_policy.policy.id
      }
    }
  }
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "id"),
					resource.TestCheckResourceAttrSet("ciphertrust_cte_client_guardpoint.gp", "client_id"),
				),
			},

			// Delete testing automatically occurs in TestCase
		},
	})
}
