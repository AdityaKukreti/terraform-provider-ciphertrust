package provider

import (
	"testing"

	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

func TestResourceCMPolicy(t *testing.T) {
	RequireCM(t)
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + `
resource "ciphertrust_policies" "policy" {
  	name    =   "policyReadKeyOnly"
    actions =   ["ReadKey"]
    allow   =   true
    effect  =   "allow"
    conditions = [{
        path   = "context.resource.alg"
        op     = "equals"
        values = ["aes","rsa"]
    }]
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_policies.policy", "id"),
				),
			},
			// Delete testing automatically occurs in TestCase
		},
	})
}

func TestResourceCMPolicyEffectDefault(t *testing.T) {
	RequireCM(t)
	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + `
resource "ciphertrust_policies" "policy_no_effect" {
	name    =   "policyWithoutEffect"
	actions =   ["DeleteKey"]
	allow   =   false
	resources = ["kylo:*:vault:keys:*"]
	conditions = [{
		path   = "context.resource.meta.cte"
		op     = "empty"
		negate = true
	}]
}
`,
				Check: resource.ComposeAggregateTestCheckFunc(
					resource.TestCheckResourceAttrSet("ciphertrust_policies.policy_no_effect", "id"),
					resource.TestCheckResourceAttr("ciphertrust_policies.policy_no_effect", "effect", "deny"),
				),
			},
			// Delete testing automatically occurs in TestCase
		},
	})
}
