terraform {
  required_providers {
    ciphertrust = {
      source  = "ThalesGroup/CipherTrust"
      version = "1.0.0-pre3"
    }
  }
}

provider "ciphertrust" {
  address  = "https://10.10.10.10"
  username = "admin"
  password = "ChangeMe101!"
}

# Create CSI Group
resource "ciphertrust_cte_csigroup" "test_csi_group" {
  name                     = "TF_CSI_GROUP"

  kubernetes_namespace     = "default"

  kubernetes_storage_class = "standard"

  description    = "tf test csi group.."
 
  guard_policies = {
        test-csi1 = {},
        test-csi2 = {},
        test-csi3 = {},
  }


  ############################################################
  # Operation type to perform on the CSI Group
  #
  # IMPORTANT:
  # - This field is ONLY used during UPDATE operations
  # - It is IGNORED during the initial `terraform apply`
  #
  # Supported values:
  # - update                : Update description / client_profile
  # - add-clients           : Add clients to CSI group
  # - remove-clients        : Remove clients from CSI group
  # - update-guard-policies : Add/remove/Enable/Disable guard policies
 
  # op_type = "add-clients/remove-clients/update/update-guard-policies"

  # List of clients to operate on
  #
  # NOTE:
  # - Used ONLY for client-related operations: op_type = add-clients/remove-clients
  # - Ignored for other op_type values
  /*
  client_list = [
    "client1",   # Client name / hostname / UUID
    "client2"
  ]
  */

  # NOTE:
  # - when op_type = "update-guard-policies" (Using this op_type, we can add new policies or enable/disable/remove existing ones)
/*
 guard_policies = {
	test-csi1 = {},
	test-csi2 = {guard_enabled = false},
	test-csi3 = {},
}
*/

  # UPDATE OPERATIONS
  #
  # NOTE:
  # - Used ONLY when:
  #     op_type = "update"
  # - Only these fields are considered

/*  
  description    = "updated description"
  client_profile = "updated-profile"
*/

}
