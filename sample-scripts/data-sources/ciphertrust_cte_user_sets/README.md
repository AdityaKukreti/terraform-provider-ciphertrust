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

## Configure CTE user sets  data source

### Edit the CTE user sets  data source in main.tf

```bash
# Data source for retrieving User Sets
data "ciphertrust_cte_usersets" "example" {
}

output "user_sets" {
  # Outputs User Sets retrieved from the data source
  value = "${data.ciphertrust_cte_usersets.example.user_sets}"
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
