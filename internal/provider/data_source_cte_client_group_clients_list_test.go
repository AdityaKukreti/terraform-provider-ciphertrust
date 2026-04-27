package provider

import (
	"fmt"
	"testing"

	"github.com/google/uuid"
	"github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

func TestCiphertrustCTEClientGroupClientsDataSource(t *testing.T) {
	clientGroupName := "tf-cg-" + uuid.New().String()[:8]
	clientName := "tf-client-" + uuid.New().String()[:8]

	testConfigStep1 := fmt.Sprintf(`
		resource "ciphertrust_cte_client" "client" {
			name                     = "%s"
			password_creation_method = "GENERATE"
		}

		resource "ciphertrust_cte_client_group" "cg" {
			name         = "%s"
			description  = "Created for CTE client group clients data source test"
			cluster_type = "NON-CLUSTER"
		}
	`, clientName, clientGroupName)

	testConfigStep2 := fmt.Sprintf(`
		resource "ciphertrust_cte_client" "client" {
			name                     = "%s"
			password_creation_method = "GENERATE"
		}

		resource "ciphertrust_cte_client_group" "cg" {
			name               = "%s"
			description        = "Created for CTE client group clients data source test"
			cluster_type       = "NON-CLUSTER"
			op_type            = "add-client"
			client_list        = [ciphertrust_cte_client.client.id]
			inherit_attributes = true
		}

		data "ciphertrust_cte_client_group_clients_list" "ds" {
			group_name = ciphertrust_cte_client_group.cg.name
			depends_on = [ciphertrust_cte_client_group.cg]
		}
	`, clientName, clientGroupName)

	testConfigStep3 := fmt.Sprintf(`
		resource "ciphertrust_cte_client" "client" {
			name                     = "%s"
			password_creation_method = "GENERATE"
		}

		resource "ciphertrust_cte_client_group" "cg" {
			name               = "%s"
			description        = "Created for CTE client group clients data source test"
			cluster_type       = "NON-CLUSTER"
			op_type            = "remove-client"
			client_list        = [ciphertrust_cte_client.client.id]
		}
	`, clientName, clientGroupName)

	datasourceName := "data.ciphertrust_cte_client_group_clients_list.ds"
	clientGroupResourceName := "ciphertrust_cte_client_group.cg"
	clientResourceName := "ciphertrust_cte_client.client"

	resource.Test(t, resource.TestCase{
		ProtoV6ProviderFactories: testAccProtoV6ProviderFactories,
		Steps: []resource.TestStep{
			{
				Config: providerConfig + testConfigStep1,
				Check: resource.ComposeTestCheckFunc(
					resource.TestCheckResourceAttrSet(clientResourceName, "id"),
					resource.TestCheckResourceAttrSet(clientGroupResourceName, "id"),
				),
			},
			{
				Config: providerConfig + testConfigStep2,
				Check: resource.ComposeTestCheckFunc(
					// Check data source attributes
					resource.TestCheckResourceAttr(datasourceName, "group_name", clientGroupName),
					resource.TestCheckResourceAttr(datasourceName, "clients.#", "1"),
					resource.TestCheckResourceAttr(datasourceName, "clients.0.name", clientName),
					resource.TestCheckResourceAttrPair(datasourceName, "clients.0.id", clientResourceName, "id"),
				),
			},
			{
				// Remove the client from the group so the post-test destroy succeeds
				Config: providerConfig + testConfigStep3,
				Check: resource.ComposeTestCheckFunc(
					resource.TestCheckResourceAttrSet(clientResourceName, "id"),
					resource.TestCheckResourceAttrSet(clientGroupResourceName, "id"),
				),
			},
		},
	})
}
