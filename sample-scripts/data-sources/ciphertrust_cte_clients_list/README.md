# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_clients_list data source can be used.


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

## Configure CTE clients data source

### Edit the CTE clients data source in main.tf

```bash
# Data source for retrieving CTE clients details
data "ciphertrust_cte_clients_list" "data_client_list1" {
  # Filters to apply when retrieving the list of CTE clients
  filters = {
    # The name filter to specify which CTE clients to retrieve (replace with actual client names)
    name = "sjavlr89-sah-s3-test-cteu.sjcicd.com"
  }
}

output "cte_list" {
  # Output the list of CTE clients retrieved from the data source
  value = "${data.ciphertrust_cte_clients_list.data_client_list1.clients}"
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