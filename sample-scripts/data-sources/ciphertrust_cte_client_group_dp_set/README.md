# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_client_group_dp_set data source can be used.


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

## Configure CTE DP set in client group data source

### Edit the CTE  DP set in client group data source in main.tf

```bash
# Data source for retrieving CTE DP set in client group details
data "ciphertrust_cte_client_group_dp_set" "example" {
  # The name filter to specify for which CTE Group Designated Primary Set to retrieve (replace with actual client group name)
 client_group_name = ""
}

output "client_group_dp_set" {
  # Output the list of DP set of a client group retrieved from the data source
  value = "${data.ciphertrust_cte_client_group_dp_set.example.client_group_dp_set}"
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