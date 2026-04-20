# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_ldtcommgroup_clients_list  data source can be used.


## Configure CipherTrust Manager

### Edit the provider block in main.tf

```bash
provider "ciphertrust" {
  address  = "https://cm-address"
  username = "cm-username"
  password = "cm-password"
  domain   = "cm-domain"
  bootstrap = "no"
}
```

## Configure CTE LDT comm group clients data source

### Edit the CTE LST comm group clients data source in main.tf

```bash
# Data source for retrieving LDT CommGroup Client  details
data "ciphertrust_cte_ldtcommgroup_clients_list" "example" {
  #Provide group name for which clients needs to be retrieved
  group_name = ""
}

output "clients" {
  # Output the list of LDTComm group clients retrieved from the data source
  value = "${data.ciphertrust_cte_ldtcommgroup_clients_list.example.clients}"
}
```

## Run the Example

```bash
terraform init
terraform apply
```

## Destroy Resources
Resources must be destroyed before another sample script using the same cloud is run.

```bash
terraform destroy
```

Run this step even if the apply step fails.