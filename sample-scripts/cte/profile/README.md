# Configure a CipherTrust Transparent Encryption Client Profile on CipherTrust Manager

This example shows how to:
- Create a CipherTrust Transparent Encryption Client Profile on CipherTrust Manager

These steps explain how to:
- Configure CipherTrust Manager Provider parameters required to run the examples
- Configure CTE Client Profile parameters required to create a CTE Client Profile
- Run the example

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

## Configure CTE Client Profile Parameters
Edit the CTE Client Profile resource in main.tf with actual values:
```bash
resource "ciphertrust_cte_profile" "profile" {
  name        = "TEST_API_Profile1"
  description = "Testing profile using Terraforms"

  cache_settings = {
    max_space = 500
    max_files = 250
  }

  concise_logging = true

  duplicate_settings = {
    suppress_threshold = 20
    suppress_interval  = 500
  }

  file_settings = {
    allow_purge    = true
    max_old_files  = 10
    max_file_size  = 2000000
    file_threshold = "ERROR"
  }

  client_logging_configuration = {
    threshold      = "ERROR"
    duplicates     = "SUPPRESS"
    syslog_enabled = true
    file_enabled   = true
    upload_enabled = true
  }

  syslog_settings = {
    local = true
    servers = [{
      name           = "localhost"
      port           = 22
      protocol       = "TCP"
      message_format = "LEEF"
    }]
    syslog_threshold = "ERROR"
  }

  upload_settings = {
    min_interval           = 10
    max_interval           = 20
    max_messages           = 2000
    connection_timeout     = 50
    job_completion_timeout = 600
    drop_if_busy           = true
    upload_threshold       = "ERROR"
  }
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