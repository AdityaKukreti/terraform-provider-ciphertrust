# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_process_sets  set  data source can be used.


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

## Configure CTE Process Set data source

### Edit the CTE Process  Set  data source in main.tf

```bash
# Data source for retrieving ProcessSets
data "ciphertrust_cte_process_sets" "example" {
}

output "process_sets" {
  # Outputs the Process Sets retrieved from the data source
  value = "${data.ciphertrust_cte_process_sets.example.process_sets}"
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
