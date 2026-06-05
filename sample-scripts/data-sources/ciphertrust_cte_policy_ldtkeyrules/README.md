# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_policy_ldt_key_rules data source can be used.


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

## Configure CTE Ldt Policy Key rules data source

### Edit the CTE Ldt Policy Key rules data source in main.tf

```bash
# Data source for retrieving LDT Key rules details of a Policy
data "ciphertrust_cte_policy_ldt_key_rules" "example" {
  # name of the policy of which LDT Keyrules needed to be fetched
  policy = "policy_name"
}

output "rules" {
  # Outputs the LDT key rules retrieved from the data source
  value = "${data.ciphertrust_cte_policy_ldt_key_rules.example.rules}"
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