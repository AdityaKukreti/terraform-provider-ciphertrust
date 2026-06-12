# CDSPaaS (multi-tenant SaaS) provider configuration.
# Set `tenant` to the tenant name shown in the CDSPaaS web console.
# All other resources behave the same as on-prem CipherTrust Manager,
# except for a small set of infrastructure resources (cluster, interface,
# license, ntp, syslog, proxy, hsm_root_of_trust_setup) that are
# platform-managed and will fail at plan time if used here.

provider "ciphertrust" {
  address  = "https://api.ciphertrust.cloud"
  username = "tenant-admin@acme.com"
  password = "password"
  tenant   = "acme"
}
