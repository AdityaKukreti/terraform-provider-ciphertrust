# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_client_group_clients_list data source can be used.


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

## Configure CTE clients in client group data source

### Edit the CTE clients in client group data source in main.tf

```bash
# Data source for retrieving CTE clients in Client Groups
data "ciphertrust_cte_client_group_clients_list" "example" {
  # The name filter to specify which CTE clients of which client group to retrieve (replace with actual client group name )
  group_name = ""
}

output "clients" {
  # Output the list of CTE clients of Client groups retrieved from the data source
  value = "${data.ciphertrust_cte_client_group_clients_list.example.clients}"
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