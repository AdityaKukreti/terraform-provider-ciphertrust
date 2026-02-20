terraform {
  required_providers {
    ciphertrust = {
      source = "ThalesGroup/CipherTrust"
      version = "1.0.0-pre3"
    }
  }
}

provider "ciphertrust" {
	address = "https://10.10.10.10"
	username = "admin"
	password = "ChangeMe101!"
}
resource "ciphertrust_cte_client_group" "test_cg_group_test1" {
  name = "test_cgp_1"
  cluster_type = "NON-CLUSTER"
}