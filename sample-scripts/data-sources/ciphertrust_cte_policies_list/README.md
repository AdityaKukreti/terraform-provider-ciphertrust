# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_policies_list  data source can be used.


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

## Configure CTE Policies  data source

### Edit the CTE Policies  data source in main.tf

```bash
# Data source for retrieving CTE Policies  details
data "ciphertrust_cte_policies_list" "example" {
  #To filter for only one policy provide its name, this is optional
  policy_name = ""
}

output "cte_policies" {
  # Output the list of CTE Policies retrieved from the data source
  value = "${data.ciphertrust_cte_policies_list.example.cte_policies}"
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
