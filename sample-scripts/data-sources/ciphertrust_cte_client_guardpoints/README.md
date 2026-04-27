# Google Cloud Connection Data Source

This example demonstrates how the ciphertrust_cte_client_guardpoint data source can be used.


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

## Configure CTE client guardpoints data source

### Edit the CTE client guardpoints data source in main.tf

```bash
# Data source for retreiving guardpoints of a Client
data "ciphertrust_cte_client_guardpoint" "example" {
  #Enter client_name to get guardpoint details
  client_name = ""
}

output "client_guardpoint" {
  # Output the list of guardpoints retrieved from the data source
  value = "${data.ciphertrust_cte_client_guardpoint.example.client_guardpoint}"
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