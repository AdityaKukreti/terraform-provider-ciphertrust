# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_policy_signature_rules data source can be used.


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

## Configure CTE Policies Signature Rules data source

### Edit the CTE Policies Signature Rules data source in main.tf

```bash
# Data source for retrieving Signature rules details of a Policy
data "ciphertrust_cte_policy_signature_rules" "example" {
  # name of the policy of which Signature rules needed to be fetched
  policy = "policy_name"
}

output "rules" {
  # Outputs the Signature rules retrieved from the data source
  value = "${data.ciphertrust_cte_policy_signature_rules.example.rules}" 
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
