# All operations

One line per swagger operation. Format: `<area> | <VERB> <path> | <tag> | <summary>`.

Grep this file for keywords (e.g. "azure key", "rotate", "create-hyok"), then open the area JSON listed in the left column.

```
auth-users         | POST   /v1/auth/akeyless/tokens                                               | Tokens                              | Create Akeyless Token
auth-users         | GET    /v1/auth/auth-key                                                      | Tokens                              | List
auth-users         | GET    /v1/auth/banners/post-auth                                             | Banners                             | Get
auth-users         | PATCH  /v1/auth/banners/post-auth                                             | Banners                             | Set
auth-users         | GET    /v1/auth/banners/pre-auth                                              | Banners                             | Get
auth-users         | PATCH  /v1/auth/banners/pre-auth                                              | Banners                             | Set
auth-users         | PATCH  /v1/auth/changepw                                                      | Users                               | Change password
auth-users         | GET    /v1/auth/id-providers                                                  | Identity Providers                  | Get
auth-users         | GET    /v1/auth/id-providers/{id}/login                                       | Identity Providers                  | Login
auth-users         | POST   /v1/auth/id-providers/{id}/login                                       | Identity Providers                  | Login
auth-users         | GET    /v1/auth/jwks.json                                                     | Tokens                              | List
auth-users         | POST   /v1/auth/logout                                                        | Tokens                              | Post
auth-users         | POST   /v1/auth/oidc-callback                                                 | Identity Providers                  | Post
auth-users         | POST   /v1/auth/revoke                                                        | Tokens                              | Revoke
auth-users         | POST   /v1/auth/rotate-auth-key                                               | Tokens                              | Rotate
auth-users         | GET    /v1/auth/self/domains                                                  | Tokens                              | Get
auth-users         | POST   /v1/auth/self/permissions                                              | Permissions                         | Query
auth-users         | GET    /v1/auth/self/pwdpolicy                                                | Users                               | Get password policy for self
auth-users         | GET    /v1/auth/self/user                                                     | Users                               | Get
auth-users         | PATCH  /v1/auth/self/user                                                     | Users                               | Update
auth-users         | GET    /v1/auth/tokens/                                                       | Tokens                              | List
auth-users         | POST   /v1/auth/tokens/                                                       | Tokens                              | Create
auth-users         | DELETE /v1/auth/tokens/{id}                                                   | Tokens                              | Delete
auth-users         | GET    /v1/auth/tokens/{id}                                                   | Tokens                              | Get
auth-users         | DELETE /v1/client-management/groups/{name}/clients/{client_id}                | Groups                              | Remove client
auth-users         | POST   /v1/client-management/groups/{name}/clients/{client_id}                | Groups                              | Add client
auth-users         | GET    /v1/domain                                                             | Domains                             | get
auth-users         | POST   /v1/domain-syslog-redirection/disable                                  | Domains                             | Disable Syslog Messages Redirection
auth-users         | POST   /v1/domain-syslog-redirection/enable                                   | Domains                             | Enable Syslog Messages Redirection
auth-users         | GET    /v1/domain-syslog-redirection/status                                   | Domains                             | Syslog Messages Redirection Status
auth-users         | GET    /v1/domains                                                            | Domains                             | List
auth-users         | POST   /v1/domains                                                            | Domains                             | Create
auth-users         | DELETE /v1/domains/{id}                                                       | Domains                             | Delete
auth-users         | GET    /v1/domains/{id}                                                       | Domains                             | Get
auth-users         | PATCH  /v1/domains/{id}                                                       | Domains                             | Update
auth-users         | GET    /v1/domains/{id}/keks                                                  | Domains                             | List domain KEKs
auth-users         | GET    /v1/domains/{id}/keks/{kekID}                                          | Domains                             | Get domain KEK
auth-users         | POST   /v1/domains/{id}/retry-kek-rotation                                    | Domains                             | Retry Domain KEK Rotation
auth-users         | POST   /v1/domains/{id}/rotate-kek                                            | Domains                             | Rotate KEK
auth-users         | GET    /v1/usermgmt/groups/                                                   | Groups                              | List
auth-users         | POST   /v1/usermgmt/groups/                                                   | Groups                              | Create
auth-users         | DELETE /v1/usermgmt/groups/{name}                                             | Groups                              | Delete
auth-users         | GET    /v1/usermgmt/groups/{name}                                             | Groups                              | Get
auth-users         | PATCH  /v1/usermgmt/groups/{name}                                             | Groups                              | Update
auth-users         | DELETE /v1/usermgmt/groups/{name}/users/{user_id}                             | Groups                              | Remove user
auth-users         | POST   /v1/usermgmt/groups/{name}/users/{user_id}                             | Groups                              | Add user
auth-users         | GET    /v1/usermgmt/pwdpolicies/                                              | Users                               | List password policies
auth-users         | POST   /v1/usermgmt/pwdpolicies/                                              | Users                               | Create a password policy
auth-users         | GET    /v1/usermgmt/pwdpolicies/global                                        | Users                               | Get global password policy
auth-users         | PATCH  /v1/usermgmt/pwdpolicies/global                                        | Users                               | Change global password policy
auth-users         | DELETE /v1/usermgmt/pwdpolicies/{policy_name}                                 | Users                               | Delete password policy
auth-users         | GET    /v1/usermgmt/pwdpolicies/{policy_name}                                 | Users                               | Get password policy
auth-users         | PATCH  /v1/usermgmt/pwdpolicies/{policy_name}                                 | Users                               | Change password policy
auth-users         | GET    /v1/usermgmt/users/                                                    | Users                               | List
auth-users         | POST   /v1/usermgmt/users/                                                    | Users                               | Create
auth-users         | DELETE /v1/usermgmt/users/{user_id}                                           | Users                               | Delete
auth-users         | GET    /v1/usermgmt/users/{user_id}                                           | Users                               | Get
auth-users         | PATCH  /v1/usermgmt/users/{user_id}                                           | Users                               | Update
cckm-aws           | POST   /v1/cckm/aws/accounts                                                  | CCKM/AWSKms                         | List account
cckm-aws           | POST   /v1/cckm/aws/alias/verify                                              | CCKM/AWSKeys                        | Verify alias
cckm-aws           | GET    /v1/cckm/aws/bulkjob                                                   | CCKM/AWSKeys Bulk Job               | List
cckm-aws           | POST   /v1/cckm/aws/bulkjob                                                   | CCKM/AWSKeys Bulk Job               | Create
cckm-aws           | GET    /v1/cckm/aws/bulkjob/{id}                                              | CCKM/AWSKeys Bulk Job               | Get
cckm-aws           | POST   /v1/cckm/aws/bulkjob/{id}/cancel                                       | CCKM/AWSKeys Bulk Job               | Cancel
cckm-aws           | POST   /v1/cckm/aws/create-hyok-key                                           | CCKM/AWS Custom Key Stores          | Create AWS HYOK Key
cckm-aws           | GET    /v1/cckm/aws/custom-key-stores                                         | CCKM/AWS Custom Key Stores          | List
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores                                         | CCKM/AWS Custom Key Stores          | Create
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/get-unused-cloudhsm-clusters            | CCKM/AWS Custom Key Stores          | List unused AWS CloudHSM clusters
cckm-aws           | GET    /v1/cckm/aws/custom-key-stores/synchronization-jobs                    | CCKM/AWS Custom Key Stores          | Status
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/synchronization-jobs                    | CCKM/AWS Custom Key Stores          | Synchronize
cckm-aws           | GET    /v1/cckm/aws/custom-key-stores/synchronization-jobs/{id}               | CCKM/AWS Custom Key Stores          | Get
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/synchronization-jobs/{id}/cancel        | CCKM/AWS Custom Key Stores          | Cancel
cckm-aws           | DELETE /v1/cckm/aws/custom-key-stores/{customKeyStoreID}/credentials/{id}     | CCKM/AWS Custom Key Stores          | Delete
cckm-aws           | GET    /v1/cckm/aws/custom-key-stores/{customKeyStoreID}/credentials/{id}     | CCKM/AWS Custom Key Stores          | Get
cckm-aws           | DELETE /v1/cckm/aws/custom-key-stores/{id}                                    | CCKM/AWS Custom Key Stores          | Delete
cckm-aws           | GET    /v1/cckm/aws/custom-key-stores/{id}                                    | CCKM/AWS Custom Key Stores          | Get
cckm-aws           | PATCH  /v1/cckm/aws/custom-key-stores/{id}                                    | CCKM/AWS Custom Key Stores          | Edit
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/{id}/block                              | CCKM/AWS Custom Key Stores          | Block access to an AWS custom key store.
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/{id}/connect                            | CCKM/AWS Custom Key Stores          | Connect
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/{id}/create-aws-key                     | CCKM/AWS Custom Key Stores          | Creates a KMS key in a custom key store that is backed by a CloudHSM.
cckm-aws           | GET    /v1/cckm/aws/custom-key-stores/{id}/credentials                        | CCKM/AWS Custom Key Stores          | List
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/{id}/disable-credential-rotation-job    | CCKM/AWS Custom Key Stores (Schedule Rotation) | Disable custom key store for credentials rotation job.
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/{id}/disconnect                         | CCKM/AWS Custom Key Stores          | Disconnect
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/{id}/enable-credential-rotation-job     | CCKM/AWS Custom Key Stores (Schedule Rotation) | Enable custom key store for credentials rotation job.
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/{id}/link                               | CCKM/AWS Custom Key Stores          | Link local CKS with AWS
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/{id}/rotate-credential                  | CCKM/AWS Custom Key Stores          | Rotate
cckm-aws           | POST   /v1/cckm/aws/custom-key-stores/{id}/unblock                            | CCKM/AWS Custom Key Stores          | Unblock access to an AWS custom key store
cckm-aws           | GET    /v1/cckm/aws/custom-key-stores/{keystore_id}/health                    | CCKM/AWS Custom Key Stores          | Custom key store health check
cckm-aws           | POST   /v1/cckm/aws/get-all-regions                                           | CCKM/AWSKms                         | List all regions
cckm-aws           | POST   /v1/cckm/aws/get-iam-roles                                             | CCKM/AWS IAM                        | List
cckm-aws           | POST   /v1/cckm/aws/get-iam-users                                             | CCKM/AWS IAM                        | List
cckm-aws           | POST   /v1/cckm/aws/get-log-groups                                            | CCKM/AWSReports                     | Log Groups
cckm-aws           | GET    /v1/cckm/aws/keys                                                      | CCKM/AWSKeys                        | List
cckm-aws           | POST   /v1/cckm/aws/keys                                                      | CCKM/AWSKeys                        | Create
cckm-aws           | DELETE /v1/cckm/aws/keys/{id}                                                 | CCKM/AWSKeys                        | Delete
cckm-aws           | GET    /v1/cckm/aws/keys/{id}                                                 | CCKM/AWSKeys                        | Get
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/add-alias                                       | CCKM/AWSKeys                        | Add alias
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/add-tags                                        | CCKM/AWSKeys                        | Add tags
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/block                                           | CCKM/AWS Custom Key Stores          | Block AWS HYOK Key
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/cancel-deletion                                 | CCKM/AWSKeys                        | Cancel delete
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/delete-alias                                    | CCKM/AWSKeys                        | Delete alias
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/delete-material                                 | CCKM/AWSKeys                        | Delete key material
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/disable                                         | CCKM/AWSKeys                        | Disable key
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/disable-auto-rotation                           | CCKM/AWSKeys                        | Disable key rotation
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/disable-rotation-job                            | CCKM/AWSKeys                        | Disable key for rotation job.
cckm-aws           | GET    /v1/cckm/aws/keys/{id}/download-public-key                             | CCKM/AWSKeys                        | Download a public key for an asymmetric key.
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/enable                                          | CCKM/AWSKeys                        | Enable key
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/enable-auto-rotation                            | CCKM/AWSKeys                        | Enable key rotation
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/enable-rotation-job                             | CCKM/AWSKeys                        | Enable key for rotation job
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/get-key-rotation-status                         | CCKM/AWSKeys                        | Get key rotation status
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/import-material                                 | CCKM/AWSKeys                        | Import
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/link                                            | CCKM/AWS Custom Key Stores          | Link an unlinked AWS HYOK Key
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/policy                                          | CCKM/AWSKeys                        | Update key policy
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/refresh                                         | CCKM/AWSKeys                        | Refreshes the key details and updates with the latest values.
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/remove-tags                                     | CCKM/AWSKeys                        | Remove tags
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/replicate-key                                   | CCKM/AWSKeys                        | Replicate multi region primary key
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/rotate                                          | CCKM/AWSKeys                        | Rotate
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/rotate-material                                 | CCKM/AWSKeys                        | Rotate key material
cckm-aws           | GET    /v1/cckm/aws/keys/{id}/rotations                                       | CCKM/AWSKeys                        | List
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/schedule-deletion                               | CCKM/AWSKeys                        | Schedule Deletion
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/unblock                                         | CCKM/AWS Custom Key Stores          | Unblock AWS HYOK Key
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/update-description                              | CCKM/AWSKeys                        | Update key description
cckm-aws           | POST   /v1/cckm/aws/keys/{id}/update-primary-region                           | CCKM/AWSKeys                        | Changes the primary key of a multi-region key.
cckm-aws           | GET    /v1/cckm/aws/keys/{id}/versions                                        | CCKM/AWS Custom Key Stores          | List
cckm-aws           | GET    /v1/cckm/aws/kms                                                       | CCKM/AWSKms                         | List AWS KMS
cckm-aws           | POST   /v1/cckm/aws/kms                                                       | CCKM/AWSKms                         | Add AWS KMS
cckm-aws           | DELETE /v1/cckm/aws/kms/{id}                                                  | CCKM/AWSKms                         | Delete
cckm-aws           | GET    /v1/cckm/aws/kms/{id}                                                  | CCKM/AWSKms                         | Get
cckm-aws           | PATCH  /v1/cckm/aws/kms/{id}                                                  | CCKM/AWSKms                         | Update
cckm-aws           | POST   /v1/cckm/aws/kms/{id}/archive                                          | CCKM/AWSKms                         | Archive KMS container
cckm-aws           | POST   /v1/cckm/aws/kms/{id}/recover                                          | CCKM/AWSKms                         | Recover KMS container
cckm-aws           | POST   /v1/cckm/aws/kms/{id}/update-acls                                      | CCKM/AWSKms                         | User ACLs
cckm-aws           | GET    /v1/cckm/aws/reports                                                   | CCKM/AWSReports                     | List Reports
cckm-aws           | POST   /v1/cckm/aws/reports                                                   | CCKM/AWSReports                     | Generate a report
cckm-aws           | DELETE /v1/cckm/aws/reports/{id}                                              | CCKM/AWSReports                     | Delete
cckm-aws           | GET    /v1/cckm/aws/reports/{id}                                              | CCKM/AWSReports                     | Get Report
cckm-aws           | GET    /v1/cckm/aws/reports/{id}/contents                                     | CCKM/AWSReports                     | Get Contents
cckm-aws           | GET    /v1/cckm/aws/reports/{id}/download                                     | CCKM/AWSReports                     | Get CSV Contents
cckm-aws           | GET    /v1/cckm/aws/synchronization-jobs                                      | CCKM/AWSKeys                        | Status
cckm-aws           | POST   /v1/cckm/aws/synchronization-jobs                                      | CCKM/AWSKeys                        | Synchronize
cckm-aws           | GET    /v1/cckm/aws/synchronization-jobs/{id}                                 | CCKM/AWSKeys                        | Get
cckm-aws           | POST   /v1/cckm/aws/synchronization-jobs/{id}/cancel                          | CCKM/AWSKeys                        | Cancel
cckm-aws           | GET    /v1/cckm/aws/templates                                                 | CCKM/AWSKeys                        | List
cckm-aws           | POST   /v1/cckm/aws/templates                                                 | CCKM/AWSKeys                        | Create
cckm-aws           | DELETE /v1/cckm/aws/templates/{id}                                            | CCKM/AWSKeys                        | Delete
cckm-aws           | GET    /v1/cckm/aws/templates/{id}                                            | CCKM/AWSKeys                        | Get
cckm-aws           | PATCH  /v1/cckm/aws/templates/{id}                                            | CCKM/AWSKeys                        | Update
cckm-aws           | POST   /v1/cckm/aws/upload-key                                                | CCKM/AWSKeys                        | Upload
cckm-aws           | POST   /v1/cckm/aws/xks-proxy-endpoints/{keystore_id}/kms/xks/v1/health       | CCKM/AWS Custom Key Stores (Data Plane) | Get health status
cckm-aws           | POST   /v1/cckm/aws/xks-proxy-endpoints/{keystore_id}/kms/xks/v1/keys/{xks_key_id}/decrypt | CCKM/AWS Custom Key Stores (Data Plane) | Decrypt data
cckm-aws           | POST   /v1/cckm/aws/xks-proxy-endpoints/{keystore_id}/kms/xks/v1/keys/{xks_key_id}/encrypt | CCKM/AWS Custom Key Stores (Data Plane) | Encrypt data
cckm-aws           | POST   /v1/cckm/aws/xks-proxy-endpoints/{keystore_id}/kms/xks/v1/keys/{xks_key_id}/metadata | CCKM/AWS Custom Key Stores (Data Plane) | Get key metadata
cckm-aws           | GET    /v1/cckm/virtual/keys                                                  | CCKM/AWS Custom Key Stores          | List
cckm-aws           | POST   /v1/cckm/virtual/keys                                                  | CCKM/AWS Custom Key Stores          | Create
cckm-aws           | DELETE /v1/cckm/virtual/keys/{id}                                             | CCKM/AWS Custom Key Stores          | Delete virtual key
cckm-aws           | GET    /v1/cckm/virtual/keys/{id}                                             | CCKM/AWS Custom Key Stores          | Get virtual key
cckm-aws           | PATCH  /v1/cckm/virtual/keys/{id}                                             | CCKM/AWS Custom Key Stores          | Update virtual key
cckm-aws           | GET    /v1/cckm/virtual/keys/{id}/versions                                    | CCKM/AWS Custom Key Stores          | List
cckm-azure         | POST   /v1/cckm/azure/add-vaults                                              | CCKM/AzureVaults                    | Add Azure Vault
cckm-azure         | GET    /v1/cckm/azure/bulkjobs                                                | CCKM/Azure Bulk Job                 | List
cckm-azure         | POST   /v1/cckm/azure/bulkjobs                                                | CCKM/Azure Bulk Job                 | Create
cckm-azure         | DELETE /v1/cckm/azure/bulkjobs/{id}                                           | CCKM/Azure Bulk Job                 | Delete
cckm-azure         | GET    /v1/cckm/azure/bulkjobs/{id}                                           | CCKM/Azure Bulk Job                 | Get
cckm-azure         | POST   /v1/cckm/azure/bulkjobs/{id}/cancel                                    | CCKM/Azure Bulk Job                 | Cancel
cckm-azure         | GET    /v1/cckm/azure/certificates                                            | CCKM/AzureCertificates              | List
cckm-azure         | POST   /v1/cckm/azure/certificates                                            | CCKM/AzureCertificates              | Create
cckm-azure         | POST   /v1/cckm/azure/certificates/import                                     | CCKM/AzureCertificates              | Import
cckm-azure         | GET    /v1/cckm/azure/certificates/synchronization-jobs                       | CCKM/AzureCertificates              | Status
cckm-azure         | POST   /v1/cckm/azure/certificates/synchronization-jobs                       | CCKM/AzureCertificates              | Synchronize
cckm-azure         | GET    /v1/cckm/azure/certificates/synchronization-jobs/{id}                  | CCKM/AzureCertificates              | Get
cckm-azure         | POST   /v1/cckm/azure/certificates/synchronization-jobs/{id}/cancel           | CCKM/AzureCertificates              | Cancel
cckm-azure         | DELETE /v1/cckm/azure/certificates/{id}                                       | CCKM/AzureCertificates              | Delete
cckm-azure         | GET    /v1/cckm/azure/certificates/{id}                                       | CCKM/AzureCertificates              | Get
cckm-azure         | PATCH  /v1/cckm/azure/certificates/{id}                                       | CCKM/AzureCertificates              | Update
cckm-azure         | POST   /v1/cckm/azure/certificates/{id}/hard-delete                           | CCKM/AzureCertificates              | Purge
cckm-azure         | POST   /v1/cckm/azure/certificates/{id}/recover                               | CCKM/AzureCertificates              | Recover
cckm-azure         | POST   /v1/cckm/azure/certificates/{id}/restore                               | CCKM/AzureCertificates              | Restore
cckm-azure         | POST   /v1/cckm/azure/certificates/{id}/soft-delete                           | CCKM/AzureCertificates              | Soft Delete
cckm-azure         | POST   /v1/cckm/azure/get-managed-hsms                                        | CCKM/AzureVaults                    | Get Azure managed HSM vaults
cckm-azure         | POST   /v1/cckm/azure/get-subscriptions                                       | CCKM/AzureSubscriptions             | Fetch subscriptions from Azure
cckm-azure         | POST   /v1/cckm/azure/get-vaults                                              | CCKM/AzureVaults                    | Get Azure vault
cckm-azure         | GET    /v1/cckm/azure/keys                                                    | CCKM/AzureKeys                      | List
cckm-azure         | POST   /v1/cckm/azure/keys                                                    | CCKM/AzureKeys                      | Create
cckm-azure         | GET    /v1/cckm/azure/keys/{id}                                               | CCKM/AzureKeys                      | Get
cckm-azure         | PATCH  /v1/cckm/azure/keys/{id}                                               | CCKM/AzureKeys                      | Update
cckm-azure         | GET    /v1/cckm/azure/keys/{id}/backups                                       | CCKM/AzureKeys                      | List Backups
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/backups                                       | CCKM/AzureKeys                      | Create Backup
cckm-azure         | DELETE /v1/cckm/azure/keys/{id}/backups/{backup_id}                           | CCKM/AzureKeys                      | Delete Backup
cckm-azure         | GET    /v1/cckm/azure/keys/{id}/backups/{backup_id}                           | CCKM/AzureKeys                      | Get Backup
cckm-azure         | PATCH  /v1/cckm/azure/keys/{id}/backups/{backup_id}                           | CCKM/AzureKeys                      | Update Backup
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/delete-backup                                 | CCKM/AzureKeys                      | Delete Backup
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/disable-backup-job                            | CCKM/AzureKeys                      | Disable key for backup job.
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/disable-rotation-job                          | CCKM/AzureKeys                      | Disable key for rotation job.
cckm-azure         | GET    /v1/cckm/azure/keys/{id}/download-public-key                           | CCKM/AzureKeys                      | Download a public key for an asymmetric key.
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/enable-backup-job                             | CCKM/AzureKeys                      | Enable key for backup job.
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/enable-rotation-job                           | CCKM/AzureKeys                      | Enable key for rotation job.
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/hard-delete                                   | CCKM/AzureKeys                      | Purge
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/recover                                       | CCKM/AzureKeys                      | Recover
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/refresh                                       | CCKM/AzureKeys                      | Refreshes the key and all the version details and updates with the latest values.
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/restore                                       | CCKM/AzureKeys                      | Restore
cckm-azure         | POST   /v1/cckm/azure/keys/{id}/soft-delete                                   | CCKM/AzureKeys                      | Soft Delete
cckm-azure         | GET    /v1/cckm/azure/reports                                                 | CCKM/AzureReports                   | List Reports
cckm-azure         | POST   /v1/cckm/azure/reports                                                 | CCKM/AzureReports                   | Generate a report
cckm-azure         | DELETE /v1/cckm/azure/reports/{id}                                            | CCKM/AzureReports                   | Delete
cckm-azure         | GET    /v1/cckm/azure/reports/{id}                                            | CCKM/AzureReports                   | Get Report
cckm-azure         | GET    /v1/cckm/azure/reports/{id}/contents                                   | CCKM/AzureReports                   | Get Contents
cckm-azure         | GET    /v1/cckm/azure/reports/{id}/download                                   | CCKM/AzureReports                   | Get CSV Contents
cckm-azure         | GET    /v1/cckm/azure/secrets                                                 | CCKM/AzureSecrets                   | List
cckm-azure         | POST   /v1/cckm/azure/secrets                                                 | CCKM/AzureSecrets                   | Create
cckm-azure         | GET    /v1/cckm/azure/secrets/synchronization-jobs                            | CCKM/AzureSecrets                   | Status
cckm-azure         | POST   /v1/cckm/azure/secrets/synchronization-jobs                            | CCKM/AzureSecrets                   | Synchronize
cckm-azure         | GET    /v1/cckm/azure/secrets/synchronization-jobs/{id}                       | CCKM/AzureSecrets                   | Get
cckm-azure         | POST   /v1/cckm/azure/secrets/synchronization-jobs/{id}/cancel                | CCKM/AzureSecrets                   | Cancel
cckm-azure         | DELETE /v1/cckm/azure/secrets/{id}                                            | CCKM/AzureSecrets                   | Delete
cckm-azure         | GET    /v1/cckm/azure/secrets/{id}                                            | CCKM/AzureSecrets                   | Get
cckm-azure         | PATCH  /v1/cckm/azure/secrets/{id}                                            | CCKM/AzureSecrets                   | Update
cckm-azure         | POST   /v1/cckm/azure/secrets/{id}/hard-delete                                | CCKM/AzureSecrets                   | Purge
cckm-azure         | POST   /v1/cckm/azure/secrets/{id}/recover                                    | CCKM/AzureSecrets                   | Recover
cckm-azure         | POST   /v1/cckm/azure/secrets/{id}/restore                                    | CCKM/AzureSecrets                   | Restore
cckm-azure         | POST   /v1/cckm/azure/secrets/{id}/soft-delete                                | CCKM/AzureSecrets                   | Soft Delete
cckm-azure         | GET    /v1/cckm/azure/subscriptions                                           | CCKM/AzureSubscriptions             | List Subscriptions
cckm-azure         | DELETE /v1/cckm/azure/subscriptions/{id}                                      | CCKM/AzureSubscriptions             | Delete
cckm-azure         | GET    /v1/cckm/azure/subscriptions/{id}                                      | CCKM/AzureSubscriptions             | Get
cckm-azure         | GET    /v1/cckm/azure/synchronization-jobs                                    | CCKM/AzureKeys                      | Status
cckm-azure         | POST   /v1/cckm/azure/synchronization-jobs                                    | CCKM/AzureKeys                      | Synchronize
cckm-azure         | GET    /v1/cckm/azure/synchronization-jobs/{id}                               | CCKM/AzureKeys                      | Get
cckm-azure         | POST   /v1/cckm/azure/synchronization-jobs/{id}/cancel                        | CCKM/AzureKeys                      | Cancel
cckm-azure         | POST   /v1/cckm/azure/upload-key                                              | CCKM/AzureKeys                      | Upload
cckm-azure         | GET    /v1/cckm/azure/vaults                                                  | CCKM/AzureVaults                    | List Vaults
cckm-azure         | GET    /v1/cckm/azure/vaults/{id}                                             | CCKM/AzureVaults                    | Get
cckm-azure         | PATCH  /v1/cckm/azure/vaults/{id}                                             | CCKM/AzureVaults                    | Update
cckm-azure         | POST   /v1/cckm/azure/vaults/{id}/disable-rotation-job                        | CCKM/AzureVaults                    | Disable key rotation schedule for azure key vault.
cckm-azure         | POST   /v1/cckm/azure/vaults/{id}/enable-rotation-job                         | CCKM/AzureVaults                    | Enable key rotation schedule for azure key vault.
cckm-azure         | POST   /v1/cckm/azure/vaults/{id}/remove-vault                                | CCKM/AzureVaults                    | Delete
cckm-azure         | POST   /v1/cckm/azure/vaults/{id}/update-acls                                 | CCKM/AzureVaults                    | Vault ACLS
cckm-google        | GET    /v1/cckm/GoogleWorkspaceCSE/endpoints                                  | CCKM/Google Workspace CSE           | List
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints                                  | CCKM/Google Workspace CSE           | Create
cckm-google        | DELETE /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}                             | CCKM/Google Workspace CSE           | Delete
cckm-google        | GET    /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}                             | CCKM/Google Workspace CSE           | Get
cckm-google        | PATCH  /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}                             | CCKM/Google Workspace CSE           | Update
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/archive                     | CCKM/Google Workspace CSE           | Archive Endpoint
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/delegate                    | CCKM/Google Workspace CSE (Data Plane) | Delegate
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/disable                     | CCKM/Google Workspace CSE           | Disable Endpoint
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/enable                      | CCKM/Google Workspace CSE           | Enable Endpoint
cckm-google        | GET    /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/perimeters                  | CCKM/Google Workspace CSE           | Get
cckm-google        | PUT    /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/perimeters                  | CCKM/Google Workspace CSE           | Update
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/privatekeydecrypt           | CCKM/Google Workspace CSE (Data Plane) | Unwrap the content encryption key
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/privatekeysign              | CCKM/Google Workspace CSE (Data Plane) | Signs the digest provided by the client.
cckm-google        | GET    /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/privileged-unwrap-configuration | CCKM/Google Workspace CSE           | Get
cckm-google        | PUT    /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/privileged-unwrap-configuration | CCKM/Google Workspace CSE           | Update
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/privilegedprivatekeydecrypt | CCKM/Google Workspace CSE (Data Plane) | Unwraps the data exported (takeout) from Google.
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/privilegedunwrap            | CCKM/Google Workspace CSE (Data Plane) | Privileged Unwrap
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/privilegedwrap              | CCKM/Google Workspace CSE (Data Plane) | Privileged Wrap
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/recover                     | CCKM/Google Workspace CSE           | Recover Endpoint
cckm-google        | GET    /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/rewrap-configuration        | CCKM/Google Workspace CSE           | Get
cckm-google        | PUT    /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/rewrap-configuration        | CCKM/Google Workspace CSE           | Update
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/rotate-key                  | CCKM/Google Workspace CSE           | Rotate Key
cckm-google        | GET    /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/status                      | CCKM/Google Workspace CSE           | Get
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/unwrap                      | CCKM/Google Workspace CSE (Data Plane) | Unwrap
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/wrap                        | CCKM/Google Workspace CSE (Data Plane) | Wrap
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/endpoints/{id}/wrapprivatekey              | CCKM/Google Workspace CSE           | Wrap Private Key
cckm-google        | GET    /v1/cckm/GoogleWorkspaceCSE/issuers                                    | CCKM/Google Workspace CSE           | List
cckm-google        | POST   /v1/cckm/GoogleWorkspaceCSE/issuers                                    | CCKM/Google Workspace CSE           | Create
cckm-google        | DELETE /v1/cckm/GoogleWorkspaceCSE/issuers/{id}                               | CCKM/Google Workspace CSE           | Delete
cckm-google        | GET    /v1/cckm/GoogleWorkspaceCSE/issuers/{id}                               | CCKM/Google Workspace CSE           | Get
cckm-google        | GET    /v1/cckm/ekm/cryptospaces                                              | CCKM/Google Cloud EKM CryptoSpaces  | List
cckm-google        | POST   /v1/cckm/ekm/cryptospaces                                              | CCKM/Google Cloud EKM CryptoSpaces  | Create
cckm-google        | DELETE /v1/cckm/ekm/cryptospaces/{id}                                         | CCKM/Google Cloud EKM CryptoSpaces  | Delete
cckm-google        | GET    /v1/cckm/ekm/cryptospaces/{id}                                         | CCKM/Google Cloud EKM CryptoSpaces  | Get
cckm-google        | PATCH  /v1/cckm/ekm/cryptospaces/{id}                                         | CCKM/Google Cloud EKM CryptoSpaces  | Update
cckm-google        | POST   /v1/cckm/ekm/cryptospaces/{id}/block                                   | CCKM/Google Cloud EKM CryptoSpaces  | Block access to EKM Cryptospace.
cckm-google        | POST   /v1/cckm/ekm/cryptospaces/{id}/unblock                                 | CCKM/Google Cloud EKM CryptoSpaces  | Unblock access to EKM Cryptospace.
cckm-google        | POST   /v1/cckm/ekm/cryptospaces/{id}:checkCryptoSpacePermissions             | CCKM/Google Cloud EKM CryptoSpaces (Data Plane) | Check cryptospace permissions
cckm-google        | POST   /v1/cckm/ekm/cryptospaces/{id}:createKey                               | CCKM/Google Cloud EKM CryptoSpaces (Data Plane) | Create a key in a cryptospace.
cckm-google        | GET    /v1/cckm/ekm/endpoints                                                 | CCKM/Google Cloud EKM               | List
cckm-google        | POST   /v1/cckm/ekm/endpoints                                                 | CCKM/Google Cloud EKM               | Create
cckm-google        | DELETE /v1/cckm/ekm/endpoints/{id}                                            | CCKM/Google Cloud EKM               | Delete
cckm-google        | GET    /v1/cckm/ekm/endpoints/{id}                                            | CCKM/Google Cloud EKM               | Get
cckm-google        | PATCH  /v1/cckm/ekm/endpoints/{id}                                            | CCKM/Google Cloud EKM               | Update
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}/destroy                                    | CCKM/Google Cloud EKM               | Destroy EKM Cryptospace Endpoint
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}/disable                                    | CCKM/Google Cloud EKM               | Disable EKM Endpoint
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}/enable                                     | CCKM/Google Cloud EKM               | Enable EKM Endpoint
cckm-google        | GET    /v1/cckm/ekm/endpoints/{id}/policies                                   | CCKM/Google Cloud EKM               | Get
cckm-google        | PATCH  /v1/cckm/ekm/endpoints/{id}/policies                                   | CCKM/Google Cloud EKM               | Update
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}/rotate                                     | CCKM/Google Cloud EKM               | Rotate EKM Endpoint
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}:asymmetricSign                             | CCKM/Google Cloud EKM (Data Plane)  | AsymmetricSign
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}:asymmetricVerify                           | CCKM/Google Cloud EKM (Data Plane)  | AsymmetricVerify
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}:confidentialunwrap                         | CCKM/Google Cloud EKM (Data Plane)  | Confidential Unwrap
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}:confidentialwrap                           | CCKM/Google Cloud EKM (Data Plane)  | Confidential Wrap
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}:destroyKey                                 | CCKM/Google Cloud EKM CryptoSpaces (Data Plane) | Destroys a key in a cryptospace. The key will be marked to be in a DESTROYED state.
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}:getPublicKey                               | CCKM/Google Cloud EKM (Data Plane)  | GetPublicKey
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}:unwrap                                     | CCKM/Google Cloud EKM (Data Plane)  | UnWrap
cckm-google        | POST   /v1/cckm/ekm/endpoints/{id}:wrap                                       | CCKM/Google Cloud EKM (Data Plane)  | Wrap
cckm-google        | GET    /v1/cckm/ekm/issuers                                                   | CCKM/Google Cloud EKM Issuers       | List
cckm-google        | POST   /v1/cckm/ekm/issuers                                                   | CCKM/Google Cloud EKM Issuers       | Create
cckm-google        | DELETE /v1/cckm/ekm/issuers/{id}                                              | CCKM/Google Cloud EKM Issuers       | Delete
cckm-google        | GET    /v1/cckm/ekm/issuers/{id}                                              | CCKM/Google Cloud EKM Issuers       | Get
cckm-google        | PATCH  /v1/cckm/ekm/issuers/{id}                                              | CCKM/Google Cloud EKM Issuers       | Update
cckm-google        | POST   /v1/cckm/ekm/session/beginsession                                      | CCKM/Google Cloud EKM (Data Plane)  | Begin Session
cckm-google        | POST   /v1/cckm/ekm/session/endsession                                        | CCKM/Google Cloud EKM (Data Plane)  | End Session
cckm-google        | POST   /v1/cckm/ekm/session/finalize                                          | CCKM/Google Cloud EKM (Data Plane)  | Finalize
cckm-google        | POST   /v1/cckm/ekm/session/handshake                                         | CCKM/Google Cloud EKM (Data Plane)  | Handshake
cckm-google        | POST   /v1/cckm/ekm/session/negotiateattestation                              | CCKM/Google Cloud EKM (Data Plane)  | Negotiate Attestation
cckm-google        | POST   /v1/cckm/google/add-key-rings                                          | CCKM/Google Cloud Key Rings         | Add Google Cloud KeyRings
cckm-google        | POST   /v1/cckm/google/get-iam-roles                                          | CCKM/Google Cloud Keys              | List
cckm-google        | POST   /v1/cckm/google/get-key-rings                                          | CCKM/Google Cloud Key Rings         | Get Google Cloud KeyRings
cckm-google        | POST   /v1/cckm/google/get-locations                                          | CCKM/Google Cloud Locations         | Get Google Cloud Locations
cckm-google        | POST   /v1/cckm/google/get-projects                                           | CCKM/Google Cloud Projects          | Get projects from Google Cloud
cckm-google        | GET    /v1/cckm/google/key-rings                                              | CCKM/Google Cloud Key Rings         | List Key Rings
cckm-google        | GET    /v1/cckm/google/key-rings/{id}                                         | CCKM/Google Cloud Key Rings         | Get
cckm-google        | PATCH  /v1/cckm/google/key-rings/{id}                                         | CCKM/Google Cloud Key Rings         | Update
cckm-google        | POST   /v1/cckm/google/key-rings/{id}/remove-key-ring                         | CCKM/Google Cloud Key Rings         | Delete
cckm-google        | POST   /v1/cckm/google/key-rings/{id}/update-acls                             | CCKM/Google Cloud Key Rings         | Key Ring ACLS
cckm-google        | GET    /v1/cckm/google/keys                                                   | CCKM/Google Cloud Keys              | List Keys
cckm-google        | POST   /v1/cckm/google/keys                                                   | CCKM/Google Cloud Keys              | Create
cckm-google        | GET    /v1/cckm/google/keys/{id}                                              | CCKM/Google Cloud Keys              | Gets a key
cckm-google        | PATCH  /v1/cckm/google/keys/{id}                                              | CCKM/Google Cloud Keys              | Update
cckm-google        | POST   /v1/cckm/google/keys/{id}/disable-auto-rotation                        | CCKM/Google Cloud Keys              | Disable the auto-rotation for Google Cloud Key
cckm-google        | POST   /v1/cckm/google/keys/{id}/enable-auto-rotation                         | CCKM/Google Cloud Keys              | Enables auto rotation
cckm-google        | GET    /v1/cckm/google/keys/{id}/policy                                       | CCKM/Google Cloud Keys              | Get
cckm-google        | POST   /v1/cckm/google/keys/{id}/policy                                       | CCKM/Google Cloud Keys              | Update key policy
cckm-google        | POST   /v1/cckm/google/keys/{id}/refresh                                      | CCKM/Google Cloud Keys              | Refreshes the key and all the version details and updates with the latest values.
cckm-google        | GET    /v1/cckm/google/keys/{id}/versions                                     | CCKM/Google Cloud Keys              | List
cckm-google        | POST   /v1/cckm/google/keys/{id}/versions                                     | CCKM/Google Cloud Keys              | Post
cckm-google        | GET    /v1/cckm/google/keys/{id}/versions/{versionID}                         | CCKM/Google Cloud Keys              | Get key version details.
cckm-google        | POST   /v1/cckm/google/keys/{id}/versions/{versionID}/cancel-schedule-destroy | CCKM/Google Cloud Keys              | Cancel scheduled destruction of a key version.
cckm-google        | POST   /v1/cckm/google/keys/{id}/versions/{versionID}/disable                 | CCKM/Google Cloud Keys              | Disable Key version
cckm-google        | POST   /v1/cckm/google/keys/{id}/versions/{versionID}/download-public-key     | CCKM/Google Cloud Keys              | Download a public key for an asymmetric key version.
cckm-google        | POST   /v1/cckm/google/keys/{id}/versions/{versionID}/enable                  | CCKM/Google Cloud Keys              | Enable Key version
cckm-google        | POST   /v1/cckm/google/keys/{id}/versions/{versionID}/re-import               | CCKM/Google Cloud Keys              | Re-Import Key Version.
cckm-google        | POST   /v1/cckm/google/keys/{id}/versions/{versionID}/refresh                 | CCKM/Google Cloud Keys              | Refreshes the key version details and updates with the latest version.
cckm-google        | POST   /v1/cckm/google/keys/{id}/versions/{versionID}/schedule-destroy        | CCKM/Google Cloud Keys              | Schedule destruction of a key version.
cckm-google        | GET    /v1/cckm/google/projects                                               | CCKM/Google Cloud Projects          | List Projects
cckm-google        | POST   /v1/cckm/google/projects                                               | CCKM/Google Cloud Projects          | Add
cckm-google        | DELETE /v1/cckm/google/projects/{id}                                          | CCKM/Google Cloud Projects          | Delete
cckm-google        | GET    /v1/cckm/google/projects/{id}                                          | CCKM/Google Cloud Projects          | Get
cckm-google        | PATCH  /v1/cckm/google/projects/{id}                                          | CCKM/Google Cloud Projects          | Update
cckm-google        | POST   /v1/cckm/google/projects/{id}/update-acls                              | CCKM/Google Cloud Projects          | Project ACLS
cckm-google        | GET    /v1/cckm/google/reports                                                | CCKM/Google Cloud Reports           | List Reports
cckm-google        | POST   /v1/cckm/google/reports                                                | CCKM/Google Cloud Reports           | Generate a report
cckm-google        | DELETE /v1/cckm/google/reports/{id}                                           | CCKM/Google Cloud Reports           | Delete
cckm-google        | GET    /v1/cckm/google/reports/{id}                                           | CCKM/Google Cloud Reports           | Get Report
cckm-google        | GET    /v1/cckm/google/reports/{id}/contents                                  | CCKM/Google Cloud Reports           | Get Contents
cckm-google        | GET    /v1/cckm/google/reports/{id}/download                                  | CCKM/Google Cloud Reports           | Get CSV Contents
cckm-google        | GET    /v1/cckm/google/synchronization-jobs                                   | CCKM/Google Cloud Keys              | Status
cckm-google        | POST   /v1/cckm/google/synchronization-jobs                                   | CCKM/Google Cloud Keys              | Synchronize
cckm-google        | GET    /v1/cckm/google/synchronization-jobs/{id}                              | CCKM/Google Cloud Keys              | Get
cckm-google        | POST   /v1/cckm/google/synchronization-jobs/{id}/cancel                       | CCKM/Google Cloud Keys              | Cancel
cckm-google        | POST   /v1/cckm/google/update-all-versions-jobs                               | CCKM/Google Cloud Keys              | UpdateVersions
cckm-google        | GET    /v1/cckm/google/update-all-versions-jobs/{id}                          | CCKM/Google Cloud Keys              | Get
cckm-google        | POST   /v1/cckm/google/upload-key                                             | CCKM/Google Cloud Keys              | Upload
cckm-hsm           | POST   /v1/cckm/hsm/luna/add-partition                                        | CCKM/HSMLunaPartitions              | Add Partition
cckm-hsm           | GET    /v1/cckm/hsm/luna/keys                                                 | CCKM/HSMLunaKeys                    | List
cckm-hsm           | POST   /v1/cckm/hsm/luna/keys                                                 | CCKM/HSMLunaKeys                    | Create key
cckm-hsm           | DELETE /v1/cckm/hsm/luna/keys/{id}                                            | CCKM/HSMLunaKeys                    | Delete
cckm-hsm           | GET    /v1/cckm/hsm/luna/keys/{id}                                            | CCKM/HSMLunaKeys                    | Get
cckm-hsm           | PATCH  /v1/cckm/hsm/luna/keys/{id}                                            | CCKM/HSMLunaKeys                    | Update
cckm-hsm           | POST   /v1/cckm/hsm/luna/keys/{id}/replicate                                  | CCKM/HSMLunaKeys                    | Post
cckm-hsm           | GET    /v1/cckm/hsm/luna/partitions                                           | CCKM/HSMLunaPartitions              | List
cckm-hsm           | DELETE /v1/cckm/hsm/luna/partitions/{id}                                      | CCKM/HSMLunaPartitions              | Delete
cckm-hsm           | GET    /v1/cckm/hsm/luna/partitions/{id}                                      | CCKM/HSMLunaPartitions              | Get
cckm-hsm           | PATCH  /v1/cckm/hsm/luna/partitions/{id}                                      | CCKM/HSMLunaPartitions              | Update
cckm-hsm           | POST   /v1/cckm/hsm/luna/partitions/{id}/update-acls                          | CCKM/HSMLunaPartitions              | User ACLS
cckm-hsm           | GET    /v1/cckm/hsm/luna/refresh                                              | CCKM/HSMLunaKeys                    | Status
cckm-hsm           | POST   /v1/cckm/hsm/luna/refresh                                              | CCKM/HSMLunaKeys                    | Refresh
cckm-hsm           | GET    /v1/cckm/hsm/luna/refresh/{id}                                         | CCKM/HSMLunaKeys                    | Get
cckm-hsm           | POST   /v1/cckm/hsm/luna/refresh/{id}/cancel                                  | CCKM/HSMLunaKeys                    | Cancel
cckm-hsm           | GET    /v1/cckm/hsm/luna/synchronize                                          | CCKM/HSMLunaKeys                    | Status
cckm-hsm           | POST   /v1/cckm/hsm/luna/synchronize                                          | CCKM/HSMLunaKeys                    | Synchronize
cckm-hsm           | GET    /v1/cckm/hsm/luna/synchronize/{id}                                     | CCKM/HSMLunaKeys                    | Get
cckm-hsm           | POST   /v1/cckm/hsm/luna/synchronize/{id}/cancel                              | CCKM/HSMLunaKeys                    | Cancel
cckm-hsm           | POST   /v1/cckm/hsm/luna/{id}/delete                                          | CCKM/HSMLunaKeys                    | Post
cckm-microsoft     | GET    /v1/cckm/microsoft/dke/auth-tenants                                    | CCKM/MicrosoftDKE                   | List
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/auth-tenants                                    | CCKM/MicrosoftDKE                   | Create
cckm-microsoft     | DELETE /v1/cckm/microsoft/dke/auth-tenants/{id}                               | CCKM/MicrosoftDKE                   | Delete
cckm-microsoft     | GET    /v1/cckm/microsoft/dke/auth-tenants/{id}                               | CCKM/MicrosoftDKE                   | Get
cckm-microsoft     | PATCH  /v1/cckm/microsoft/dke/auth-tenants/{id}                               | CCKM/MicrosoftDKE                   | Update
cckm-microsoft     | GET    /v1/cckm/microsoft/dke/endpoints                                       | CCKM/MicrosoftDKE                   | List
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/endpoints                                       | CCKM/MicrosoftDKE                   | Create
cckm-microsoft     | DELETE /v1/cckm/microsoft/dke/endpoints/{id}                                  | CCKM/MicrosoftDKE                   | Delete
cckm-microsoft     | GET    /v1/cckm/microsoft/dke/endpoints/{id}                                  | CCKM/MicrosoftDKE                   | Get
cckm-microsoft     | PATCH  /v1/cckm/microsoft/dke/endpoints/{id}                                  | CCKM/MicrosoftDKE                   | Update
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/endpoints/{id}/archive                          | CCKM/MicrosoftDKE                   | Archive DKE Endpoint
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/endpoints/{id}/disable                          | CCKM/MicrosoftDKE                   | Disable DKE Endpoint
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/endpoints/{id}/disable-key-rotation-job         | CCKM/MicrosoftDKE                   | Disable auto rotation schedule for DKE endpoint
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/endpoints/{id}/enable                           | CCKM/MicrosoftDKE                   | Enable DKE Endpoint
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/endpoints/{id}/enable-key-rotation-job          | CCKM/MicrosoftDKE                   | Enable auto rotation schedule for DKE endpoint
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/endpoints/{id}/recover                          | CCKM/MicrosoftDKE                   | Recover DKE Endpoint
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/endpoints/{id}/rotate                           | CCKM/MicrosoftDKE                   | Rotate DKE Endpoint
cckm-microsoft     | POST   /v1/cckm/microsoft/dke/get-roles                                       | CCKM/MicrosoftDKE                   | List
cckm-misc          | GET    /v1/cckm/cloud-units                                                   | CCKM/Cloud                          | Consumed cloud count
cckm-misc          | POST   /v1/cckm/dsm/add-domains                                               | CCKM/DSMDomains                     | Add domains
cckm-misc          | GET    /v1/cckm/dsm/domains                                                   | CCKM/DSMDomains                     | List
cckm-misc          | DELETE /v1/cckm/dsm/domains/{id}                                              | CCKM/DSMDomains                     | Delete
cckm-misc          | GET    /v1/cckm/dsm/domains/{id}                                              | CCKM/DSMDomains                     | Get
cckm-misc          | PATCH  /v1/cckm/dsm/domains/{id}                                              | CCKM/DSMDomains                     | Update
cckm-misc          | POST   /v1/cckm/dsm/domains/{id}/update-acls                                  | CCKM/DSMDomains                     | User ACLS
cckm-misc          | POST   /v1/cckm/dsm/get-domains                                               | CCKM/DSMDomains                     | Get domains from DSM
cckm-misc          | GET    /v1/cckm/dsm/keys                                                      | CCKM/DSMKeys                        | List
cckm-misc          | POST   /v1/cckm/dsm/keys                                                      | CCKM/DSMKeys                        | Create Key
cckm-misc          | DELETE /v1/cckm/dsm/keys/{id}                                                 | CCKM/DSMKeys                        | Delete
cckm-misc          | GET    /v1/cckm/dsm/keys/{id}                                                 | CCKM/DSMKeys                        | Get
cckm-misc          | POST   /v1/cckm/dsm/keys/{id}/delete                                          | CCKM/DSMKeys                        | Post
cckm-misc          | GET    /v1/cckm/dsm/refresh                                                   | CCKM/DSMKeys                        | Status
cckm-misc          | POST   /v1/cckm/dsm/refresh                                                   | CCKM/DSMKeys                        | Refresh
cckm-misc          | GET    /v1/cckm/dsm/refresh/{id}                                              | CCKM/DSMKeys                        | Get
cckm-misc          | POST   /v1/cckm/dsm/refresh/{id}/cancel                                       | CCKM/DSMKeys                        | Cancel
cckm-misc          | POST   /v1/cckm/external-cm/add-domains                                       | CCKM/CipherTrust (External) Domains | Add External CM Domains
cckm-misc          | GET    /v1/cckm/external-cm/domains                                           | CCKM/CipherTrust (External) Domains | List External CM Domains
cckm-misc          | DELETE /v1/cckm/external-cm/domains/{id}                                      | CCKM/CipherTrust (External) Domains | Delete
cckm-misc          | GET    /v1/cckm/external-cm/domains/{id}                                      | CCKM/CipherTrust (External) Domains | Get
cckm-misc          | PATCH  /v1/cckm/external-cm/domains/{id}                                      | CCKM/CipherTrust (External) Domains | Update
cckm-misc          | POST   /v1/cckm/external-cm/domains/{id}/update-acls                          | CCKM/CipherTrust (External) Domains | User ACLS
cckm-misc          | POST   /v1/cckm/external-cm/get-domains                                       | CCKM/CipherTrust (External) Domains | Get domains from external CM
cckm-misc          | GET    /v1/cckm/external-cm/keys                                              | CCKM/CipherTrust (External) Keys    | List External CM Keys
cckm-misc          | POST   /v1/cckm/external-cm/keys                                              | CCKM/CipherTrust (External) Keys    | Create
cckm-misc          | DELETE /v1/cckm/external-cm/keys/{id}                                         | CCKM/CipherTrust (External) Keys    | Delete
cckm-misc          | GET    /v1/cckm/external-cm/keys/{id}                                         | CCKM/CipherTrust (External) Keys    | Get
cckm-misc          | PATCH  /v1/cckm/external-cm/keys/{id}                                         | CCKM/CipherTrust (External) Keys    | Update
cckm-misc          | POST   /v1/cckm/external-cm/keys/{id}/delete                                  | CCKM/CipherTrust (External) Keys    | Post
cckm-misc          | GET    /v1/cckm/external-cm/keys/{id}/versions                                | CCKM/CipherTrust (External) Keys    | List External CM Key Versions
cckm-misc          | POST   /v1/cckm/external-cm/keys/{id}/versions                                | CCKM/CipherTrust (External) Keys    | Post
cckm-misc          | GET    /v1/cckm/external-cm/refresh                                           | CCKM/CipherTrust (External) Keys    | Status
cckm-misc          | POST   /v1/cckm/external-cm/refresh                                           | CCKM/CipherTrust (External) Keys    | Refresh
cckm-misc          | GET    /v1/cckm/external-cm/refresh/{id}                                      | CCKM/CipherTrust (External) Keys    | Get
cckm-misc          | POST   /v1/cckm/external-cm/refresh/{id}/cancel                               | CCKM/CipherTrust (External) Keys    | Cancel
cckm-misc          | GET    /v1/cckm/settings/aws_key_expiry_notification                          | CCKM/Settings                       | List
cckm-misc          | PATCH  /v1/cckm/settings/aws_key_expiry_notification                          | CCKM/Settings                       | Update
cckm-misc          | GET    /v1/cckm/settings/azure_key_expiry_notification                        | CCKM/Settings                       | List
cckm-misc          | PATCH  /v1/cckm/settings/azure_key_expiry_notification                        | CCKM/Settings                       | Update
cckm-misc          | GET    /v1/cckm/settings/backups                                              | CCKM/Settings                       | List
cckm-misc          | PATCH  /v1/cckm/settings/backups                                              | CCKM/Settings                       | Update
cckm-oracle        | POST   /v1/cckm/oci/add-compartments                                          | CCKM/Oracle Compartments            | Add OCI compartments
cckm-oracle        | POST   /v1/cckm/oci/add-tenancy                                               | CCKM/Oracle Tenancies               | Add OCI tenancy
cckm-oracle        | POST   /v1/cckm/oci/add-vaults                                                | CCKM/Oracle Vaults                  | Add OCI vaults
cckm-oracle        | GET    /v1/cckm/oci/compartments                                              | CCKM/Oracle Compartments            | List
cckm-oracle        | DELETE /v1/cckm/oci/compartments/{id}                                         | CCKM/Oracle Compartments            | Delete
cckm-oracle        | GET    /v1/cckm/oci/compartments/{id}                                         | CCKM/Oracle Compartments            | Get
cckm-oracle        | POST   /v1/cckm/oci/create-external-key                                       | CCKM/Oracle External Vaults         | Create external keys in OCI external vault
cckm-oracle        | POST   /v1/cckm/oci/create-external-vault                                     | CCKM/Oracle External Vaults         | Create OCI External Vaults
cckm-oracle        | POST   /v1/cckm/oci/get-compartments                                          | CCKM/Oracle Compartments            | Get OCI compartments
cckm-oracle        | POST   /v1/cckm/oci/get-defined-tags                                          | CCKM/Oracle Compartments            | Get OCI defined tags
cckm-oracle        | POST   /v1/cckm/oci/get-subscribed-regions                                    | CCKM/Oracle Regions                 | Get OCI subscribed regions
cckm-oracle        | POST   /v1/cckm/oci/get-vaults                                                | CCKM/Oracle Vaults                  | Get OCI vaults
cckm-oracle        | GET    /v1/cckm/oci/issuers                                                   | CCKM/Oracle Issuers                 | List
cckm-oracle        | POST   /v1/cckm/oci/issuers                                                   | CCKM/Oracle Issuers                 | Create
cckm-oracle        | DELETE /v1/cckm/oci/issuers/{id}                                              | CCKM/Oracle Issuers                 | Delete
cckm-oracle        | GET    /v1/cckm/oci/issuers/{id}                                              | CCKM/Oracle Issuers                 | Get
cckm-oracle        | PATCH  /v1/cckm/oci/issuers/{id}                                              | CCKM/Oracle Issuers                 | Update
cckm-oracle        | GET    /v1/cckm/oci/keys                                                      | CCKM/Oracle Keys                    | List
cckm-oracle        | POST   /v1/cckm/oci/keys                                                      | CCKM/Oracle Keys                    | Create
cckm-oracle        | DELETE /v1/cckm/oci/keys/{id}                                                 | CCKM/Oracle Keys                    | Delete
cckm-oracle        | GET    /v1/cckm/oci/keys/{id}                                                 | CCKM/Oracle Keys                    | Get
cckm-oracle        | PATCH  /v1/cckm/oci/keys/{id}                                                 | CCKM/Oracle Keys                    | Update
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/block                                           | CCKM/Oracle External Vaults         | Block access to OCI external key
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/cancel-deletion                                 | CCKM/Oracle Keys                    | Cancel delete
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/change-compartment                              | CCKM/Oracle Keys                    | Change compartment
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/delete-backup                                   | CCKM/Oracle Keys                    | Delete backup of key from the CM
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/disable                                         | CCKM/Oracle Keys                    | Disable key
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/disable-auto-rotation                           | CCKM/Oracle Keys                    | Disable the auto rotation for OCI key
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/enable                                          | CCKM/Oracle Keys                    | Enable key
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/enable-auto-rotation                            | CCKM/Oracle Keys                    | Enable auto rotation for an OCI key
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/refresh                                         | CCKM/Oracle Keys                    | Refresh the key
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/restore                                         | CCKM/Oracle Keys                    | Restore deleted key
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/schedule-deletion                               | CCKM/Oracle Keys                    | Schedule deletion
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/unblock                                         | CCKM/Oracle External Vaults         | Unblock access to OCI external key
cckm-oracle        | GET    /v1/cckm/oci/keys/{id}/versions/{versionID}/                           | CCKM/Oracle Keys                    | Get key version details
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/versions/{versionID}/cancel-deletion            | CCKM/Oracle Keys                    | Cancel scheduled key version deletion
cckm-oracle        | POST   /v1/cckm/oci/keys/{id}/versions/{versionID}/schedule-deletion          | CCKM/Oracle Keys                    | Schedule key version for deletion
cckm-oracle        | GET    /v1/cckm/oci/keys/{keyID}/versions                                     | CCKM/Oracle Keys                    | List OCI key versions
cckm-oracle        | POST   /v1/cckm/oci/keys/{keyID}/versions                                     | CCKM/Oracle Keys                    | Add key version
cckm-oracle        | GET    /v1/cckm/oci/reports                                                   | CCKM/Oracle Reports                 | List reports
cckm-oracle        | POST   /v1/cckm/oci/reports                                                   | CCKM/Oracle Reports                 | Generate a report
cckm-oracle        | DELETE /v1/cckm/oci/reports/{id}                                              | CCKM/Oracle Reports                 | Delete
cckm-oracle        | GET    /v1/cckm/oci/reports/{id}                                              | CCKM/Oracle Reports                 | Get report
cckm-oracle        | GET    /v1/cckm/oci/reports/{id}/contents                                     | CCKM/Oracle Reports                 | Get contents
cckm-oracle        | GET    /v1/cckm/oci/reports/{id}/download                                     | CCKM/Oracle Reports                 | Get CSV contents
cckm-oracle        | POST   /v1/cckm/oci/storage/list-buckets                                      | CCKM/Oracle Storage                 | List Buckets
cckm-oracle        | GET    /v1/cckm/oci/synchronization-jobs                                      | CCKM/Oracle Keys                    | Status
cckm-oracle        | POST   /v1/cckm/oci/synchronization-jobs                                      | CCKM/Oracle Keys                    | Synchronize
cckm-oracle        | GET    /v1/cckm/oci/synchronization-jobs/{id}                                 | CCKM/Oracle Keys                    | Get
cckm-oracle        | POST   /v1/cckm/oci/synchronization-jobs/{id}/cancel                          | CCKM/Oracle Keys                    | Cancel
cckm-oracle        | GET    /v1/cckm/oci/tenancy                                                   | CCKM/Oracle Tenancies               | List
cckm-oracle        | DELETE /v1/cckm/oci/tenancy/{id}                                              | CCKM/Oracle Tenancies               | Delete
cckm-oracle        | GET    /v1/cckm/oci/tenancy/{id}                                              | CCKM/Oracle Tenancies               | Get
cckm-oracle        | POST   /v1/cckm/oci/upload-key                                                | CCKM/Oracle Keys                    | Upload
cckm-oracle        | GET    /v1/cckm/oci/vaults                                                    | CCKM/Oracle Vaults                  | List
cckm-oracle        | DELETE /v1/cckm/oci/vaults/{id}                                               | CCKM/Oracle Vaults                  | Delete
cckm-oracle        | GET    /v1/cckm/oci/vaults/{id}                                               | CCKM/Oracle Vaults                  | Get
cckm-oracle        | PATCH  /v1/cckm/oci/vaults/{id}                                               | CCKM/Oracle Vaults                  | Update
cckm-oracle        | POST   /v1/cckm/oci/vaults/{id}/block                                         | CCKM/Oracle External Vaults         | Blocks access to the OCI external vault
cckm-oracle        | POST   /v1/cckm/oci/vaults/{id}/unblock                                       | CCKM/Oracle External Vaults         | Unblocks access to the OCI external vault
cckm-oracle        | POST   /v1/cckm/oci/vaults/{id}/update-acls                                   | CCKM/Oracle Vaults                  | User ACLS
cckm-sap           | POST   /v1/cckm/sap/add-groups                                                | CCKM/SAP Data Custodian Groups      | Add SAP group
cckm-sap           | GET    /v1/cckm/sap/applications                                              | CCKM/SAP Data Custodian Applications | List SAP Applications
cckm-sap           | GET    /v1/cckm/sap/dkr                                                       | CCKM/SAP Data Custodian Keys        | List
cckm-sap           | POST   /v1/cckm/sap/dkr                                                       | CCKM/SAP Data Custodian Keys        | Create
cckm-sap           | DELETE /v1/cckm/sap/dkr/{id}                                                  | CCKM/SAP Data Custodian Keys        | Delete
cckm-sap           | GET    /v1/cckm/sap/dkr/{id}                                                  | CCKM/SAP Data Custodian Keys        | Get
cckm-sap           | PATCH  /v1/cckm/sap/dkr/{id}                                                  | CCKM/SAP Data Custodian Keys        | Update
cckm-sap           | POST   /v1/cckm/sap/dkr/{id}/delete                                           | CCKM/SAP Data Custodian Keys        | Deletes a Dynamic Key Reference from SAP.
cckm-sap           | GET    /v1/cckm/sap/ekm/keys                                                  | CCKM/SAP Data Custodian HYOK        | List
cckm-sap           | POST   /v1/cckm/sap/ekm/keys                                                  | CCKM/SAP Data Custodian HYOK        | Create external keys in SAP KeyStores.
cckm-sap           | DELETE /v1/cckm/sap/ekm/keys/{id}                                             | CCKM/SAP Data Custodian HYOK        | Delete
cckm-sap           | GET    /v1/cckm/sap/ekm/keys/{id}                                             | CCKM/SAP Data Custodian HYOK        | Get
cckm-sap           | PATCH  /v1/cckm/sap/ekm/keys/{id}                                             | CCKM/SAP Data Custodian HYOK        | Update
cckm-sap           | POST   /v1/cckm/sap/ekm/keys/{id}/archive                                     | CCKM/SAP Data Custodian HYOK        | Archive key
cckm-sap           | POST   /v1/cckm/sap/ekm/keys/{id}/block                                       | CCKM/SAP Data Custodian HYOK        | Blocks access to the SAP external key.
cckm-sap           | POST   /v1/cckm/sap/ekm/keys/{id}/disable                                     | CCKM/SAP Data Custodian HYOK        | Disable key
cckm-sap           | POST   /v1/cckm/sap/ekm/keys/{id}/disable-auto-rotation                       | CCKM/SAP Data Custodian HYOK        | Disable key rotation
cckm-sap           | POST   /v1/cckm/sap/ekm/keys/{id}/enable                                      | CCKM/SAP Data Custodian HYOK        | Enable key
cckm-sap           | POST   /v1/cckm/sap/ekm/keys/{id}/enable-auto-rotation                        | CCKM/SAP Data Custodian HYOK        | Enable key rotation
cckm-sap           | POST   /v1/cckm/sap/ekm/keys/{id}/recover                                     | CCKM/SAP Data Custodian HYOK        | Recovers key
cckm-sap           | POST   /v1/cckm/sap/ekm/keys/{id}/unblock                                     | CCKM/SAP Data Custodian HYOK        | Unblocks access to the SAP external key.
cckm-sap           | GET    /v1/cckm/sap/ekm/keys/{id}/versions                                    | CCKM/SAP Data Custodian HYOK        | List
cckm-sap           | POST   /v1/cckm/sap/ekm/keys/{id}/versions                                    | CCKM/SAP Data Custodian HYOK        | Add key version
cckm-sap           | GET    /v1/cckm/sap/ekm/keys/{id}/versions/{versionID}                        | CCKM/SAP Data Custodian HYOK        | Get key version details.
cckm-sap           | GET    /v1/cckm/sap/ekm/keystores                                             | CCKM/SAP Data Custodian HYOK        | List KeyStores
cckm-sap           | POST   /v1/cckm/sap/ekm/keystores                                             | CCKM/SAP Data Custodian HYOK        | Create SAP Keystore
cckm-sap           | DELETE /v1/cckm/sap/ekm/keystores/{id}                                        | CCKM/SAP Data Custodian HYOK        | Delete
cckm-sap           | GET    /v1/cckm/sap/ekm/keystores/{id}                                        | CCKM/SAP Data Custodian HYOK        | Get
cckm-sap           | PATCH  /v1/cckm/sap/ekm/keystores/{id}                                        | CCKM/SAP Data Custodian HYOK        | Update
cckm-sap           | POST   /v1/cckm/sap/ekm/keystores/{id}/archive                                | CCKM/SAP Data Custodian HYOK        | Archives SAP external keystore
cckm-sap           | POST   /v1/cckm/sap/ekm/keystores/{id}/block                                  | CCKM/SAP Data Custodian HYOK        | Blocks access to the SAP external keystore
cckm-sap           | POST   /v1/cckm/sap/ekm/keystores/{id}/recover                                | CCKM/SAP Data Custodian HYOK        | Recovers SAP external keystore
cckm-sap           | POST   /v1/cckm/sap/ekm/keystores/{id}/unblock                                | CCKM/SAP Data Custodian HYOK        | Unblocks access to the SAP external keystore
cckm-sap           | POST   /v1/cckm/sap/ekm/keystores/{id}/update-acls                            | CCKM/SAP Data Custodian HYOK        | User ACLS
cckm-sap           | POST   /v1/cckm/sap/get-groups                                                | CCKM/SAP Data Custodian Groups      | Get SAP groups
cckm-sap           | POST   /v1/cckm/sap/get-service-connectability                                | CCKM/SAP Data Custodian Groups      | Get Service Connectability
cckm-sap           | GET    /v1/cckm/sap/groups                                                    | CCKM/SAP Data Custodian Groups      | List Groups
cckm-sap           | DELETE /v1/cckm/sap/groups/{id}                                               | CCKM/SAP Data Custodian Groups      | Delete
cckm-sap           | GET    /v1/cckm/sap/groups/{id}                                               | CCKM/SAP Data Custodian Groups      | Get
cckm-sap           | PATCH  /v1/cckm/sap/groups/{id}                                               | CCKM/SAP Data Custodian Groups      | Update
cckm-sap           | POST   /v1/cckm/sap/groups/{id}/update-acls                                   | CCKM/SAP Data Custodian Groups      | User ACLS
cckm-sap           | GET    /v1/cckm/sap/keys                                                      | CCKM/SAP Data Custodian Keys        | List
cckm-sap           | POST   /v1/cckm/sap/keys                                                      | CCKM/SAP Data Custodian Keys        | Create
cckm-sap           | POST   /v1/cckm/sap/keys/jobs                                                 | CCKM/SAP Data Custodian Keys        | Creates a new job
cckm-sap           | GET    /v1/cckm/sap/keys/jobs/{id}                                            | CCKM/SAP Data Custodian Keys        | Retrieves job status
cckm-sap           | DELETE /v1/cckm/sap/keys/{id}                                                 | CCKM/SAP Data Custodian Keys        | Delete
cckm-sap           | GET    /v1/cckm/sap/keys/{id}                                                 | CCKM/SAP Data Custodian Keys        | Get
cckm-sap           | PATCH  /v1/cckm/sap/keys/{id}                                                 | CCKM/SAP Data Custodian Keys        | Update
cckm-sap           | POST   /v1/cckm/sap/keys/{id}/delete                                          | CCKM/SAP Data Custodian Keys        | Delete key from SAP
cckm-sap           | POST   /v1/cckm/sap/keys/{id}/delete-backup                                   | CCKM/SAP Data Custodian Keys        | Delete backup of key from CM
cckm-sap           | POST   /v1/cckm/sap/keys/{id}/disable-auto-rotation                           | CCKM/SAP Data Custodian Keys        | Disable the auto rotation for SAP key
cckm-sap           | POST   /v1/cckm/sap/keys/{id}/enable-auto-rotation                            | CCKM/SAP Data Custodian Keys        | Enables auto rotation
cckm-sap           | GET    /v1/cckm/sap/keys/{id}/versions                                        | CCKM/SAP Data Custodian Keys        | List
cckm-sap           | POST   /v1/cckm/sap/keys/{id}/versions                                        | CCKM/SAP Data Custodian Keys        | Add Key version
cckm-sap           | GET    /v1/cckm/sap/keys/{id}/versions/{versionID}                            | CCKM/SAP Data Custodian Keys        | Get key version details.
cckm-sap           | PATCH  /v1/cckm/sap/keys/{id}/versions/{versionID}                            | CCKM/SAP Data Custodian Keys        | Update
cckm-sap           | GET    /v1/cckm/sap/reports                                                   | CCKM/SAP Data Custodian Reports     | List Reports
cckm-sap           | POST   /v1/cckm/sap/reports                                                   | CCKM/SAP Data Custodian Reports     | Generate a report
cckm-sap           | DELETE /v1/cckm/sap/reports/{id}                                              | CCKM/SAP Data Custodian Reports     | Delete
cckm-sap           | GET    /v1/cckm/sap/reports/{id}                                              | CCKM/SAP Data Custodian Reports     | Get Report
cckm-sap           | GET    /v1/cckm/sap/reports/{id}/contents                                     | CCKM/SAP Data Custodian Reports     | Get Contents
cckm-sap           | GET    /v1/cckm/sap/reports/{id}/download                                     | CCKM/SAP Data Custodian Reports     | Get CSV Contents
cckm-sap           | GET    /v1/cckm/sap/synchronization-jobs                                      | CCKM/SAP Data Custodian Keys        | Status
cckm-sap           | POST   /v1/cckm/sap/synchronization-jobs                                      | CCKM/SAP Data Custodian Keys        | Synchronize
cckm-sap           | GET    /v1/cckm/sap/synchronization-jobs/{id}                                 | CCKM/SAP Data Custodian Keys        | Get
cckm-sap           | POST   /v1/cckm/sap/synchronization-jobs/{id}/cancel                          | CCKM/SAP Data Custodian Keys        | Cancel
cckm-sap           | POST   /v1/cckm/sap/upload-key                                                | CCKM/SAP Data Custodian Keys        | Upload
cckm-sfdc          | POST   /v1/cckm/sfdc/add-organizations                                        | CCKM/SFDC Cloud Organizations       | Add SFDC organization
cckm-sfdc          | GET    /v1/cckm/sfdc/certificates                                             | CCKM/SFDC Cloud Certificates        | List
cckm-sfdc          | POST   /v1/cckm/sfdc/certificates                                             | CCKM/SFDC Cloud Certificates        | Create
cckm-sfdc          | GET    /v1/cckm/sfdc/certificates/synchronization-jobs                        | CCKM/SFDC Cloud Certificates        | Status
cckm-sfdc          | POST   /v1/cckm/sfdc/certificates/synchronization-jobs                        | CCKM/SFDC Cloud Certificates        | Synchronize
cckm-sfdc          | GET    /v1/cckm/sfdc/certificates/synchronization-jobs/{id}                   | CCKM/SFDC Cloud Certificates        | Get
cckm-sfdc          | POST   /v1/cckm/sfdc/certificates/synchronization-jobs/{id}/cancel            | CCKM/SFDC Cloud Certificates        | Cancel
cckm-sfdc          | DELETE /v1/cckm/sfdc/certificates/{id}                                        | CCKM/SFDC Cloud Certificates        | Delete
cckm-sfdc          | GET    /v1/cckm/sfdc/certificates/{id}                                        | CCKM/SFDC Cloud Certificates        | Get
cckm-sfdc          | GET    /v1/cckm/sfdc/endpoints                                                | CCKM/SFDC Cache Only Key Endpoints  | List
cckm-sfdc          | POST   /v1/cckm/sfdc/endpoints                                                | CCKM/SFDC Cache Only Key Endpoints  | Create
cckm-sfdc          | GET    /v1/cckm/sfdc/endpoints/{endpoint_id}/keys/{id}                        | CCKM/SFDC Tenant Secret             | Get
cckm-sfdc          | DELETE /v1/cckm/sfdc/endpoints/{id}                                           | CCKM/SFDC Cache Only Key Endpoints  | Delete
cckm-sfdc          | GET    /v1/cckm/sfdc/endpoints/{id}                                           | CCKM/SFDC Cache Only Key Endpoints  | Get
cckm-sfdc          | PATCH  /v1/cckm/sfdc/endpoints/{id}                                           | CCKM/SFDC Cache Only Key Endpoints  | Update
cckm-sfdc          | POST   /v1/cckm/sfdc/get-named-credentials                                    | CCKM/SFDC Cloud Named Credentials   | List
cckm-sfdc          | POST   /v1/cckm/sfdc/get-organizations                                        | CCKM/SFDC Cloud Organizations       | Get SFDC organizations
cckm-sfdc          | GET    /v1/cckm/sfdc/issuers                                                  | CCKM/Salesforce Issuers             | List
cckm-sfdc          | POST   /v1/cckm/sfdc/issuers                                                  | CCKM/Salesforce Issuers             | Create
cckm-sfdc          | DELETE /v1/cckm/sfdc/issuers/{id}                                             | CCKM/Salesforce Issuers             | Delete
cckm-sfdc          | GET    /v1/cckm/sfdc/issuers/{id}                                             | CCKM/Salesforce Issuers             | Get
cckm-sfdc          | PATCH  /v1/cckm/sfdc/issuers/{id}                                             | CCKM/Salesforce Issuers             | Update
cckm-sfdc          | GET    /v1/cckm/sfdc/keys                                                     | CCKM/SFDC Tenant Secret             | List
cckm-sfdc          | POST   /v1/cckm/sfdc/keys                                                     | CCKM/SFDC Tenant Secret             | Create
cckm-sfdc          | GET    /v1/cckm/sfdc/keys/synchronization-jobs                                | CCKM/SFDC Tenant Secret             | Status
cckm-sfdc          | POST   /v1/cckm/sfdc/keys/synchronization-jobs                                | CCKM/SFDC Tenant Secret             | Synchronize
cckm-sfdc          | GET    /v1/cckm/sfdc/keys/synchronization-jobs/{id}                           | CCKM/SFDC Tenant Secret             | Get
cckm-sfdc          | POST   /v1/cckm/sfdc/keys/synchronization-jobs/{id}/cancel                    | CCKM/SFDC Tenant Secret             | Cancel
cckm-sfdc          | POST   /v1/cckm/sfdc/keys/upload                                              | CCKM/SFDC Tenant Secret             | Upload
cckm-sfdc          | GET    /v1/cckm/sfdc/keys/{id}                                                | CCKM/SFDC Tenant Secret             | Get
cckm-sfdc          | PATCH  /v1/cckm/sfdc/keys/{id}                                                | CCKM/SFDC Tenant Secret             | Update
cckm-sfdc          | POST   /v1/cckm/sfdc/keys/{id}/activate                                       | CCKM/SFDC Tenant Secret             | Activate Cache-only key
cckm-sfdc          | POST   /v1/cckm/sfdc/keys/{id}/delete-backup                                  | CCKM/SFDC Tenant Secret             | Delete Backup
cckm-sfdc          | POST   /v1/cckm/sfdc/keys/{id}/destroy                                        | CCKM/SFDC Tenant Secret             | Destroy a SFDC key.
cckm-sfdc          | POST   /v1/cckm/sfdc/keys/{id}/import                                         | CCKM/SFDC Tenant Secret             | Import
cckm-sfdc          | GET    /v1/cckm/sfdc/organizations                                            | CCKM/SFDC Cloud Organizations       | List Organizations
cckm-sfdc          | DELETE /v1/cckm/sfdc/organizations/{id}                                       | CCKM/SFDC Cloud Organizations       | Delete
cckm-sfdc          | GET    /v1/cckm/sfdc/organizations/{id}                                       | CCKM/SFDC Cloud Organizations       | Get
cckm-sfdc          | PATCH  /v1/cckm/sfdc/organizations/{id}                                       | CCKM/SFDC Cloud Organizations       | Update
cckm-sfdc          | POST   /v1/cckm/sfdc/organizations/{id}/update-acls                           | CCKM/SFDC Cloud Organizations       | User ACLS
cckm-sfdc          | GET    /v1/cckm/sfdc/reports                                                  | CCKM/SFDC Cloud Reports             | List Reports
cckm-sfdc          | POST   /v1/cckm/sfdc/reports                                                  | CCKM/SFDC Cloud Reports             | Generate a report
cckm-sfdc          | DELETE /v1/cckm/sfdc/reports/{id}                                             | CCKM/SFDC Cloud Reports             | Delete
cckm-sfdc          | GET    /v1/cckm/sfdc/reports/{id}                                             | CCKM/SFDC Cloud Reports             | Get Report
cckm-sfdc          | GET    /v1/cckm/sfdc/reports/{id}/contents                                    | CCKM/SFDC Cloud Reports             | Get Contents
cckm-sfdc          | GET    /v1/cckm/sfdc/reports/{id}/download                                    | CCKM/SFDC Cloud Reports             | Get CSV Contents
cckm-sfdc          | POST   /v1/cckm/sfdc/upload-cache-only-key                                    | CCKM/SFDC Tenant Secret             | Upload SFDC Cache-only Key.
cm-admin           | POST   /v1/ca/csr                                                             | Certificate Authority               | CSR
cm-admin           | GET    /v1/ca/external-cas                                                    | Certificate Authority               | List external CAs
cm-admin           | POST   /v1/ca/external-cas                                                    | Certificate Authority               | Upload external CA
cm-admin           | DELETE /v1/ca/external-cas/{id}                                               | Certificate Authority               | Delete external CA
cm-admin           | GET    /v1/ca/external-cas/{id}                                               | Certificate Authority               | Get external CA
cm-admin           | PATCH  /v1/ca/external-cas/{id}                                               | Certificate Authority               | Update External CA
cm-admin           | GET    /v1/ca/local-cas                                                       | Certificate Authority               | List local CAs
cm-admin           | POST   /v1/ca/local-cas                                                       | Certificate Authority               | Create local CA
cm-admin           | GET    /v1/ca/local-cas/{caid}/certs                                          | Certificate Authority               | List certificates
cm-admin           | POST   /v1/ca/local-cas/{caid}/certs                                          | Certificate Authority               | Issue certificate
cm-admin           | DELETE /v1/ca/local-cas/{caid}/certs/{id}                                     | Certificate Authority               | Delete certificate
cm-admin           | GET    /v1/ca/local-cas/{caid}/certs/{id}                                     | Certificate Authority               | Get certificate
cm-admin           | POST   /v1/ca/local-cas/{caid}/certs/{id}/resume                              | Certificate Authority               | Resume certificate
cm-admin           | POST   /v1/ca/local-cas/{caid}/certs/{id}/revoke                              | Certificate Authority               | Revoke certificate
cm-admin           | DELETE /v1/ca/local-cas/{id}                                                  | Certificate Authority               | Delete local CA
cm-admin           | GET    /v1/ca/local-cas/{id}                                                  | Certificate Authority               | Get local CA
cm-admin           | PATCH  /v1/ca/local-cas/{id}                                                  | Certificate Authority               | Update local CA
cm-admin           | POST   /v1/ca/local-cas/{id}/install                                          | Certificate Authority               | Install a local CA
cm-admin           | POST   /v1/ca/local-cas/{id}/self-sign                                        | Certificate Authority               | Self-sign a local CA
cm-admin           | POST   /v1/quorum-mgmt/policy/activate                                        | Quorum                              | Activate
cm-admin           | POST   /v1/quorum-mgmt/policy/deactivate                                      | Quorum                              | Deactivate
cm-admin           | GET    /v1/quorum-mgmt/policy/status                                          | Quorum                              | Status
cm-admin           | GET    /v1/quorum-mgmt/profiles                                               | Quorum                              | Return quorum profiles.
cm-admin           | GET    /v1/quorum-mgmt/profiles/{id}                                          | Quorum                              | Return the quorum profile.
cm-admin           | PATCH  /v1/quorum-mgmt/profiles/{id}                                          | Quorum                              | Update the quorum profile associated with the identifier.
cm-admin           | GET    /v1/quorum-mgmt/quorums                                                | Quorum                              | List
cm-admin           | DELETE /v1/quorum-mgmt/quorums/{id}                                           | Quorum                              | Delete a quorum.
cm-admin           | GET    /v1/quorum-mgmt/quorums/{id}                                           | Quorum                              | Fetch a quorum.
cm-admin           | POST   /v1/quorum-mgmt/quorums/{id}/activate                                  | Quorum                              | Activate a quorum.
cm-admin           | POST   /v1/quorum-mgmt/quorums/{id}/approve                                   | Quorum                              | Approve a quorum.
cm-admin           | POST   /v1/quorum-mgmt/quorums/{id}/deny                                      | Quorum                              | Deny a quorum.
cm-admin           | GET    /v1/quorum-mgmt/quorums/{id}/resources                                 | Quorum                              | List resources of the quorum.
cm-admin           | POST   /v1/quorum-mgmt/quorums/{id}/revoke                                    | Quorum                              | Revoke the vote cast for the quorum.
cm-admin           | GET    /v1/snmp/communities                                                   | SNMP                                | List
cm-admin           | POST   /v1/snmp/communities                                                   | SNMP                                | Add
cm-admin           | DELETE /v1/snmp/communities/{id}                                              | SNMP                                | Delete
cm-admin           | GET    /v1/snmp/communities/{id}                                              | SNMP                                | Get
cm-admin           | PATCH  /v1/snmp/communities/{id}                                              | SNMP                                | Update
cm-admin           | GET    /v1/snmp/info                                                          | SNMP                                | Get
cm-admin           | GET    /v1/snmp/management-stations                                           | SNMP                                | List
cm-admin           | POST   /v1/snmp/management-stations                                           | SNMP                                | Add
cm-admin           | DELETE /v1/snmp/management-stations/{id}                                      | SNMP                                | Delete
cm-admin           | GET    /v1/snmp/management-stations/{id}                                      | SNMP                                | Get
cm-admin           | PATCH  /v1/snmp/management-stations/{id}                                      | SNMP                                | Update Management Station
cm-admin           | GET    /v1/snmp/users                                                         | SNMP                                | List
cm-admin           | POST   /v1/snmp/users                                                         | SNMP                                | Add
cm-admin           | DELETE /v1/snmp/users/{id}                                                    | SNMP                                | Delete
cm-admin           | GET    /v1/snmp/users/{id}                                                    | SNMP                                | Get
cm-admin           | PATCH  /v1/snmp/users/{id}                                                    | SNMP                                | Update
cm-keys            | POST   /v1/vault/csr                                                          | Certificate Authority               | CSR
cm-keys            | GET    /v1/vault/key-labels/                                                  | Keys                                | List key labels
cm-keys            | GET    /v1/vault/key-policies/                                                | Key Policies                        | List key policies
cm-keys            | POST   /v1/vault/key-policies/                                                | Key Policies                        | Create a key policy
cm-keys            | DELETE /v1/vault/key-policies/{id}                                            | Key Policies                        | Delete
cm-keys            | GET    /v1/vault/key-policies/{id}                                            | (none)                              | Get key policy
cm-keys            | PATCH  /v1/vault/key-policies/{id}                                            | (none)                              | Update
cm-keys            | POST   /v1/vault/keys-bulk-export                                             | Keys                                | Bulk export keys
cm-keys            | GET    /v1/vault/keys2/                                                       | Keys                                | List
cm-keys            | POST   /v1/vault/keys2/                                                       | Keys                                | Create
cm-keys            | DELETE /v1/vault/keys2/{id}                                                   | Keys                                | Delete
cm-keys            | GET    /v1/vault/keys2/{id}                                                   | Keys                                | Get
cm-keys            | PATCH  /v1/vault/keys2/{id}                                                   | Keys                                | Update
cm-keys            | POST   /v1/vault/keys2/{id}/archive                                           | Keys                                | Archive
cm-keys            | POST   /v1/vault/keys2/{id}/attributes                                        | Keys                                | Generates or Returns the value of attribute.
cm-keys            | POST   /v1/vault/keys2/{id}/clone                                             | Keys                                | Clone
cm-keys            | POST   /v1/vault/keys2/{id}/destroy                                           | Keys                                | Destroy
cm-keys            | POST   /v1/vault/keys2/{id}/export                                            | Keys                                | Export
cm-keys            | POST   /v1/vault/keys2/{id}/generate-kcv                                      | Keys                                | Generate KCV
cm-keys            | POST   /v1/vault/keys2/{id}/reactivate                                        | Keys                                | Reactivate
cm-keys            | POST   /v1/vault/keys2/{id}/recover                                           | Keys                                | Recover
cm-keys            | POST   /v1/vault/keys2/{id}/revoke                                            | Keys                                | Revoke
cm-keys            | GET    /v1/vault/keys2/{id}/versions/                                         | Keys                                | List versions
cm-keys            | POST   /v1/vault/keys2/{id}/versions/                                         | Keys                                | Create version
cm-keys            | GET    /v1/vault/links/                                                       | Links                               | List
cm-keys            | POST   /v1/vault/links/                                                       | Links                               | Create
cm-keys            | DELETE /v1/vault/links/{id}                                                   | Links                               | Delete
cm-keys            | GET    /v1/vault/links/{id}                                                   | Links                               | Get
cm-keys            | PATCH  /v1/vault/links/{id}                                                   | Links                               | Update
cm-keys            | POST   /v1/vault/query-keys/                                                  | Keys                                | Query
cm-keys            | GET    /v1/vault/secrets                                                      | Secrets                             | List
cm-keys            | POST   /v1/vault/secrets                                                      | Secrets                             | Create
cm-keys            | DELETE /v1/vault/secrets/{id}                                                 | Secrets                             | Delete
cm-keys            | GET    /v1/vault/secrets/{id}                                                 | Secrets                             | Get
cm-keys            | PATCH  /v1/vault/secrets/{id}                                                 | Secrets                             | Update
cm-keys            | POST   /v1/vault/secrets/{id}/destroy                                         | Secrets                             | Destroy
cm-keys            | POST   /v1/vault/secrets/{id}/export                                          | Secrets                             | Export
cm-keys            | GET    /v1/vault/secrets/{id}/versions/                                       | Secrets                             | List versions
cm-keys            | POST   /v1/vault/secrets/{id}/versions/                                       | Secrets                             | Create version
cm-keys            | GET    /v1/vault/templates                                                    | Templates                           | List
cm-keys            | POST   /v1/vault/templates                                                    | Templates                           | Create
cm-keys            | DELETE /v1/vault/templates/{id}                                               | Templates                           | Delete
cm-keys            | GET    /v1/vault/templates/{id}                                               | Templates                           | Get
cm-keys            | PATCH  /v1/vault/templates/{id}                                               | Templates                           | Update
cm-logs            | GET    /v1/audit/alarm-configs                                                | Records                             | List
cm-logs            | POST   /v1/audit/alarm-configs                                                | Records                             | Create
cm-logs            | DELETE /v1/audit/alarm-configs/{id}                                           | Records                             | Delete
cm-logs            | GET    /v1/audit/alarm-configs/{id}                                           | Records                             | Get
cm-logs            | PATCH  /v1/audit/alarm-configs/{id}                                           | Records                             | Update
cm-logs            | GET    /v1/audit/client-records                                               | Records                             | List
cm-logs            | GET    /v1/audit/client-records/{id}                                          | Records                             | Get
cm-logs            | GET    /v1/audit/loki/api/v1/query_range                                      | Records                             | List
cm-logs            | GET    /v1/audit/records                                                      | Records                             | List
cm-logs            | GET    /v1/audit/records/{id}                                                 | Records                             | Get
cm-logs            | GET    /v1/logs/download/                                                     | Logs                                | Logs Download
cm-logs            | GET    /v1/logs/download/all-logs                                             | Logs                                | Download All Logs
cm-logs            | GET    /v1/logs/download/debug-logs                                           | Logs                                | Download Debug Logs
cm-logs            | GET    /v1/logs/download/kmip-activity-logs                                   | Logs                                | Download KMIP Activity Logs
cm-logs            | GET    /v1/logs/download/nae-activity-logs                                    | Logs                                | Download NAE Activity Logs
cm-logs            | GET    /v1/logs/download/web-activity-logs                                    | Logs                                | Download Web Activity Logs
cm-logs            | GET    /v1/logs/level/                                                        | Logs                                | Get Log Level
cm-logs            | POST   /v1/logs/level/                                                        | Logs                                | Set Log Level
cm-misc            | GET    /v1/admin/policies/                                                    | Policies                            | List
cm-misc            | POST   /v1/admin/policies/                                                    | Policies                            | Create
cm-misc            | DELETE /v1/admin/policies/{id}                                                | Policies                            | Delete
cm-misc            | GET    /v1/admin/policies/{id}                                                | Policies                            | Get
cm-misc            | GET    /v1/admin/policy-attachments/                                          | Policy Attachments                  | List
cm-misc            | POST   /v1/admin/policy-attachments/                                          | Policy Attachments                  | Attach
cm-misc            | DELETE /v1/admin/policy-attachments/{id}                                      | Policy Attachments                  | Detach
cm-misc            | GET    /v1/admin/policy-attachments/{id}                                      | Policy Attachments                  | Get
cm-misc            | GET    /v1/backupStatus                                                       | Backups/Backup-Restore              | Status
cm-misc            | GET    /v1/backupkeys                                                         | Backup Keys                         | List
cm-misc            | POST   /v1/backupkeys                                                         | Backup Keys                         | Create
cm-misc            | POST   /v1/backupkeys/upload                                                  | Backup Keys                         | Upload
cm-misc            | DELETE /v1/backupkeys/{id}                                                    | Backup Keys                         | Delete
cm-misc            | GET    /v1/backupkeys/{id}                                                    | Backup Keys                         | Get
cm-misc            | POST   /v1/backupkeys/{id}/default                                            | Backup Keys                         | Default
cm-misc            | POST   /v1/backupkeys/{id}/download                                           | Backup Keys                         | Download
cm-misc            | GET    /v1/client-management/clients/                                         | Client-Management/Clients           | List
cm-misc            | POST   /v1/client-management/clients/                                         | Client-Management/Clients           | Register
cm-misc            | DELETE /v1/client-management/clients/{id}                                     | Client-Management/Clients           | Delete
cm-misc            | GET    /v1/client-management/clients/{id}                                     | Client-Management/Clients           | Get
cm-misc            | POST   /v1/client-management/clients/{id}/renew                               | Client-Management/Clients           | Renew
cm-misc            | PATCH  /v1/client-management/clients/{id}/revoke                              | Client-Management/Clients           | Revoke
cm-misc            | POST   /v1/client-management/confidential-computing/policies                  | Client-Management/Confidential-Computing | List
cm-misc            | POST   /v1/client-management/confidential-computing/{id}/attest               | Client-Management/Confidential-Computing | Attest
cm-misc            | GET    /v1/client-management/confidential-computing/{id}/nonce                | Client-Management/Confidential-Computing | Get
cm-misc            | GET    /v1/client-management/profiles                                         | Client-Management/Profiles          | List
cm-misc            | POST   /v1/client-management/profiles                                         | Client-Management/Profiles          | Create
cm-misc            | DELETE /v1/client-management/profiles/{id}                                    | Client-Management/Profiles          | Delete
cm-misc            | GET    /v1/client-management/profiles/{id}                                    | Client-Management/Profiles          | Get
cm-misc            | PATCH  /v1/client-management/profiles/{id}                                    | Client-Management/Profiles          | Update
cm-misc            | GET    /v1/client-management/regtokens/                                       | Client-Management/Tokens            | List
cm-misc            | POST   /v1/client-management/regtokens/                                       | Client-Management/Tokens            | Create
cm-misc            | DELETE /v1/client-management/regtokens/{id}                                   | Client-Management/Tokens            | Delete
cm-misc            | GET    /v1/client-management/regtokens/{id}                                   | Client-Management/Tokens            | Get
cm-misc            | PATCH  /v1/client-management/regtokens/{id}                                   | Client-Management/Tokens            | Update
cm-misc            | POST   /v1/client-management/self/client/renew                                | Client-Management/Clients           | Renew
cm-misc            | GET    /v1/client-management/webcert-fingerprint/                             | Client-Management/Tokens            | Web Certificate Fingerprint
cm-misc            | GET    /v1/dns-hosts                                                          | DNS Hosts                           | List
cm-misc            | POST   /v1/dns-hosts                                                          | DNS Hosts                           | Create
cm-misc            | DELETE /v1/dns-hosts/{name}                                                   | DNS Hosts                           | Delete
cm-misc            | GET    /v1/dns-hosts/{name}                                                   | DNS Hosts                           | Get
cm-misc            | PATCH  /v1/dns-hosts/{name}                                                   | DNS Hosts                           | Update
cm-misc            | GET    /v1/kmip/kmip-clients                                                  | KMIP/Client-Management              | List
cm-misc            | POST   /v1/kmip/kmip-clients                                                  | KMIP/Client-Management              | Register KMIP client
cm-misc            | GET    /v1/kmip/kmip-clients-count                                            | KMIP/Client-Management              | Get clients count
cm-misc            | DELETE /v1/kmip/kmip-clients/{id}                                             | KMIP/Client-Management              | Delete
cm-misc            | GET    /v1/kmip/kmip-profiles                                                 | KMIP/Client-Management              | List
cm-misc            | POST   /v1/kmip/kmip-profiles                                                 | KMIP/Client-Management              | Create
cm-misc            | DELETE /v1/kmip/kmip-profiles/{name}                                          | KMIP/Client-Management              | Delete
cm-misc            | GET    /v1/kmip/kmip-profiles/{name}                                          | KMIP/Client-Management              | Get
cm-misc            | POST   /v1/kmip/regtokens/                                                    | KMIP/Client-Management              | Create
cm-misc            | POST   /v1/locker/diskenc/setup                                               | Disk Encryption                     | Encrypt
cm-misc            | GET    /v1/locker/diskenc/status                                              | Disk Encryption                     | Status
cm-misc            | GET    /v1/migration-split-keys                                               | Migration Split Keys                | List
cm-misc            | POST   /v1/migration-split-keys                                               | Migration Split Keys                | Create
cm-misc            | DELETE /v1/migration-split-keys/{name}                                        | Migration Split Keys                | Delete
cm-misc            | GET    /v1/migration-split-keys/{name}                                        | Migration Split Keys                | Get
cm-misc            | POST   /v1/migration-split-keys/{name}/shares                                 | Migration Split Keys                | Add a share
cm-misc            | DELETE /v1/migration-split-keys/{name}/shares/{share_name}                    | Migration Split Keys                | Delete a share
cm-misc            | PATCH  /v1/migration-split-keys/{name}/shares/{share_name}                    | Migration Split Keys                | Modify a share
cm-misc            | GET    /v1/nodes                                                              | Cluster Nodes                       | List
cm-misc            | POST   /v1/nodes                                                              | Cluster Nodes                       | Sign Cert
cm-misc            | DELETE /v1/nodes/{id}                                                         | Cluster Nodes                       | Delete
cm-misc            | GET    /v1/nodes/{id}                                                         | Cluster Nodes                       | Get
cm-misc            | PATCH  /v1/nodes/{id}                                                         | Cluster Nodes                       | Update
cm-misc            | POST   /v1/nodes/{id}/delete                                                  | Cluster Nodes                       | Delete
cm-misc            | GET    /v1/notification/email-addresses                                       | Notifications                       | List
cm-misc            | POST   /v1/notification/email-addresses                                       | Notifications                       | Add
cm-misc            | DELETE /v1/notification/email-addresses/{id}                                  | Notifications                       | Delete
cm-misc            | GET    /v1/notification/email-addresses/{id}                                  | Notifications                       | Get
cm-misc            | GET    /v1/notification/smtp-servers                                          | SMTP Servers                        | List
cm-misc            | POST   /v1/notification/smtp-servers                                          | SMTP Servers                        | Add
cm-misc            | DELETE /v1/notification/smtp-servers/{id}                                     | SMTP Servers                        | Delete
cm-misc            | POST   /v1/notification/smtp-test-mail                                        | SMTP Servers                        | Test
cm-misc            | GET    /v1/protectdb/databases                                                | CDP/Database                        | List
cm-misc            | POST   /v1/protectdb/databases                                                | CDP/Database                        | Add
cm-misc            | POST   /v1/protectdb/databases/cert                                           | CDP/Database                        | Upload
cm-misc            | GET    /v1/protectdb/databases/request/{id}                                   | CDP/Database                        | GetRequest
cm-misc            | DELETE /v1/protectdb/databases/{id}                                           | CDP/Database                        | Delete
cm-misc            | GET    /v1/protectdb/databases/{id}                                           | CDP/Database                        | Get
cm-misc            | PATCH  /v1/protectdb/databases/{id}                                           | CDP/Database                        | Update
cm-misc            | POST   /v1/protectdb/databases/{id}/auth                                      | CDP/Database                        | AuthorizeUser
cm-misc            | GET    /v1/protectdb/databases/{id}/column                                    | CDP/Database                        | Get Column
cm-misc            | GET    /v1/protectdb/databases/{id}/columns                                   | CDP/Database                        | List Columns
cm-misc            | PATCH  /v1/protectdb/databases/{id}/columns                                   | CDP/Database                        | Update Column
cm-misc            | GET    /v1/protectdb/databases/{id}/dbusers                                   | CDP/UserMapping                     | ListDBUsers
cm-misc            | POST   /v1/protectdb/databases/{id}/decrypt                                   | CDP/Migration Server                | Decrypt table
cm-misc            | DELETE /v1/protectdb/databases/{id}/deleteData                                | CDP/Database                        | DeleteOldData
cm-misc            | DELETE /v1/protectdb/databases/{id}/domainIndex                               | CDP/Database                        | DeleteDomainIndex
cm-misc            | POST   /v1/protectdb/databases/{id}/domainIndex                               | CDP/Database                        | CreateDomainIndex
cm-misc            | POST   /v1/protectdb/databases/{id}/encrypt                                   | CDP/Migration Server                | Encrypt table
cm-misc            | GET    /v1/protectdb/databases/{id}/job-detail                                | CDP/Database                        | Job Details
cm-misc            | GET    /v1/protectdb/databases/{id}/jobs                                      | CDP/Database                        | List Jobs
cm-misc            | DELETE /v1/protectdb/databases/{id}/migration-server                          | CDP/Migration Server                | Delete
cm-misc            | GET    /v1/protectdb/databases/{id}/migration-server                          | CDP/Migration Server                | Get
cm-misc            | PATCH  /v1/protectdb/databases/{id}/migration-server                          | CDP/Migration Server                | Update
cm-misc            | POST   /v1/protectdb/databases/{id}/migration-server                          | CDP/Migration Server                | Add
cm-misc            | GET    /v1/protectdb/databases/{id}/table                                     | CDP/Database                        | Get Table
cm-misc            | POST   /v1/protectdb/databases/{id}/table/{name}/cancel-job                   | CDP/Migration Server                | Cancel Job
cm-misc            | POST   /v1/protectdb/databases/{id}/table/{name}/restore-job                  | CDP/Migration Server                | Restore Job
cm-misc            | POST   /v1/protectdb/databases/{id}/table/{name}/resume-job                   | CDP/Migration Server                | Resume Job
cm-misc            | GET    /v1/protectdb/databases/{id}/tables                                    | CDP/Database                        | List Tables
cm-misc            | GET    /v1/protectdb/databases/{id}/user                                      | CDP/UserMapping                     | ListMap
cm-misc            | PATCH  /v1/protectdb/databases/{id}/user                                      | CDP/UserMapping                     | UpdateMap
cm-misc            | DELETE /v1/protectdb/databases/{id}/view                                      | CDP/Database                        | Delete Views and Trigger
cm-misc            | POST   /v1/protectdb/databases/{id}/view                                      | CDP/Database                        | Create Views and Trigger
cm-misc            | GET    /v1/reports/capacity-report                                            | Reports                             | Get
cm-misc            | GET    /v1/reports/orphaned-resources                                         | Reports                             | Get
cm-misc            | GET    /v1/scp/public-key                                                     | Backups/SCP Backup                  | Get
cm-misc            | POST   /v1/scp/public-key/rotate                                              | Backups/SCP Backup                  | POST
cm-misc            | POST   /v1/trusted-cas-create-many/                                           | Trusted CA Certificates             | Add
cm-misc            | GET    /v1/trusted-cas/                                                       | Trusted CA Certificates             | List
cm-misc            | POST   /v1/trusted-cas/                                                       | Trusted CA Certificates             | Add
cm-misc            | DELETE /v1/trusted-cas/{id}                                                   | Trusted CA Certificates             | Delete
cm-misc            | POST   /v1/uploadBackup                                                       | Backups/Backup-Restore              | Upload
cm-misc            | POST   /v1/usermgmt/connection-test/                                          | Connections/Connections             | Test
cm-misc            | GET    /v1/usermgmt/connections/                                              | Connections/Connections             | List
cm-misc            | POST   /v1/usermgmt/connections/                                              | Connections/Connections             | Create
cm-misc            | DELETE /v1/usermgmt/connections/{id}                                          | Connections/Connections             | Delete
cm-misc            | GET    /v1/usermgmt/connections/{id}                                          | Connections/Connections             | Get
cm-misc            | PATCH  /v1/usermgmt/connections/{id}                                          | Connections/Connections             | Update
cm-misc            | POST   /v1/usermgmt/connections/{id}/delete                                   | Connections/Connections             | Delete connection with optional parameters
cm-misc            | POST   /v1/usermgmt/connections/{id}/refresh                                  | Connections/Connections             | Refresh OIDC connection
cm-misc            | GET    /v1/usermgmt/connections/{id}/users/                                   | Connections/Connections             | List
cm-misc            | GET    /v1/usermgmt/connections/{id}/users/{user_id}                          | Connections/Connections             | Get
cm-misc            | GET    /v1/usermgmt/groupmaps/                                                | Groupmaps                           | List
cm-misc            | POST   /v1/usermgmt/groupmaps/                                                | Groupmaps                           | Create
cm-misc            | DELETE /v1/usermgmt/groupmaps/{id}                                            | Groupmaps                           | Delete
cm-misc            | GET    /v1/usermgmt/groupmaps/{id}                                            | Groupmaps                           | Get
cm-misc            | PATCH  /v1/usermgmt/groupmaps/{id}                                            | Groupmaps                           | Update
cm-misc            | POST   /v1/usermgmt/ldap-browse/{id}/groups                                   | LDAP Browse                         | List
cm-misc            | POST   /v1/usermgmt/ldap-browse/{id}/users                                    | LDAP Browse                         | List
cm-ops             | GET    /v1/backups                                                            | Backups/Backup-Restore              | List
cm-ops             | POST   /v1/backups                                                            | Backups/Backup-Restore              | Create
cm-ops             | DELETE /v1/backups/{id}                                                       | Backups/Backup-Restore              | Delete
cm-ops             | GET    /v1/backups/{id}                                                       | Backups/Backup-Restore              | Get
cm-ops             | POST   /v1/backups/{id}/browse                                                | Backups/Backup-Restore              | Browse backup
cm-ops             | DELETE /v1/backups/{id}/browse-cleanup                                        | Backups/Backup-Restore              | Browse-Cleanup
cm-ops             | POST   /v1/backups/{id}/browse-prepare                                        | Backups/Backup-Restore              | Browse-Prepare
cm-ops             | GET    /v1/backups/{id}/download                                              | Backups/Backup-Restore              | Download
cm-ops             | POST   /v1/backups/{id}/restore                                               | Backups/Backup-Restore              | Restore
cm-ops             | POST   /v1/backups/{id}/scp                                                   | Backups/SCP Backup                  | SCP
cm-ops             | GET    /v1/backups/{id}/scp-status                                            | Backups/SCP Backup                  | Recent backup transfer status of the provided backup
cm-ops             | GET    /v1/backups/{id}/scp-status/{scp_id}                                   | Backups/SCP Backup                  | SCP/SFTP Status
cm-ops             | POST   /v1/backups/{id}/scp/{connection_id}                                   | Backups/SCP Backup                  | SCP
cm-ops             | GET    /v1/licensing/features/                                                | Licensing                           | List
cm-ops             | GET    /v1/licensing/licenses/                                                | Licensing                           | List
cm-ops             | POST   /v1/licensing/licenses/                                                | Licensing                           | Add
cm-ops             | DELETE /v1/licensing/licenses/{id}                                            | Licensing                           | Delete
cm-ops             | GET    /v1/licensing/licenses/{id}                                            | Licensing                           | Get
cm-ops             | GET    /v1/licensing/lockdata                                                 | Licensing                           | Get
cm-ops             | GET    /v1/licensing/trials/                                                  | Licensing                           | List
cm-ops             | GET    /v1/licensing/trials/{id}                                              | Licensing                           | Get
cm-ops             | POST   /v1/licensing/trials/{id}/activate                                     | Licensing                           | Activate
cm-ops             | POST   /v1/licensing/trials/{id}/deactivate                                   | Licensing                           | Deactivate
cm-ops             | GET    /v1/migrations                                                         | Migrations                          | List
cm-ops             | POST   /v1/migrations                                                         | Migrations                          | Upload
cm-ops             | POST   /v1/migrations/download                                                | Migrations                          | Migration Data Download
cm-ops             | POST   /v1/migrations/generate-migration                                      | Migrations                          | Generate and upload migration file based on the key source.
cm-ops             | GET    /v1/migrations/status                                                  | Migrations                          | Status
cm-ops             | DELETE /v1/migrations/{id}                                                    | Migrations                          | Delete
cm-ops             | GET    /v1/migrations/{id}                                                    | Migrations                          | Get
cm-ops             | GET    /v1/migrations/{id}/containers                                         | Migrations                          | Get Containers from migration file
cm-ops             | GET    /v1/migrations/{id}/log                                                | Migrations                          | Log
cm-ops             | POST   /v1/migrations/{id}/migrate                                            | Migrations                          | Migrate
cm-ops             | GET    /v1/scheduler/job-configs                                              | Scheduler                           | List
cm-ops             | POST   /v1/scheduler/job-configs                                              | Scheduler                           | Create
cm-ops             | DELETE /v1/scheduler/job-configs/{id}                                         | Scheduler                           | Delete
cm-ops             | GET    /v1/scheduler/job-configs/{id}                                         | Scheduler                           | Get
cm-ops             | PATCH  /v1/scheduler/job-configs/{id}                                         | Scheduler                           | Update
cm-ops             | POST   /v1/scheduler/job-configs/{id}/run-now                                 | Scheduler                           | Run now
cm-ops             | GET    /v1/scheduler/jobs                                                     | Scheduler                           | List
cm-ops             | DELETE /v1/scheduler/jobs/{id}                                                | Scheduler                           | Delete
cm-ops             | GET    /v1/scheduler/jobs/{id}                                                | Scheduler                           | Get
cm-ops             | GET    /v1/scheduler/operations                                               | Scheduler                           | Get
cm-system          | DELETE /v1/cluster                                                            | Cluster                             | Delete
cm-system          | GET    /v1/cluster                                                            | Cluster                             | Info
cm-system          | POST   /v1/cluster/csr                                                        | Cluster                             | Create CSR
cm-system          | GET    /v1/cluster/errors                                                     | Cluster                             | List
cm-system          | POST   /v1/cluster/join                                                       | Cluster                             | Join
cm-system          | POST   /v1/cluster/new                                                        | Cluster                             | New
cm-system          | GET    /v1/cluster/summary                                                    | Cluster                             | Info
cm-system          | GET    /v1/configs/akeyless                                                   | Akeyless Configuration              | Get Akeyless Config
cm-system          | PATCH  /v1/configs/akeyless                                                   | Akeyless Configuration              | Update Akeyless Config
cm-system          | GET    /v1/configs/akeyless/customer-fragments                                | Akeyless Configuration              | List
cm-system          | POST   /v1/configs/akeyless/customer-fragments                                | Akeyless Configuration              | Create
cm-system          | GET    /v1/configs/akeyless/customer-fragments/export                         | Akeyless Configuration              | GET
cm-system          | POST   /v1/configs/akeyless/customer-fragments/import                         | Akeyless Configuration              | Import
cm-system          | DELETE /v1/configs/akeyless/customer-fragments/{name}                         | Akeyless Configuration              | Delete
cm-system          | PATCH  /v1/configs/akeyless/customer-fragments/{name}                         | Akeyless Configuration              | Patch
cm-system          | GET    /v1/configs/akeyless/gateway-version                                   | Akeyless Configuration              | Returns the active Akeyless version
cm-system          | PATCH  /v1/configs/akeyless/gateway-version                                   | Akeyless Configuration              | Updates the Akeyless version
cm-system          | GET    /v1/configs/akeyless/gateway-versions/                                 | Akeyless Configuration              | List
cm-system          | POST   /v1/configs/akeyless/gateway-versions/upload                           | Akeyless Configuration              | Upload
cm-system          | GET    /v1/configs/akeyless/status                                            | Akeyless Configuration              | Status
cm-system          | GET    /v1/configs/interfaces/                                                | Interfaces                          | List
cm-system          | POST   /v1/configs/interfaces/                                                | Interfaces                          | Add
cm-system          | DELETE /v1/configs/interfaces/{interface}                                     | Interfaces                          | Delete
cm-system          | GET    /v1/configs/interfaces/{interface}                                     | Interfaces                          | Get
cm-system          | PATCH  /v1/configs/interfaces/{interface}                                     | Interfaces                          | Update
cm-system          | POST   /v1/configs/interfaces/{interface}/auto-gen-server-cert                | Interfaces                          | AutoGen Server Certificate
cm-system          | GET    /v1/configs/interfaces/{interface}/certificate                         | Interfaces                          | Get Certificate
cm-system          | PUT    /v1/configs/interfaces/{interface}/certificate                         | Interfaces                          | Put Certificate
cm-system          | GET    /v1/configs/interfaces/{interface}/csr                                 | Interfaces                          | Get CSR
cm-system          | POST   /v1/configs/interfaces/{interface}/csr                                 | Interfaces                          | CSR
cm-system          | POST   /v1/configs/interfaces/{interface}/disable                             | Interfaces                          | Disable Interface
cm-system          | POST   /v1/configs/interfaces/{interface}/enable                              | Interfaces                          | Enable Interface
cm-system          | DELETE /v1/configs/interfaces/{interface}/renewal-certificate                 | Interfaces                          | Delete Upcoming Certificate
cm-system          | GET    /v1/configs/interfaces/{interface}/renewal-certificate                 | Interfaces                          | Get Upcoming Certificate
cm-system          | PUT    /v1/configs/interfaces/{interface}/renewal-certificate                 | Interfaces                          | Put upcoming Certificate
cm-system          | POST   /v1/configs/interfaces/{interface}/renewal-certificate/apply           | Interfaces                          | Apply Upcoming Certificate
cm-system          | POST   /v1/configs/interfaces/{interface}/restore-default-tls-ciphers         | Interfaces                          | Restores Interface TLS Ciphers and Groups
cm-system          | POST   /v1/configs/interfaces/{interface}/use-certificate                     | Interfaces                          | Copy Interface Certificate.
cm-system          | POST   /v1/configs/log-forwarders-domain-redirection/disable                  | Log Forwarders                      | Disable Domain Log Messages Redirection
cm-system          | POST   /v1/configs/log-forwarders-domain-redirection/enable                   | Log Forwarders                      | Enable Domain Log Messages Redirection
cm-system          | GET    /v1/configs/log-forwarders-domain-redirection/status                   | Log Forwarders                      | Domain Log Messages Redirection Status
cm-system          | GET    /v1/configs/log-forwarders/                                            | Log Forwarders                      | List
cm-system          | POST   /v1/configs/log-forwarders/                                            | Log Forwarders                      | Add
cm-system          | DELETE /v1/configs/log-forwarders/{id}                                        | Log Forwarders                      | Delete
cm-system          | GET    /v1/configs/log-forwarders/{id}                                        | Log Forwarders                      | Get
cm-system          | PATCH  /v1/configs/log-forwarders/{id}                                        | Log Forwarders                      | Update
cm-system          | GET    /v1/configs/loki                                                       | Loki Configuration                  | Get
cm-system          | PATCH  /v1/configs/loki                                                       | Loki Configuration                  | Update
cm-system          | GET    /v1/configs/properties                                                 | Properties                          | List
cm-system          | GET    /v1/configs/properties/{name}                                          | Properties                          | Get
cm-system          | PATCH  /v1/configs/properties/{name}                                          | Properties                          | Update
cm-system          | POST   /v1/configs/properties/{name}/reset                                    | Properties                          | Reset
cm-system          | DELETE /v1/configs/proxy                                                      | Proxy                               | Delete
cm-system          | GET    /v1/configs/proxy                                                      | Proxy                               | Get
cm-system          | PATCH  /v1/configs/proxy                                                      | Proxy                               | Update proxy
cm-system          | PUT    /v1/configs/proxy                                                      | Proxy                               | Set proxy
cm-system          | POST   /v1/configs/proxy/test                                                 | Proxy                               | Test proxy
cm-system          | GET    /v1/configs/syslogs/                                                   | Syslog Connections                  | List
cm-system          | POST   /v1/configs/syslogs/                                                   | Syslog Connections                  | Add
cm-system          | DELETE /v1/configs/syslogs/{id}                                               | Syslog Connections                  | Delete
cm-system          | GET    /v1/configs/syslogs/{id}                                               | Syslog Connections                  | Get
cm-system          | PATCH  /v1/configs/syslogs/{id}                                               | Syslog Connections                  | Update
cm-system          | GET    /v1/system/alarms                                                      | Alarms                              | List Alarms
cm-system          | POST   /v1/system/alarms/{id}/acknowledge                                     | Alarms                              | Acknowledge alarm
cm-system          | POST   /v1/system/alarms/{id}/clear                                           | Alarms                              | Clear alarm
cm-system          | GET    /v1/system/hsm/clients/stcidentity/download                            | HSM Clients                         | Luna STC client identity file download
cm-system          | GET    /v1/system/hsm/servers                                                 | HSM Servers                         | List
cm-system          | POST   /v1/system/hsm/servers                                                 | HSM Servers                         | Add
cm-system          | DELETE /v1/system/hsm/servers/{id}                                            | HSM Servers                         | Delete
cm-system          | GET    /v1/system/hsm/servers/{id}                                            | HSM Servers                         | Get
cm-system          | POST   /v1/system/hsm/setup                                                   | HSM Servers                         | Setup
cm-system          | GET    /v1/system/info                                                        | Info                                | Get
cm-system          | PATCH  /v1/system/info                                                        | Info                                | Set
cm-system          | GET    /v1/system/metrics/prometheus                                          | Prometheus Metrics                  | Get metrics
cm-system          | POST   /v1/system/metrics/prometheus/disable                                  | Prometheus Metrics                  | Disable metrics collection
cm-system          | POST   /v1/system/metrics/prometheus/enable                                   | Prometheus Metrics                  | Enable metrics collection
cm-system          | POST   /v1/system/metrics/prometheus/renew-token                              | Prometheus Metrics                  | Renew metrics collection token
cm-system          | GET    /v1/system/metrics/prometheus/status                                   | Prometheus Metrics                  | get configuration
cm-system          | GET    /v1/system/mkeks                                                       | MKek                                | List
cm-system          | POST   /v1/system/mkeks/rotate                                                | MKek                                | Rotate MKek
cm-system          | GET    /v1/system/mkeks/{id}                                                  | MKek                                | Get MKek
cm-system          | POST   /v1/system/network/checkport                                           | Network                             | Check if a port is available on a remote system
cm-system          | GET    /v1/system/network/interfaces                                          | Network                             | List
cm-system          | GET    /v1/system/network/interfaces/{interface}                              | Network                             | Get
cm-system          | PATCH  /v1/system/network/interfaces/{interface}                              | Network                             | Update
cm-system          | POST   /v1/system/network/lookup                                              | Network                             | Query the mapping between domain name and ipaddress or other dns records.
cm-system          | POST   /v1/system/network/ping                                                | Network                             | Ping a host
cm-system          | POST   /v1/system/network/traceroute                                          | Network                             | Tracerouting a host
cm-system          | GET    /v1/system/ntp/servers                                                 | NTP Servers                         | List
cm-system          | POST   /v1/system/ntp/servers                                                 | NTP Servers                         | Add
cm-system          | DELETE /v1/system/ntp/servers/{host}                                          | NTP Servers                         | Delete
cm-system          | GET    /v1/system/ntp/servers/{host}                                          | NTP Servers                         | Get
cm-system          | GET    /v1/system/ntp/status                                                  | NTP Servers                         | Status
cm-system          | GET    /v1/system/products                                                    | Products                            | List
cm-system          | GET    /v1/system/products/{name}                                             | Products                            | Get Product's state
cm-system          | POST   /v1/system/products/{name}/disable                                     | Products                            | Disable Product
cm-system          | POST   /v1/system/products/{name}/enable                                      | Products                            | Enable product
cm-system          | GET    /v1/system/rot-keys                                                    | Root of Trust Keys                  | List
cm-system          | DELETE /v1/system/rot-keys/{id}                                               | Root of Trust Keys                  | Delete
cm-system          | GET    /v1/system/rot-keys/{id}                                               | Root of Trust Keys                  | Get
cm-system          | POST   /v1/system/rotate-rot-keys                                             | Root of Trust Keys                  | Rotate
cm-system          | POST   /v1/system/services/reset                                              | Services                            | Reset
cm-system          | POST   /v1/system/services/restart                                            | Services                            | Restart
cm-system          | GET    /v1/system/services/status                                             | Services                            | Status
cm-system          | GET    /v1/system/ssh/kex                                                     | SSH                                 | List
cm-system          | PATCH  /v1/system/ssh/kex                                                     | SSH                                 | Update
cm-system          | POST   /v1/system/ssh/keys                                                    | SSH                                 | Add
connections        | GET    /v1/connectionmgmt/connections                                         | Connection Manager                  | List
connections        | POST   /v1/connectionmgmt/connections/csr                                     | Connection Manager/CSR Creation     | Creates a Certificate Signing Request (CSR).
connections        | DELETE /v1/connectionmgmt/connections/{id}                                    | Connection Manager                  | Delete
connections        | POST   /v1/connectionmgmt/connections/{id}/delete                             | Connection Manager                  | Force delete an existing connection.
connections        | POST   /v1/connectionmgmt/services/akeyless/connection-test                   | Connection Manager/Akeyless Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/akeyless/connections                       | Connection Manager/Akeyless Connections | List
connections        | POST   /v1/connectionmgmt/services/akeyless/connections                       | Connection Manager/Akeyless Connections | Create a new Akeyless connection.
connections        | DELETE /v1/connectionmgmt/services/akeyless/connections/{id}                  | Connection Manager/Akeyless Connections | Delete
connections        | GET    /v1/connectionmgmt/services/akeyless/connections/{id}                  | Connection Manager/Akeyless Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/akeyless/connections/{id}                  | Connection Manager/Akeyless Connections | Update
connections        | POST   /v1/connectionmgmt/services/akeyless/connections/{id}/test             | Connection Manager/Akeyless Connections | Test existing connection
connections        | POST   /v1/connectionmgmt/services/aws/connection-test                        | Connection Manager/AWS Connections  | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/aws/connections                            | Connection Manager/AWS Connections  | List
connections        | POST   /v1/connectionmgmt/services/aws/connections                            | Connection Manager/AWS Connections  | Create a new AWS connection.
connections        | DELETE /v1/connectionmgmt/services/aws/connections/{id}                       | Connection Manager/AWS Connections  | Delete
connections        | GET    /v1/connectionmgmt/services/aws/connections/{id}                       | Connection Manager/AWS Connections  | Get
connections        | PATCH  /v1/connectionmgmt/services/aws/connections/{id}                       | Connection Manager/AWS Connections  | Update
connections        | POST   /v1/connectionmgmt/services/aws/connections/{id}/test                  | Connection Manager/AWS Connections  | Test existing connection
connections        | POST   /v1/connectionmgmt/services/azure/connection-test                      | Connection Manager/Azure Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/azure/connections                          | Connection Manager/Azure Connections | List
connections        | POST   /v1/connectionmgmt/services/azure/connections                          | Connection Manager/Azure Connections | Create a new Azure connection.
connections        | DELETE /v1/connectionmgmt/services/azure/connections/{id}                     | Connection Manager/Azure Connections | Delete
connections        | GET    /v1/connectionmgmt/services/azure/connections/{id}                     | Connection Manager/Azure Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/azure/connections/{id}                     | Connection Manager/Azure Connections | Update
connections        | POST   /v1/connectionmgmt/services/azure/connections/{id}/test                | Connection Manager/Azure Connections | Test existing connection
connections        | POST   /v1/connectionmgmt/services/cm/connection-test                         | Connection Manager/CM Connections   | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/cm/connections                             | Connection Manager/CM Connections   | List
connections        | POST   /v1/connectionmgmt/services/cm/connections                             | Connection Manager/CM Connections   | Create a new CM connection
connections        | DELETE /v1/connectionmgmt/services/cm/connections/{id}                        | Connection Manager/CM Connections   | Delete
connections        | GET    /v1/connectionmgmt/services/cm/connections/{id}                        | Connection Manager/CM Connections   | Get
connections        | PATCH  /v1/connectionmgmt/services/cm/connections/{id}                        | Connection Manager/CM Connections   | Update
connections        | POST   /v1/connectionmgmt/services/cm/connections/{id}/test                   | Connection Manager/CM Connections   | Post
connections        | GET    /v1/connectionmgmt/services/confidential-computing/connections         | Connection Manager/CC Connections   | List
connections        | POST   /v1/connectionmgmt/services/confidential-computing/connections         | Connection Manager/CC Connections   | Creates a new CC connection.
connections        | GET    /v1/connectionmgmt/services/confidential-computing/connections/{id}    | Connection Manager/CC Connections   | Get
connections        | PATCH  /v1/connectionmgmt/services/confidential-computing/connections/{id}    | Connection Manager/CC Connections   | Update
connections        | POST   /v1/connectionmgmt/services/confidential-computing/connections/{id}/delete | Connection Manager/CC Connections   | Delete a CC connection with optional parameters
connections        | POST   /v1/connectionmgmt/services/dsm/connection-test                        | Connection Manager/DSM Connections  | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/dsm/connections                            | Connection Manager/DSM Connections  | List
connections        | POST   /v1/connectionmgmt/services/dsm/connections                            | Connection Manager/DSM Connections  | Create a new connection
connections        | DELETE /v1/connectionmgmt/services/dsm/connections/{id}                       | Connection Manager/DSM Connections  | Delete
connections        | GET    /v1/connectionmgmt/services/dsm/connections/{id}                       | Connection Manager/DSM Connections  | Get
connections        | PATCH  /v1/connectionmgmt/services/dsm/connections/{id}                       | Connection Manager/DSM Connections  | Update
connections        | GET    /v1/connectionmgmt/services/dsm/connections/{id}/nodes                 | Connection Manager/DSM Connections  | List
connections        | POST   /v1/connectionmgmt/services/dsm/connections/{id}/nodes                 | Connection Manager/DSM Connections  | Add a new DSM Node
connections        | DELETE /v1/connectionmgmt/services/dsm/connections/{id}/nodes/{node_id}       | Connection Manager/DSM Connections  | Delete
connections        | GET    /v1/connectionmgmt/services/dsm/connections/{id}/nodes/{node_id}       | Connection Manager/DSM Connections  | Get
connections        | PATCH  /v1/connectionmgmt/services/dsm/connections/{id}/nodes/{node_id}       | Connection Manager/DSM Connections  | Update
connections        | POST   /v1/connectionmgmt/services/dsm/connections/{id}/test                  | Connection Manager/DSM Connections  | Post
connections        | GET    /v1/connectionmgmt/services/external-cm                                | Connection Manager/External CM Server | List
connections        | POST   /v1/connectionmgmt/services/external-cm                                | Connection Manager/External CM Server | Creates a new external CM.
connections        | DELETE /v1/connectionmgmt/services/external-cm/{id}                           | Connection Manager/External CM Server | Delete
connections        | GET    /v1/connectionmgmt/services/external-cm/{id}                           | Connection Manager/External CM Server | Get
connections        | POST   /v1/connectionmgmt/services/external-cm/{id}/ca                        | Connection Manager/External CM Server | Add a trusted CA
connections        | DELETE /v1/connectionmgmt/services/external-cm/{id}/ca/{ca_id}                | Connection Manager/External CM Server | Delete
connections        | POST   /v1/connectionmgmt/services/external-cm/{id}/nodes                     | Connection Manager/External CM Server | Adds a new node
connections        | DELETE /v1/connectionmgmt/services/external-cm/{id}/nodes/{node_id}           | Connection Manager/External CM Server | Delete
connections        | GET    /v1/connectionmgmt/services/external-cm/{id}/nodes/{node_id}           | Connection Manager/External CM Server | Get
connections        | PATCH  /v1/connectionmgmt/services/external-cm/{id}/nodes/{node_id}           | Connection Manager/External CM Server | Update
connections        | POST   /v1/connectionmgmt/services/gcp/connection-test                        | Connection Manager/Google Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/gcp/connections                            | Connection Manager/Google Connections | List
connections        | POST   /v1/connectionmgmt/services/gcp/connections                            | Connection Manager/Google Connections | Create a new GCP connection.
connections        | DELETE /v1/connectionmgmt/services/gcp/connections/{id}                       | Connection Manager/Google Connections | Delete
connections        | GET    /v1/connectionmgmt/services/gcp/connections/{id}                       | Connection Manager/Google Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/gcp/connections/{id}                       | Connection Manager/Google Connections | Update
connections        | POST   /v1/connectionmgmt/services/gcp/connections/{id}/test                  | Connection Manager/Google Connections | Test existing connection
connections        | POST   /v1/connectionmgmt/services/hadoop/connection-test                     | Connection Manager/Hadoop Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/hadoop/connections                         | Connection Manager/Hadoop Connections | List
connections        | POST   /v1/connectionmgmt/services/hadoop/connections                         | Connection Manager/Hadoop Connections | Create a new connection
connections        | DELETE /v1/connectionmgmt/services/hadoop/connections/{id}                    | Connection Manager/Hadoop Connections | Delete
connections        | GET    /v1/connectionmgmt/services/hadoop/connections/{id}                    | Connection Manager/Hadoop Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/hadoop/connections/{id}                    | Connection Manager/Hadoop Connections | Update
connections        | GET    /v1/connectionmgmt/services/hadoop/connections/{id}/nodes              | Connection Manager/Hadoop Connections | List
connections        | POST   /v1/connectionmgmt/services/hadoop/connections/{id}/nodes              | Connection Manager/Hadoop Connections | Add a new Hadoop Node
connections        | DELETE /v1/connectionmgmt/services/hadoop/connections/{id}/nodes/{node_id}    | Connection Manager/Hadoop Connections | Delete
connections        | GET    /v1/connectionmgmt/services/hadoop/connections/{id}/nodes/{node_id}    | Connection Manager/Hadoop Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/hadoop/connections/{id}/nodes/{node_id}    | Connection Manager/Hadoop Connections | Update
connections        | POST   /v1/connectionmgmt/services/hadoop/connections/{id}/test               | Connection Manager/Hadoop Connections | Post
connections        | POST   /v1/connectionmgmt/services/ldap/connection-test                       | Connection Manager/LDAP Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/ldap/connections                           | Connection Manager/LDAP Connections | List
connections        | POST   /v1/connectionmgmt/services/ldap/connections                           | Connection Manager/LDAP Connections | Creates a new LDAP connection.
connections        | DELETE /v1/connectionmgmt/services/ldap/connections/{id}                      | Connection Manager/LDAP Connections | Delete
connections        | GET    /v1/connectionmgmt/services/ldap/connections/{id}                      | Connection Manager/LDAP Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/ldap/connections/{id}                      | Connection Manager/LDAP Connections | Update
connections        | POST   /v1/connectionmgmt/services/ldap/connections/{id}/test                 | Connection Manager/LDAP Connections | Test existing connection
connections        | POST   /v1/connectionmgmt/services/log-forwarders/elasticsearch/connection-test | Connection Manager/Elasticsearch Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/log-forwarders/elasticsearch/connections   | Connection Manager/Elasticsearch Connections | List
connections        | POST   /v1/connectionmgmt/services/log-forwarders/elasticsearch/connections   | Connection Manager/Elasticsearch Connections | Creates a new Elasticsearch connection.
connections        | DELETE /v1/connectionmgmt/services/log-forwarders/elasticsearch/connections/{id} | Connection Manager/Elasticsearch Connections | Delete
connections        | GET    /v1/connectionmgmt/services/log-forwarders/elasticsearch/connections/{id} | Connection Manager/Elasticsearch Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/log-forwarders/elasticsearch/connections/{id} | Connection Manager/Elasticsearch Connections | Update
connections        | POST   /v1/connectionmgmt/services/log-forwarders/elasticsearch/connections/{id}/test | Connection Manager/Elasticsearch Connections | Test existing connection
connections        | POST   /v1/connectionmgmt/services/log-forwarders/loki/connection-test        | Connection Manager/Loki Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/log-forwarders/loki/connections            | Connection Manager/Loki Connections | List
connections        | POST   /v1/connectionmgmt/services/log-forwarders/loki/connections            | Connection Manager/Loki Connections | Creates a new Loki connection.
connections        | DELETE /v1/connectionmgmt/services/log-forwarders/loki/connections/{id}       | Connection Manager/Loki Connections | Delete
connections        | GET    /v1/connectionmgmt/services/log-forwarders/loki/connections/{id}       | Connection Manager/Loki Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/log-forwarders/loki/connections/{id}       | Connection Manager/Loki Connections | Update
connections        | POST   /v1/connectionmgmt/services/log-forwarders/loki/connections/{id}/test  | Connection Manager/Loki Connections | Test existing connection
connections        | POST   /v1/connectionmgmt/services/log-forwarders/syslog/connection-test      | Connection Manager/Syslog Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/log-forwarders/syslog/connections          | Connection Manager/Syslog Connections | List
connections        | POST   /v1/connectionmgmt/services/log-forwarders/syslog/connections          | Connection Manager/Syslog Connections | Creates a new Syslog connection.
connections        | DELETE /v1/connectionmgmt/services/log-forwarders/syslog/connections/{id}     | Connection Manager/Syslog Connections | Delete
connections        | GET    /v1/connectionmgmt/services/log-forwarders/syslog/connections/{id}     | Connection Manager/Syslog Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/log-forwarders/syslog/connections/{id}     | Connection Manager/Syslog Connections | Update
connections        | POST   /v1/connectionmgmt/services/log-forwarders/syslog/connections/{id}/test | Connection Manager/Syslog Connections | Test existing connection
connections        | GET    /v1/connectionmgmt/services/luna-network/client                        | Connection Manager/Luna Network HSM Servers | Get
connections        | POST   /v1/connectionmgmt/services/luna-network/connection-test               | Connection Manager/Luna Network HSM Connections | Tests Luna Network HSM connection parameters.
connections        | GET    /v1/connectionmgmt/services/luna-network/connection-test/{id}          | Connection Manager/Luna Network HSM Connections | Get connection status
connections        | GET    /v1/connectionmgmt/services/luna-network/connections                   | Connection Manager/Luna Network HSM Connections | List
connections        | POST   /v1/connectionmgmt/services/luna-network/connections                   | Connection Manager/Luna Network HSM Connections | Create a new Luna Network HSM connection.
connections        | DELETE /v1/connectionmgmt/services/luna-network/connections/{id}              | Connection Manager/Luna Network HSM Connections | Delete
connections        | GET    /v1/connectionmgmt/services/luna-network/connections/{id}              | Connection Manager/Luna Network HSM Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/luna-network/connections/{id}              | Connection Manager/Luna Network HSM Connections | Update
connections        | POST   /v1/connectionmgmt/services/luna-network/connections/{id}/partitions/  | Connection Manager/Luna Network HSM Connections | Add
connections        | DELETE /v1/connectionmgmt/services/luna-network/connections/{id}/partitions/{partition_id} | Connection Manager/Luna Network HSM Connections | Delete
connections        | POST   /v1/connectionmgmt/services/luna-network/connections/{id}/test         | Connection Manager/Luna Network HSM Connections | Test existing connection
connections        | GET    /v1/connectionmgmt/services/luna-network/servers                       | Connection Manager/Luna Network HSM Servers | List
connections        | POST   /v1/connectionmgmt/services/luna-network/servers                       | Connection Manager/Luna Network HSM Servers | Adds a new Luna Network HSM Server.
connections        | DELETE /v1/connectionmgmt/services/luna-network/servers/{id}                  | Connection Manager/Luna Network HSM Servers | Delete
connections        | GET    /v1/connectionmgmt/services/luna-network/servers/{id}                  | Connection Manager/Luna Network HSM Servers | Get
connections        | POST   /v1/connectionmgmt/services/luna-network/servers/{id}/delete           | Connection Manager/Luna Network HSM Servers | Force delete an existing HSM server.
connections        | POST   /v1/connectionmgmt/services/luna-network/servers/{id}/disable-stc      | Connection Manager/Luna Network HSM Servers | Post
connections        | POST   /v1/connectionmgmt/services/luna-network/servers/{id}/enable-stc       | Connection Manager/Luna Network HSM Servers | Post
connections        | GET    /v1/connectionmgmt/services/luna-network/stc-partitions                | Connection Manager/Luna Network HSM STC Partition | List
connections        | POST   /v1/connectionmgmt/services/luna-network/stc-partitions                | Connection Manager/Luna Network HSM STC Partition | Registers a new Luna Network HSM STC Partition.
connections        | DELETE /v1/connectionmgmt/services/luna-network/stc-partitions/{id}           | Connection Manager/Luna Network HSM STC Partition | Delete
connections        | GET    /v1/connectionmgmt/services/luna-network/stc-partitions/{id}           | Connection Manager/Luna Network HSM STC Partition | Get
connections        | POST   /v1/connectionmgmt/services/oci/connection-test                        | Connection Manager/Oracle Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/oci/connections                            | Connection Manager/Oracle Connections | List
connections        | POST   /v1/connectionmgmt/services/oci/connections                            | Connection Manager/Oracle Connections | Creates a new OCI connection.
connections        | DELETE /v1/connectionmgmt/services/oci/connections/{id}                       | Connection Manager/Oracle Connections | Delete
connections        | GET    /v1/connectionmgmt/services/oci/connections/{id}                       | Connection Manager/Oracle Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/oci/connections/{id}                       | Connection Manager/Oracle Connections | Update
connections        | POST   /v1/connectionmgmt/services/oci/connections/{id}/test                  | Connection Manager/Oracle Connections | Test existing connection
connections        | GET    /v1/connectionmgmt/services/oidc/connections                           | Connection Manager/OIDC Connections | List
connections        | POST   /v1/connectionmgmt/services/oidc/connections                           | Connection Manager/OIDC Connections | Creates a new OIDC connection.
connections        | GET    /v1/connectionmgmt/services/oidc/connections/{id}                      | Connection Manager/OIDC Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/oidc/connections/{id}                      | Connection Manager/OIDC Connections | Update
connections        | POST   /v1/connectionmgmt/services/oidc/connections/{id}/delete               | Connection Manager/OIDC Connections | Delete connection with optional parameters
connections        | POST   /v1/connectionmgmt/services/salesforce/connection-test                 | Connection Manager/Salesforce Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/salesforce/connections                     | Connection Manager/Salesforce Connections | List
connections        | POST   /v1/connectionmgmt/services/salesforce/connections                     | Connection Manager/Salesforce Connections | Create a new Salesforce connection.
connections        | DELETE /v1/connectionmgmt/services/salesforce/connections/{id}                | Connection Manager/Salesforce Connections | Delete
connections        | GET    /v1/connectionmgmt/services/salesforce/connections/{id}                | Connection Manager/Salesforce Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/salesforce/connections/{id}                | Connection Manager/Salesforce Connections | Update
connections        | POST   /v1/connectionmgmt/services/salesforce/connections/{id}/test           | Connection Manager/Salesforce Connections | Test existing connection
connections        | POST   /v1/connectionmgmt/services/sap-dc/connection-test                     | Connection Manager/SAP Data Custodian Connections | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/sap-dc/connections                         | Connection Manager/SAP Data Custodian Connections | List
connections        | POST   /v1/connectionmgmt/services/sap-dc/connections                         | Connection Manager/SAP Data Custodian Connections | Creates a new SAP Data Custodian connection.
connections        | DELETE /v1/connectionmgmt/services/sap-dc/connections/{id}                    | Connection Manager/SAP Data Custodian Connections | Delete
connections        | GET    /v1/connectionmgmt/services/sap-dc/connections/{id}                    | Connection Manager/SAP Data Custodian Connections | Get
connections        | PATCH  /v1/connectionmgmt/services/sap-dc/connections/{id}                    | Connection Manager/SAP Data Custodian Connections | Update
connections        | POST   /v1/connectionmgmt/services/sap-dc/connections/{id}/test               | Connection Manager/SAP Data Custodian Connections | Test existing connection
connections        | POST   /v1/connectionmgmt/services/scp/connection-test                        | Connection Manager/SCP Connections  | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/scp/connections                            | Connection Manager/SCP Connections  | List
connections        | POST   /v1/connectionmgmt/services/scp/connections                            | Connection Manager/SCP Connections  | Create a new connection
connections        | DELETE /v1/connectionmgmt/services/scp/connections/{id}                       | Connection Manager/SCP Connections  | Delete
connections        | GET    /v1/connectionmgmt/services/scp/connections/{id}                       | Connection Manager/SCP Connections  | Get
connections        | PATCH  /v1/connectionmgmt/services/scp/connections/{id}                       | Connection Manager/SCP Connections  | Update
connections        | POST   /v1/connectionmgmt/services/scp/connections/{id}/test                  | Connection Manager/SCP Connections  | Test existing connection
connections        | POST   /v1/connectionmgmt/services/smb/connection-test                        | Connection Manager/SMB Connections  | Test connection parameters
connections        | GET    /v1/connectionmgmt/services/smb/connections                            | Connection Manager/SMB Connections  | List
connections        | POST   /v1/connectionmgmt/services/smb/connections                            | Connection Manager/SMB Connections  | Create a new connection
connections        | DELETE /v1/connectionmgmt/services/smb/connections/{id}                       | Connection Manager/SMB Connections  | Delete
connections        | GET    /v1/connectionmgmt/services/smb/connections/{id}                       | Connection Manager/SMB Connections  | Get
connections        | PATCH  /v1/connectionmgmt/services/smb/connections/{id}                       | Connection Manager/SMB Connections  | Update
connections        | POST   /v1/connectionmgmt/services/smb/connections/{id}/test                  | Connection Manager/SMB Connections  | Test existing connection
cte                | GET    /v1/transparent-encryption/clientgroups/                               | CTE/ClientGroups                    | List
cte                | POST   /v1/transparent-encryption/clientgroups/                               | CTE/ClientGroups                    | Create
cte                | GET    /v1/transparent-encryption/clientgroups/{clientGroupId}/dps/           | CTE/ClientGroups-DesignatedPrimarySet | List
cte                | POST   /v1/transparent-encryption/clientgroups/{clientGroupId}/dps/           | CTE/ClientGroups-DesignatedPrimarySet | Create
cte                | DELETE /v1/transparent-encryption/clientgroups/{clientGroupId}/dps/{dpsId}    | CTE/ClientGroups-DesignatedPrimarySet | Delete
cte                | GET    /v1/transparent-encryption/clientgroups/{clientGroupId}/dps/{dpsId}    | CTE/ClientGroups-DesignatedPrimarySet | Get
cte                | PATCH  /v1/transparent-encryption/clientgroups/{clientGroupId}/dps/{dpsId}    | CTE/ClientGroups-DesignatedPrimarySet | Update
cte                | GET    /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/   | CTE/ClientGroups-GuardPoints        | List
cte                | POST   /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/   | CTE/ClientGroups-GuardPoints        | Create
cte                | PATCH  /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/enable/ | CTE/ClientGroups-GuardPoints        | Enable/disable guardpoints
cte                | PATCH  /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/unguard/ | CTE/ClientGroups-GuardPoints        | Unguard GuardPoints
cte                | POST   /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/upload-list | CTE/ClientGroups-GuardPoints        | Upload
cte                | GET    /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/{guardpointId} | CTE/ClientGroups-GuardPoints        | Get
cte                | PATCH  /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/{guardpointId} | CTE/ClientGroups-GuardPoints        | Update
cte                | PATCH  /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/{guardpointId}/early-access | CTE/ClientGroups-GuardPoints        | Update Early Access on GuardPoint
cte                | PATCH  /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/{guardpointId}/preserve-sparse-regions-off | CTE/ClientGroups-GuardPoints        | Turn Off Preserve Spase Region
cte                | PATCH  /v1/transparent-encryption/clientgroups/{clientGroupId}/guardpoints/{guardpointId}/unguard | CTE/ClientGroups-GuardPoints        | Unguard
cte                | DELETE /v1/transparent-encryption/clientgroups/{id}                           | CTE/ClientGroups                    | Delete
cte                | GET    /v1/transparent-encryption/clientgroups/{id}                           | CTE/ClientGroups                    | Get
cte                | PATCH  /v1/transparent-encryption/clientgroups/{id}                           | CTE/ClientGroups                    | Update
cte                | PATCH  /v1/transparent-encryption/clientgroups/{id}/auth-binaries             | CTE/ClientGroups                    | Update Client Settings
cte                | GET    /v1/transparent-encryption/clientgroups/{id}/clients/                  | CTE/ClientGroups                    | List Clients in ClientGroup
cte                | POST   /v1/transparent-encryption/clientgroups/{id}/clients/                  | CTE/ClientGroups                    | Add Client to ClientGroup
cte                | DELETE /v1/transparent-encryption/clientgroups/{id}/clients/{client_id}       | CTE/ClientGroups                    | Remove Client from ClientGroup
cte                | GET    /v1/transparent-encryption/clientgroups/{id}/clients/{client_id}       | CTE/ClientGroups                    | Get ClientGroup Client Association
cte                | POST   /v1/transparent-encryption/clientgroups/{id}/ldtpause/                 | CTE/ClientGroups                    | Send LDT Suspend/Resume Request to CTE ClientGroup
cte                | PATCH  /v1/transparent-encryption/clientgroups/{id}/password                  | CTE/ClientGroups                    | Update Client Group Password
cte                | PATCH  /v1/transparent-encryption/clientgroups/{id}/resetpassword             | CTE/ClientGroups                    | Reset Password for CTE ClientGroup
cte                | GET    /v1/transparent-encryption/clients/                                    | CTE/Clients                         | List
cte                | POST   /v1/transparent-encryption/clients/                                    | CTE/Clients                         | Create
cte                | POST   /v1/transparent-encryption/clients/clear-agentinfo                     | CTE/Clients                         | Clears AgentInfo
cte                | PATCH  /v1/transparent-encryption/clients/delete/                             | CTE/Clients                         | Delete Clients
cte                | GET    /v1/transparent-encryption/clients/{clientId}/guardpoints/             | CTE/Clients-GuardPoints             | List
cte                | POST   /v1/transparent-encryption/clients/{clientId}/guardpoints/             | CTE/Clients-GuardPoints             | Create
cte                | PATCH  /v1/transparent-encryption/clients/{clientId}/guardpoints/enable       | CTE/Clients-GuardPoints             | Enable/disable guardpoints
cte                | PATCH  /v1/transparent-encryption/clients/{clientId}/guardpoints/unguard/     | CTE/Clients-GuardPoints             | Unguard GuardPoints
cte                | POST   /v1/transparent-encryption/clients/{clientId}/guardpoints/upload-list  | CTE/Clients-GuardPoints             | Upload
cte                | GET    /v1/transparent-encryption/clients/{clientId}/guardpoints/{guardpointId} | CTE/Clients-GuardPoints             | Get
cte                | PATCH  /v1/transparent-encryption/clients/{clientId}/guardpoints/{guardpointId} | CTE/Clients-GuardPoints             | Update
cte                | PATCH  /v1/transparent-encryption/clients/{clientId}/guardpoints/{guardpointId}/early-access | CTE/Clients-GuardPoints             | Update Early Access on GuardPoint
cte                | PATCH  /v1/transparent-encryption/clients/{clientId}/guardpoints/{guardpointId}/preserve-sparse-regions-off | CTE/Clients-GuardPoints             | Turn Off Preserve Spase Region
cte                | GET    /v1/transparent-encryption/clients/{clientId}/guardpoints/{guardpointId}/status | CTE/Clients-GuardPoints             | Status
cte                | PATCH  /v1/transparent-encryption/clients/{clientId}/guardpoints/{guardpointId}/unguard | CTE/Clients-GuardPoints             | Unguard
cte                | GET    /v1/transparent-encryption/clients/{id}                                | CTE/Clients                         | Get
cte                | PATCH  /v1/transparent-encryption/clients/{id}                                | CTE/Clients                         | Update
cte                | PATCH  /v1/transparent-encryption/clients/{id}/auth-binaries                  | CTE/Clients                         | Update Client Authentication Binaries
cte                | GET    /v1/transparent-encryption/clients/{id}/challenge-response/{challenge} | CTE/Clients                         | Get Challenge-Response
cte                | GET    /v1/transparent-encryption/clients/{id}/check-agentinfo                | CTE/Clients                         | Check AgentInfo
cte                | GET    /v1/transparent-encryption/clients/{id}/clientgroups                   | CTE/Clients                         | Get ClientGroups for Client
cte                | PATCH  /v1/transparent-encryption/clients/{id}/delete                         | CTE/Clients                         | Delete Client
cte                | GET    /v1/transparent-encryption/clients/{id}/download-agentinfo             | CTE/Clients                         | Download AgentInfo
cte                | POST   /v1/transparent-encryption/clients/{id}/enable-unique-to-client        | CTE/Clients                         | Enable Unique to Client
cte                | POST   /v1/transparent-encryption/clients/{id}/get-agentinfo                  | CTE/Clients                         | Collect AgentInfo
cte                | POST   /v1/transparent-encryption/clients/{id}/ldtpause/                      | CTE/Clients                         | Send LDT Suspend/Resume Request to CTE Client
cte                | PATCH  /v1/transparent-encryption/clients/{id}/password                       | CTE/Clients                         | Update Client Password
cte                | POST   /v1/transparent-encryption/clients/{id}/query-status-update            | CTE/Clients                         | Query status update
cte                | PATCH  /v1/transparent-encryption/clients/{id}/resetpassword                  | CTE/Clients                         | ResetPassword
cte                | DELETE /v1/transparent-encryption/compatibility-matrix                        | CTE/Clients                         | Delete
cte                | GET    /v1/transparent-encryption/compatibility-matrix                        | CTE/Clients                         | Get
cte                | POST   /v1/transparent-encryption/compatibility-matrix                        | CTE/Clients                         | Upload
cte                | GET    /v1/transparent-encryption/csigroups/                                  | CTE/CSIStorageGroups                | List
cte                | POST   /v1/transparent-encryption/csigroups/                                  | CTE/CSIStorageGroups                | Create
cte                | DELETE /v1/transparent-encryption/csigroups/guardpoints/{gp_id}               | CTE/CSIStorageGroups                | Remove GuardPolicy from CSI Storage Group
cte                | GET    /v1/transparent-encryption/csigroups/guardpoints/{gp_id}               | CTE/CSIStorageGroups                | Get GuardPolicy from Storage Group
cte                | PATCH  /v1/transparent-encryption/csigroups/guardpoints/{gp_id}               | CTE/CSIStorageGroups                | Update GuardPolicy in Storage Group
cte                | DELETE /v1/transparent-encryption/csigroups/{id}                              | CTE/CSIStorageGroups                | Delete
cte                | GET    /v1/transparent-encryption/csigroups/{id}                              | CTE/CSIStorageGroups                | Get
cte                | PATCH  /v1/transparent-encryption/csigroups/{id}                              | CTE/CSIStorageGroups                | Update
cte                | GET    /v1/transparent-encryption/csigroups/{id}/clients/                     | CTE/CSIStorageGroups                | List Clients in Storage Group
cte                | POST   /v1/transparent-encryption/csigroups/{id}/clients/                     | CTE/CSIStorageGroups                | Add Clients to Storage Group
cte                | DELETE /v1/transparent-encryption/csigroups/{id}/clients/{client_id}          | CTE/CSIStorageGroups                | Remove Client from Storage Group
cte                | GET    /v1/transparent-encryption/csigroups/{id}/clients/{client_id}          | CTE/CSIStorageGroups                | Get StorageGroup Client Association
cte                | GET    /v1/transparent-encryption/csigroups/{id}/guardpoints/                 | CTE/CSIStorageGroups                | List GuardPolicies in Storage Group
cte                | POST   /v1/transparent-encryption/csigroups/{id}/guardpoints/                 | CTE/CSIStorageGroups                | Add GuardPolicy to Storage Group
cte                | PATCH  /v1/transparent-encryption/fam/clients/{id}                            | CTE/File Activity Monitoring        | Update FAM Client
cte                | GET    /v1/transparent-encryption/fam/clients/{id}/attributes                 | CTE/File Activity Monitoring        | Get FAM Attributes
cte                | PATCH  /v1/transparent-encryption/fam/clients/{id}/attributes                 | CTE/File Activity Monitoring        | Update FAM Attributes
cte                | GET    /v1/transparent-encryption/fam/clients/{id}/policies/                  | CTE/File Activity Monitoring        | List FAM Policy associations
cte                | PATCH  /v1/transparent-encryption/fam/clients/{id}/policies/                  | CTE/File Activity Monitoring        | Bulk remove FAM Policies association from Client
cte                | POST   /v1/transparent-encryption/fam/clients/{id}/policies/                  | CTE/File Activity Monitoring        | Add Client-FAM Policies Association
cte                | DELETE /v1/transparent-encryption/fam/clients/{id}/policies/{policy_id}       | CTE/File Activity Monitoring        | Remove FAM Policy association from Client
cte                | PATCH  /v1/transparent-encryption/fam/clients/{id}/policies/{policy_id}       | CTE/File Activity Monitoring        | Update Client-FAM Policies Association
cte                | GET    /v1/transparent-encryption/fam/destination/                            | CTE/File Activity Monitoring        | List FAM Destination
cte                | POST   /v1/transparent-encryption/fam/destination/                            | CTE/File Activity Monitoring        | Create FAM Destination
cte                | DELETE /v1/transparent-encryption/fam/destination/{id}                        | CTE/File Activity Monitoring        | Delete FAM Destination
cte                | GET    /v1/transparent-encryption/fam/destination/{id}                        | CTE/File Activity Monitoring        | Get FAM Destination
cte                | PATCH  /v1/transparent-encryption/fam/destination/{id}                        | CTE/File Activity Monitoring        | Update FAM Destination
cte                | GET    /v1/transparent-encryption/fam/policies/                               | CTE/File Activity Monitoring        | List FAM Policies
cte                | POST   /v1/transparent-encryption/fam/policies/                               | CTE/File Activity Monitoring        | Create FAM Policy
cte                | DELETE /v1/transparent-encryption/fam/policies/{id}                           | CTE/File Activity Monitoring        | Delete FAM Policy
cte                | GET    /v1/transparent-encryption/fam/policies/{id}                           | CTE/File Activity Monitoring        | Get FAM Policy
cte                | PATCH  /v1/transparent-encryption/fam/policies/{id}                           | CTE/File Activity Monitoring        | Update FAM Policy
cte                | DELETE /v1/transparent-encryption/fam/policies/{id}/clients                   | CTE/File Activity Monitoring        | Remove FAM policy association from all the clients
cte                | GET    /v1/transparent-encryption/fam/policies/{policyId}/securityrules/      | CTE/File Activity Monitoring        | List Security Rules
cte                | POST   /v1/transparent-encryption/fam/policies/{policyId}/securityrules/      | CTE/File Activity Monitoring        | Create Security Rule
cte                | DELETE /v1/transparent-encryption/fam/policies/{policyId}/securityrules/{securityRuleId} | CTE/File Activity Monitoring        | Delete Security Rule
cte                | GET    /v1/transparent-encryption/fam/policies/{policyId}/securityrules/{securityRuleId} | CTE/File Activity Monitoring        | Get Security Rule
cte                | PATCH  /v1/transparent-encryption/fam/policies/{policyId}/securityrules/{securityRuleId} | CTE/File Activity Monitoring        | Update Security Rule
cte                | GET    /v1/transparent-encryption/ldtgroupcommservice/                        | CTE/LDTGroupCommServices            | List LDT Group Communication Service
cte                | POST   /v1/transparent-encryption/ldtgroupcommservice/                        | CTE/LDTGroupCommServices            | Create LDT Group Communication Service
cte                | DELETE /v1/transparent-encryption/ldtgroupcommservice/{id}                    | CTE/LDTGroupCommServices            | Delete LDT Group Communication Service
cte                | GET    /v1/transparent-encryption/ldtgroupcommservice/{id}                    | CTE/LDTGroupCommServices            | Get LDT Group Communication Service
cte                | PATCH  /v1/transparent-encryption/ldtgroupcommservice/{id}                    | CTE/LDTGroupCommServices            | Update LDT Group Communication Service
cte                | GET    /v1/transparent-encryption/ldtgroupcommservice/{id}/clients/           | CTE/LDTGroupCommServices            | List Clients in LDT Group Communication Service
cte                | POST   /v1/transparent-encryption/ldtgroupcommservice/{id}/clients/           | CTE/LDTGroupCommServices            | Add Client to LDT Group Communication Service
cte                | PATCH  /v1/transparent-encryption/ldtgroupcommservice/{id}/clients/delete/    | CTE/LDTGroupCommServices            | Delete Bulk Client from LDT Group Communication Service
cte                | DELETE /v1/transparent-encryption/ldtgroupcommservice/{id}/clients/{client_id} | CTE/LDTGroupCommServices            | Remove Client from LDT Group Communication Service
cte                | GET    /v1/transparent-encryption/ldtgroupcommservice/{id}/status-details/    | CTE/LDTGroupCommServices            | Get LDT Group Communication Service Status Details
cte                | GET    /v1/transparent-encryption/permissions                                 | CTE/Permissions                     | List
cte                | GET    /v1/transparent-encryption/policies/                                   | CTE/Policies                        | List
cte                | POST   /v1/transparent-encryption/policies/                                   | CTE/Policies                        | Create
cte                | DELETE /v1/transparent-encryption/policies/{id}                               | CTE/Policies                        | Delete
cte                | GET    /v1/transparent-encryption/policies/{id}                               | CTE/Policies                        | Get
cte                | PATCH  /v1/transparent-encryption/policies/{id}                               | CTE/Policies                        | Update
cte                | GET    /v1/transparent-encryption/policies/{id}/audits                        | CTE/Policies                        | Audit Records
cte                | GET    /v1/transparent-encryption/policies/{policyId}/datatxrules/            | CTE/Policies-DataTxRules            | List
cte                | POST   /v1/transparent-encryption/policies/{policyId}/datatxrules/            | CTE/Policies-DataTxRules            | Add
cte                | DELETE /v1/transparent-encryption/policies/{policyId}/datatxrules/{dataTxRuleId} | CTE/Policies-DataTxRules            | Delete
cte                | GET    /v1/transparent-encryption/policies/{policyId}/datatxrules/{dataTxRuleId} | CTE/Policies-DataTxRules            | Get
cte                | PATCH  /v1/transparent-encryption/policies/{policyId}/datatxrules/{dataTxRuleId} | CTE/Policies-DataTxRules            | Update
cte                | GET    /v1/transparent-encryption/policies/{policyId}/idtkeyrules/            | CTE/Policies-IDTRules               | List
cte                | GET    /v1/transparent-encryption/policies/{policyId}/idtkeyrules/{idtRuleId} | CTE/Policies-IDTRules               | Get
cte                | PATCH  /v1/transparent-encryption/policies/{policyId}/idtkeyrules/{idtRuleId} | CTE/Policies-IDTRules               | Update
cte                | GET    /v1/transparent-encryption/policies/{policyId}/keyrules/               | CTE/Policies-KeyRules               | List
cte                | POST   /v1/transparent-encryption/policies/{policyId}/keyrules/               | CTE/Policies-KeyRules               | Add
cte                | DELETE /v1/transparent-encryption/policies/{policyId}/keyrules/{keyRuleId}    | CTE/Policies-KeyRules               | Delete
cte                | GET    /v1/transparent-encryption/policies/{policyId}/keyrules/{keyRuleId}    | CTE/Policies-KeyRules               | Get
cte                | PATCH  /v1/transparent-encryption/policies/{policyId}/keyrules/{keyRuleId}    | CTE/Policies-KeyRules               | Update
cte                | GET    /v1/transparent-encryption/policies/{policyId}/ldtkeyrules/            | CTE/Policies-LDTRules               | List
cte                | POST   /v1/transparent-encryption/policies/{policyId}/ldtkeyrules/            | CTE/Policies-LDTRules               | Add
cte                | DELETE /v1/transparent-encryption/policies/{policyId}/ldtkeyrules/{ldtRuleId} | CTE/Policies-LDTRules               | Delete
cte                | GET    /v1/transparent-encryption/policies/{policyId}/ldtkeyrules/{ldtRuleId} | CTE/Policies-LDTRules               | Get
cte                | PATCH  /v1/transparent-encryption/policies/{policyId}/ldtkeyrules/{ldtRuleId} | CTE/Policies-LDTRules               | Update
cte                | GET    /v1/transparent-encryption/policies/{policyId}/securityrules/          | CTE/Policies-SecurityRules          | List
cte                | POST   /v1/transparent-encryption/policies/{policyId}/securityrules/          | CTE/Policies-SecurityRules          | Add
cte                | DELETE /v1/transparent-encryption/policies/{policyId}/securityrules/{securityRuleId} | CTE/Policies-SecurityRules          | Delete
cte                | GET    /v1/transparent-encryption/policies/{policyId}/securityrules/{securityRuleId} | CTE/Policies-SecurityRules          | Get
cte                | PATCH  /v1/transparent-encryption/policies/{policyId}/securityrules/{securityRuleId} | CTE/Policies-SecurityRules          | Update
cte                | GET    /v1/transparent-encryption/policies/{policyId}/signaturerules          | CTE/Policies-SignatureRules         | List
cte                | POST   /v1/transparent-encryption/policies/{policyId}/signaturerules          | CTE/Policies-SignatureRules         | Add Signature Rule
cte                | DELETE /v1/transparent-encryption/policies/{policyId}/signaturerules/{signatureRuleId} | CTE/Policies-SignatureRules         | Delete
cte                | GET    /v1/transparent-encryption/policies/{policyId}/signaturerules/{signatureRuleId} | CTE/Policies-SignatureRules         | Get
cte                | PATCH  /v1/transparent-encryption/policies/{policyId}/signaturerules/{signatureRuleId} | CTE/Policies-SignatureRules         | Update
cte                | GET    /v1/transparent-encryption/processsets/                                | CTE/ProcessSets                     | List
cte                | POST   /v1/transparent-encryption/processsets/                                | CTE/ProcessSets                     | Create
cte                | DELETE /v1/transparent-encryption/processsets/{id}                            | CTE/ProcessSets                     | Delete
cte                | GET    /v1/transparent-encryption/processsets/{id}                            | CTE/ProcessSets                     | Get
cte                | PATCH  /v1/transparent-encryption/processsets/{id}                            | CTE/ProcessSets                     | Update
cte                | PATCH  /v1/transparent-encryption/processsets/{id}/addprocesses               | CTE/ProcessSets                     | Update
cte                | DELETE /v1/transparent-encryption/processsets/{id}/delprocesses               | CTE/ProcessSets                     | Delete
cte                | GET    /v1/transparent-encryption/processsets/{id}/policies                   | CTE/ProcessSets                     | List
cte                | GET    /v1/transparent-encryption/processsets/{id}/processes                  | CTE/ProcessSets                     | List
cte                | PATCH  /v1/transparent-encryption/processsets/{id}/updateprocess/{processIndex} | CTE/ProcessSets                     | Update
cte                | GET    /v1/transparent-encryption/profiles/                                   | CTE/Profiles                        | List
cte                | POST   /v1/transparent-encryption/profiles/                                   | CTE/Profiles                        | Create
cte                | DELETE /v1/transparent-encryption/profiles/{id}                               | CTE/Profiles                        | Delete
cte                | GET    /v1/transparent-encryption/profiles/{id}                               | CTE/Profiles                        | Get
cte                | PATCH  /v1/transparent-encryption/profiles/{id}                               | CTE/Profiles                        | Update
cte                | DELETE /v1/transparent-encryption/profiles/{id}/syslogserver/{name}           | CTE/Profiles                        | Delete
cte                | GET    /v1/transparent-encryption/query-capabilities                          | CTE/Clients                         | Get latest client capabilities
cte                | GET    /v1/transparent-encryption/reports/clients-guard-status/               | CTE/Reports                         | Get
cte                | GET    /v1/transparent-encryption/reports/clients-guard-status/download/      | CTE/Reports                         | Download Report
cte                | GET    /v1/transparent-encryption/reports/clients-keys/                       | CTE/Reports                         | Get
cte                | GET    /v1/transparent-encryption/reports/clients-keys/download/              | CTE/Reports                         | Download Report
cte                | GET    /v1/transparent-encryption/reports/clients-policies/                   | CTE/Reports                         | Get
cte                | GET    /v1/transparent-encryption/reports/clients-policies/download/          | CTE/Reports                         | Download Report
cte                | GET    /v1/transparent-encryption/reports/clients-profiles/                   | CTE/Reports                         | Get
cte                | GET    /v1/transparent-encryption/reports/clients-profiles/download/          | CTE/Reports                         | Download Report
cte                | GET    /v1/transparent-encryption/reports/clients/                            | CTE/Reports                         | Get
cte                | GET    /v1/transparent-encryption/reports/clients/download/                   | CTE/Reports                         | Download Report
cte                | GET    /v1/transparent-encryption/reports/guardpoints/                        | CTE/Reports                         | Get
cte                | GET    /v1/transparent-encryption/reports/guardpoints/download/               | CTE/Reports                         | Download Report
cte                | GET    /v1/transparent-encryption/reports/policies-keys/                      | CTE/Reports                         | Get
cte                | GET    /v1/transparent-encryption/reports/policies-keys/download/             | CTE/Reports                         | Download Report
cte                | GET    /v1/transparent-encryption/resourcesets/                               | CTE/ResourceSets                    | List
cte                | POST   /v1/transparent-encryption/resourcesets/                               | CTE/ResourceSets                    | Create
cte                | DELETE /v1/transparent-encryption/resourcesets/{id}                           | CTE/ResourceSets                    | Delete
cte                | GET    /v1/transparent-encryption/resourcesets/{id}                           | CTE/ResourceSets                    | Get
cte                | PATCH  /v1/transparent-encryption/resourcesets/{id}                           | CTE/ResourceSets                    | Update
cte                | PATCH  /v1/transparent-encryption/resourcesets/{id}/addresources              | CTE/ResourceSets                    | Update
cte                | DELETE /v1/transparent-encryption/resourcesets/{id}/delresources              | CTE/ResourceSets                    | Delete
cte                | GET    /v1/transparent-encryption/resourcesets/{id}/policies                  | CTE/ResourceSets                    | List
cte                | GET    /v1/transparent-encryption/resourcesets/{id}/resources                 | CTE/ResourceSets                    | List
cte                | PATCH  /v1/transparent-encryption/resourcesets/{id}/updateresource/{resourceIndex} | CTE/ResourceSets                    | Update
cte                | GET    /v1/transparent-encryption/signaturesets/                              | CTE/SignatureSets                   | List
cte                | POST   /v1/transparent-encryption/signaturesets/                              | CTE/SignatureSets                   | Create
cte                | DELETE /v1/transparent-encryption/signaturesets/{id}                          | CTE/SignatureSets                   | Delete
cte                | GET    /v1/transparent-encryption/signaturesets/{id}                          | CTE/SignatureSets                   | Get
cte                | PATCH  /v1/transparent-encryption/signaturesets/{id}                          | CTE/SignatureSets                   | Update
cte                | POST   /v1/transparent-encryption/signaturesets/{id}/cancelsignapp/           | CTE/SignatureSets                   | Cancel Sign Request
cte                | POST   /v1/transparent-encryption/signaturesets/{id}/querysignapp/            | CTE/SignatureSets                   | Query Sign Request.
cte                | POST   /v1/transparent-encryption/signaturesets/{id}/signapp/                 | CTE/SignatureSets                   | Send Sign Request
cte                | PATCH  /v1/transparent-encryption/signaturesets/{signatureSetId}/addsignatures/ | CTE/SignatureSets                   | Update
cte                | PATCH  /v1/transparent-encryption/signaturesets/{signatureSetId}/delete-sources/ | CTE/SignatureSets                   | Update
cte                | GET    /v1/transparent-encryption/signaturesets/{signatureSetId}/signatures/  | CTE/SignatureSets                   | List
cte                | POST   /v1/transparent-encryption/signaturesets/{signatureSetId}/signatures/upload-list | CTE/SignatureSets                   | Upload
cte                | DELETE /v1/transparent-encryption/signaturesets/{signatureSetId}/signatures/{signatureId} | CTE/SignatureSets                   | Delete
cte                | POST   /v1/transparent-encryption/signaturesets/{signatureSetId}/upload-yaml  | CTE/SignatureSets                   | Upload YAML
cte                | POST   /v1/transparent-encryption/unenroll/                                   | CTE/Clients                         | Unenrolls a client from the CipherTrust Manager.
cte                | GET    /v1/transparent-encryption/usersets/                                   | CTE/UserSets                        | List
cte                | POST   /v1/transparent-encryption/usersets/                                   | CTE/UserSets                        | Create
cte                | DELETE /v1/transparent-encryption/usersets/{id}                               | CTE/UserSets                        | Delete
cte                | GET    /v1/transparent-encryption/usersets/{id}                               | CTE/UserSets                        | Get
cte                | PATCH  /v1/transparent-encryption/usersets/{id}                               | CTE/UserSets                        | Update
cte                | PATCH  /v1/transparent-encryption/usersets/{id}/addusers                      | CTE/UserSets                        | Update
cte                | DELETE /v1/transparent-encryption/usersets/{id}/delusers                      | CTE/UserSets                        | Delete
cte                | GET    /v1/transparent-encryption/usersets/{id}/policies                      | CTE/UserSets                        | List
cte                | PATCH  /v1/transparent-encryption/usersets/{id}/updateuser/{userIndex}        | CTE/UserSets                        | Update
cte                | GET    /v1/transparent-encryption/usersets/{id}/users                         | CTE/UserSets                        | List
cte                | POST   /v1/transparent-encryption/validatecosparams/                          | CTE/CloudObjectStorage              | Validate Cloud Object Storage
data-protection    | POST   /v1/crypto/decrypt                                                     | Crypto                              | Decrypt
data-protection    | POST   /v1/crypto/decryptonite                                                | Crypto                              | Decryptonite
data-protection    | POST   /v1/crypto/encrypt                                                     | Crypto                              | Encrypt
data-protection    | POST   /v1/crypto/encryptonite                                                | Crypto                              | Encryptonite
data-protection    | POST   /v1/crypto/hash                                                        | Crypto                              | Generate Hash
data-protection    | POST   /v1/crypto/hide2                                                       | Crypto                              | Format-preserving encrypt
data-protection    | POST   /v1/crypto/mac                                                         | Crypto                              | MAC
data-protection    | POST   /v1/crypto/macv                                                        | Crypto                              | MAC Verify
data-protection    | POST   /v1/crypto/reencrypt                                                   | Crypto                              | Reencrypt
data-protection    | POST   /v1/crypto/sign                                                        | Crypto                              | Sign
data-protection    | POST   /v1/crypto/signv                                                       | Crypto                              | Sign Verify
data-protection    | POST   /v1/crypto/unhide2                                                     | Crypto                              | Format-preserving decrypt
data-protection    | GET    /v1/data-protection/access-policies                                    | Data Protection/Access Policies     | List
data-protection    | POST   /v1/data-protection/access-policies                                    | Data Protection/Access Policies     | Create
data-protection    | DELETE /v1/data-protection/access-policies/{id}                               | Data Protection/Access Policies     | Delete
data-protection    | GET    /v1/data-protection/access-policies/{id}                               | Data Protection/Access Policies     | Get
data-protection    | PATCH  /v1/data-protection/access-policies/{id}                               | Data Protection/Access Policies     | Update
data-protection    | PATCH  /v1/data-protection/access-policies/{id}/error-replacement-value-null  | Data Protection/Access Policies     | Update
data-protection    | POST   /v1/data-protection/access-policies/{id}/user-set                      | Data Protection/Access Policies     | Add User-Set
data-protection    | DELETE /v1/data-protection/access-policies/{id}/user-set/{userSetID}          | Data Protection/Access Policies     | Remove user set
data-protection    | PATCH  /v1/data-protection/access-policies/{id}/user-set/{userSetID}          | Data Protection/Access Policies     | Updates the user set
data-protection    | PATCH  /v1/data-protection/access-policies/{id}/user-set/{userSetID}/error-replacement-value-null | Data Protection/Access Policies     | Update
data-protection    | GET    /v1/data-protection/bdt-policies                                       | BDT/Policies                        | List
data-protection    | POST   /v1/data-protection/bdt-policies                                       | BDT/Policies                        | Create
data-protection    | DELETE /v1/data-protection/bdt-policies/{id}                                  | BDT/Policies                        | Delete
data-protection    | GET    /v1/data-protection/bdt-policies/{id}                                  | BDT/Policies                        | Get
data-protection    | PATCH  /v1/data-protection/bdt-policies/{id}                                  | BDT/Policies                        | Update
data-protection    | GET    /v1/data-protection/bdt-policies/{id}/tables                           | BDT/Policies                        | List
data-protection    | POST   /v1/data-protection/bdt-policies/{id}/tables                           | BDT/Policies                        | Create
data-protection    | DELETE /v1/data-protection/bdt-policies/{id}/tables/{tableId}                 | BDT/Policies                        | Delete
data-protection    | PATCH  /v1/data-protection/bdt-policies/{id}/tables/{tableId}                 | BDT/Policies                        | Update
data-protection    | GET    /v1/data-protection/bdt-policies/{id}/tables/{tableId}/columns         | BDT/Policies                        | List
data-protection    | POST   /v1/data-protection/bdt-policies/{id}/tables/{tableId}/columns         | BDT/Policies                        | Create
data-protection    | DELETE /v1/data-protection/bdt-policies/{id}/tables/{tableId}/columns/{columnId} | BDT/Policies                        | Delete
data-protection    | PATCH  /v1/data-protection/bdt-policies/{id}/tables/{tableId}/columns/{columnId} | BDT/Policies                        | Update
data-protection    | GET    /v1/data-protection/bdt/job-configurations                             | Data Protection/BDT Job Configurations | List
data-protection    | POST   /v1/data-protection/bdt/job-configurations                             | Data Protection/BDT Job Configurations | Create
data-protection    | DELETE /v1/data-protection/bdt/job-configurations/{id}                        | Data Protection/BDT Job Configurations | Delete
data-protection    | GET    /v1/data-protection/bdt/job-configurations/{id}                        | Data Protection/BDT Job Configurations | Get
data-protection    | PATCH  /v1/data-protection/bdt/job-configurations/{id}                        | Data Protection/BDT Job Configurations | Update
data-protection    | POST   /v1/data-protection/bdt/job-configurations/{id}/run                    | Data Protection/BDT Job Configurations | Run Job
data-protection    | GET    /v1/data-protection/bdt/job-configurations/{id}/tables                 | Data Protection/BDT Job Configurations | List
data-protection    | POST   /v1/data-protection/bdt/job-configurations/{id}/tables                 | Data Protection/BDT Job Configurations | Create
data-protection    | DELETE /v1/data-protection/bdt/job-configurations/{id}/tables/{tableID}       | Data Protection/BDT Job Configurations | Delete
data-protection    | PATCH  /v1/data-protection/bdt/job-configurations/{id}/tables/{tableID}       | Data Protection/BDT Job Configurations | Update
data-protection    | GET    /v1/data-protection/bdt/job-configurations/{id}/tables/{tableID}/columns | Data Protection/BDT Job Configurations | List
data-protection    | POST   /v1/data-protection/bdt/job-configurations/{id}/tables/{tableID}/columns | Data Protection/BDT Job Configurations | Create
data-protection    | DELETE /v1/data-protection/bdt/job-configurations/{id}/tables/{tableID}/columns/{columnID} | Data Protection/BDT Job Configurations | Delete
data-protection    | PATCH  /v1/data-protection/bdt/job-configurations/{id}/tables/{tableID}/columns/{columnID} | Data Protection/BDT Job Configurations | Update
data-protection    | GET    /v1/data-protection/character-sets                                     | Data Protection/Character Sets      | List
data-protection    | POST   /v1/data-protection/character-sets                                     | BDT/Character Sets                  | Create
data-protection    | DELETE /v1/data-protection/character-sets/{id}                                | BDT/Character Sets                  | Delete
data-protection    | GET    /v1/data-protection/character-sets/{id}                                | Data Protection/Character Sets      | Get
data-protection    | PATCH  /v1/data-protection/character-sets/{id}                                | BDT/Character Sets                  | Update
data-protection    | GET    /v1/data-protection/client-profiles                                    | Data Protection/Client Profiles     | List
data-protection    | POST   /v1/data-protection/client-profiles                                    | Data Protection/Client Profiles     | Create
data-protection    | GET    /v1/data-protection/client-profiles/count                              | Data Protection/Client Profiles     | Summary
data-protection    | DELETE /v1/data-protection/client-profiles/{id}                               | Data Protection/Client Profiles     | Delete
data-protection    | GET    /v1/data-protection/client-profiles/{id}                               | Data Protection/Client Profiles     | Get
data-protection    | PATCH  /v1/data-protection/client-profiles/{id}                               | Data Protection/Client Profiles     | Update
data-protection    | DELETE /v1/data-protection/client-profiles/{id}/clean                         | Data Protection/Client Profiles     | Clean
data-protection    | GET    /v1/data-protection/clients/                                           | Data Protection/Clients             | List
data-protection    | POST   /v1/data-protection/clients/                                           | Data Protection/Clients             | Register
data-protection    | GET    /v1/data-protection/clients/count                                      | Data Protection/Clients             | Summary
data-protection    | DELETE /v1/data-protection/clients/{id}                                       | Data Protection/Clients             | Delete
data-protection    | GET    /v1/data-protection/clients/{id}                                       | Data Protection/Clients             | Get
data-protection    | GET    /v1/data-protection/containers                                         | BDT/Containers                      | List
data-protection    | POST   /v1/data-protection/containers                                         | BDT/Containers                      | Create
data-protection    | DELETE /v1/data-protection/containers/{id}                                    | BDT/Containers                      | Delete
data-protection    | GET    /v1/data-protection/containers/{id}                                    | BDT/Containers                      | Get
data-protection    | PATCH  /v1/data-protection/containers/{id}                                    | BDT/Containers                      | Update
data-protection    | GET    /v1/data-protection/data-sources                                       | Data Protection/Data Sources        | List
data-protection    | POST   /v1/data-protection/data-sources                                       | Data Protection/Data Sources        | Create
data-protection    | DELETE /v1/data-protection/data-sources/{id}                                  | Data Protection/Data Sources        | Delete
data-protection    | GET    /v1/data-protection/data-sources/{id}                                  | Data Protection/Data Sources        | Get
data-protection    | PATCH  /v1/data-protection/data-sources/{id}                                  | Data Protection/Data Sources        | Update
data-protection    | GET    /v1/data-protection/dpg-policies                                       | Data Protection/DPG Policies        | List
data-protection    | POST   /v1/data-protection/dpg-policies                                       | Data Protection/DPG Policies        | Create
data-protection    | DELETE /v1/data-protection/dpg-policies/{id}                                  | Data Protection/DPG Policies        | Delete
data-protection    | GET    /v1/data-protection/dpg-policies/{id}                                  | Data Protection/DPG Policies        | Get
data-protection    | PATCH  /v1/data-protection/dpg-policies/{id}                                  | Data Protection/DPG Policies        | Update
data-protection    | GET    /v1/data-protection/dpg-policies/{id}/api-urls                         | Data Protection/DPG Policies        | List
data-protection    | POST   /v1/data-protection/dpg-policies/{id}/api-urls                         | Data Protection/DPG Policies        | Create
data-protection    | DELETE /v1/data-protection/dpg-policies/{id}/api-urls/{apiUrlId}              | Data Protection/DPG Policies        | Delete
data-protection    | GET    /v1/data-protection/dpg-policies/{id}/api-urls/{apiUrlId}              | Data Protection/DPG Policies        | Get
data-protection    | PATCH  /v1/data-protection/dpg-policies/{id}/api-urls/{apiUrlId}              | Data Protection/DPG Policies        | Update
data-protection    | GET    /v1/data-protection/jobs                                               | Data Protection/Jobs                | List
data-protection    | DELETE /v1/data-protection/jobs/{id}                                          | Data Protection/Jobs                | Delete
data-protection    | GET    /v1/data-protection/jobs/{id}                                          | Data Protection/Jobs                | Get
data-protection    | GET    /v1/data-protection/masking-formats                                    | Data Protection/Masking Formats     | List
data-protection    | POST   /v1/data-protection/masking-formats                                    | Data Protection/Masking Formats     | Create
data-protection    | DELETE /v1/data-protection/masking-formats/{id}                               | Data Protection/Masking Formats     | Delete
data-protection    | GET    /v1/data-protection/masking-formats/{id}                               | Data Protection/Masking Formats     | Get
data-protection    | PATCH  /v1/data-protection/masking-formats/{id}                               | Data Protection/Masking Formats     | Update
data-protection    | GET    /v1/data-protection/protection-policies                                | Data Protection/Protection Policies | List
data-protection    | POST   /v1/data-protection/protection-policies                                | Data Protection/Protection Policies | Create
data-protection    | DELETE /v1/data-protection/protection-policies/{name}                         | Data Protection/Protection Policies | Delete
data-protection    | GET    /v1/data-protection/protection-policies/{name}                         | Data Protection/Protection Policies | Get
data-protection    | PATCH  /v1/data-protection/protection-policies/{name}                         | Data Protection/Protection Policies | Update
data-protection    | GET    /v1/data-protection/protection-profiles                                | BDT/Protection Profiles             | List
data-protection    | POST   /v1/data-protection/protection-profiles                                | BDT/Protection Profiles             | Create
data-protection    | DELETE /v1/data-protection/protection-profiles/{id}                           | BDT/Protection Profiles             | Delete
data-protection    | GET    /v1/data-protection/protection-profiles/{id}                           | BDT/Protection Profiles             | Get
data-protection    | PATCH  /v1/data-protection/protection-profiles/{id}                           | BDT/Protection Profiles             | Update
data-protection    | GET    /v1/data-protection/user-sets                                          | Data Protection/User Sets           | List
data-protection    | POST   /v1/data-protection/user-sets                                          | Data Protection/User Sets           | Create
data-protection    | DELETE /v1/data-protection/user-sets/{id}                                     | Data Protection/User Sets           | Delete
data-protection    | GET    /v1/data-protection/user-sets/{id}                                     | Data Protection/User Sets           | Get
data-protection    | PATCH  /v1/data-protection/user-sets/{id}                                     | Data Protection/User Sets           | Update
data-protection    | DELETE /v1/data-protection/user-sets/{id}/users                               | Data Protection/User Sets           | Remove Users
data-protection    | GET    /v1/data-protection/user-sets/{id}/users                               | Data Protection/User Sets           | List
data-protection    | POST   /v1/data-protection/user-sets/{id}/users                               | Data Protection/User Sets           | Add Users
data-protection    | PATCH  /v1/data-protection/user-sets/{id}/users/{user}                        | Data Protection/User Sets           | Modify Username
data-protection    | GET    /v1/vault/random                                                       | Crypto                              | Random
ddc                | GET    /v1/ddc/active-node/info                                               | DDC                                 | Retrieve information about the DDC active node
ddc                | POST   /v1/ddc/active-node/register                                           | DDC                                 | Registers a node as ddc active node
ddc                | GET    /v1/ddc/agents                                                         | DDC/Agent                           | List all
ddc                | GET    /v1/ddc/agents/{id}                                                    | DDC/Agent                           | Get
ddc                | PUT    /v1/ddc/agents/{id}                                                    | DDC/Agent                           | Update
ddc                | GET    /v1/ddc/classification-profiles                                        | DDC/ClassificationProfile           | List all
ddc                | POST   /v1/ddc/classification-profiles                                        | DDC/ClassificationProfile           | Create
ddc                | DELETE /v1/ddc/classification-profiles/{id}                                   | DDC/ClassificationProfile           | Delete
ddc                | GET    /v1/ddc/classification-profiles/{id}                                   | DDC/ClassificationProfile           | Get
ddc                | PUT    /v1/ddc/classification-profiles/{id}                                   | DDC/ClassificationProfile           | Update
ddc                | POST   /v1/ddc/classification-profiles/{id}/clone                             | DDC/ClassificationProfile           | Clone
ddc                | DELETE /v1/ddc/clean-resources/targets                                        | DDC                                 | Delete targets
ddc                | GET    /v1/ddc/clean-resources/targets/{processID}                            | DDC                                 | Get delete targets process status
ddc                | GET    /v1/ddc/config-profiles                                                | DDC/ConfigProfile                   | List all
ddc                | POST   /v1/ddc/config-profiles                                                | DDC/ConfigProfile                   | Create
ddc                | DELETE /v1/ddc/config-profiles/{id}                                           | DDC/ConfigProfile                   | Delete
ddc                | GET    /v1/ddc/config-profiles/{id}                                           | DDC/ConfigProfile                   | Get
ddc                | PUT    /v1/ddc/config-profiles/{id}                                           | DDC/ConfigProfile                   | Update
ddc                | GET    /v1/ddc/datastores                                                     | DDC/DataStore                       | List all
ddc                | POST   /v1/ddc/datastores                                                     | DDC/DataStore                       | Create
ddc                | POST   /v1/ddc/datastores/amazon-s3                                           | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/amazon-s3/{id}                                      | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/azure-blob                                          | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/azure-blob/{id}                                     | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/azure-table                                         | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/azure-table/{id}                                    | DDC/DataStore                       | Update
ddc                | GET    /v1/ddc/datastores/browse-target-path/{processID}                      | DDC/DataStore                       | Get
ddc                | GET    /v1/ddc/datastores/by-type                                             | DDC/DataStore                       | List
ddc                | GET    /v1/ddc/datastores/connection-test/{processID}                         | DDC/DataStore                       | Get
ddc                | POST   /v1/ddc/datastores/exchange-server                                     | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/exchange-server/{id}                                | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/google-drive                                        | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/google-drive/{id}                                   | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/google-mail                                         | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/google-mail/{id}                                    | DDC/DataStore                       | Update
ddc                | GET    /v1/ddc/datastores/group-by-type                                       | DDC/DataStore                       | List
ddc                | POST   /v1/ddc/datastores/hadoop-cluster                                      | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/hadoop-cluster/{id}                                 | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/ibm-db2                                             | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/ibm-db2/{id}                                        | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/local-storage                                       | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/local-storage/{id}                                  | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/microsoft-sql-db                                    | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/microsoft-sql-db/{id}                               | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/mongo-db                                            | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/mongo-db/{id}                                       | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/mysql-db                                            | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/mysql-db/{id}                                       | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/office365-exchange-online                           | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/office365-exchange-online/{id}                      | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/office365-onedrive-business                         | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/office365-onedrive-business/{id}                    | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/office365-sharepoint-online                         | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/office365-sharepoint-online/{id}                    | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/oracle-db                                           | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/oracle-db/{id}                                      | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/postgresql-db                                       | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/postgresql-db/{id}                                  | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/salesforce                                          | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/salesforce/{id}                                     | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/sap-hana-db                                         | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/sap-hana-db/{id}                                    | DDC/DataStore                       | Update
ddc                | GET    /v1/ddc/datastores/scanned                                             | DDC/DataStore                       | Get
ddc                | GET    /v1/ddc/datastores/sensitive-percentage                                | DDC/DataStore                       | Get
ddc                | POST   /v1/ddc/datastores/sharepoint-server                                   | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/sharepoint-server/{id}                              | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/teradata-db                                         | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/teradata-db/{id}                                    | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/unix-file-share                                     | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/unix-file-share/{id}                                | DDC/DataStore                       | Update
ddc                | POST   /v1/ddc/datastores/windows-share                                       | DDC/DataStore                       | Create
ddc                | PUT    /v1/ddc/datastores/windows-share/{id}                                  | DDC/DataStore                       | Update
ddc                | DELETE /v1/ddc/datastores/{id}                                                | DDC/DataStore                       | Delete
ddc                | GET    /v1/ddc/datastores/{id}                                                | DDC/DataStore                       | Get
ddc                | PUT    /v1/ddc/datastores/{id}                                                | DDC/DataStore                       | Update
ddc                | GET    /v1/ddc/datastores/{id}/agent-search                                   | DDC/DataStore                       | Get
ddc                | GET    /v1/ddc/datastores/{id}/browse-target-path                             | DDC/DataStore                       | Get
ddc                | GET    /v1/ddc/datastores/{id}/connection-test                                | DDC/DataStore                       | Get
ddc                | PUT    /v1/ddc/datastores/{id}/status                                         | DDC/DataStore                       | Update
ddc                | GET    /v1/ddc/license/allowance                                              | DDC                                 | Returns data allowance total and consumed
ddc                | GET    /v1/ddc/ml-agents                                                      | DDC/Agent                           | List all
ddc                | GET    /v1/ddc/ml-agents/{id}                                                 | DDC/Agent                           | Get
ddc                | PUT    /v1/ddc/ml-agents/{id}                                                 | DDC/Agent                           | Update
ddc                | GET    /v1/ddc/ml-agents/{id}/config-profile                                  | DDC/Agent                           | Get
ddc                | GET    /v1/ddc/provisioned/countries                                          | DDC                                 | List all
ddc                | GET    /v1/ddc/provisioned/states                                             | DDC                                 | List all
ddc                | POST   /v1/ddc/raw-data/decrypt                                               | DDC                                 | Decrypt raw data file
ddc                | GET    /v1/ddc/report-template                                                | DDC/ReportTemplate                  | List all
ddc                | POST   /v1/ddc/report-template                                                | DDC/ReportTemplate                  | Create
ddc                | POST   /v1/ddc/report-template/scan/aggregated                                | DDC/ReportTemplate                  | Create
ddc                | POST   /v1/ddc/report-template/scan/trend                                     | DDC/ReportTemplate                  | Create
ddc                | DELETE /v1/ddc/report-template/{id}                                           | DDC/ReportTemplate                  | Delete
ddc                | GET    /v1/ddc/report-template/{id}                                           | DDC/ReportTemplate                  | Get
ddc                | PUT    /v1/ddc/report-template/{id}/auto-generate                             | DDC/ReportTemplate                  | Update
ddc                | POST   /v1/ddc/report-template/{id}/run                                       | DDC/ReportTemplate                  | Run Report Template
ddc                | GET    /v1/ddc/reports                                                        | DDC/Report                          | List all
ddc                | GET    /v1/ddc/reports/dynamic/data-objects/{id}/report                       | DDC/Report                          | List All.
ddc                | GET    /v1/ddc/reports/dynamic/data-objects/{id}/status                       | DDC/Report                          | Get dynamic query report status.
ddc                | GET    /v1/ddc/reports/{id}                                                   | DDC/Report                          | Get the report info
ddc                | GET    /v1/ddc/reports/{id}/data-objects/details                              | DDC/Report                          | List All.
ddc                | GET    /v1/ddc/reports/{id}/data-objects/export                               | DDC/Report                          | List All.
ddc                | GET    /v1/ddc/reports/{id}/data-objects/summary                              | DDC/Report                          | Get all data objects summary
ddc                | GET    /v1/ddc/reports/{id}/datastores/details                                | DDC/Report                          | List All.
ddc                | POST   /v1/ddc/reports/{id}/dynamic/data-objects                              | DDC/Report                          | Create new dynamic query for data objects
ddc                | GET    /v1/ddc/reports/{id}/inaccessible-data-objects/details                 | DDC/Report                          | List All.
ddc                | GET    /v1/ddc/reports/{id}/inaccessible-data-objects/export                  | DDC/Report                          | List All.
ddc                | GET    /v1/ddc/reports/{id}/infotypes/summary                                 | DDC/Report                          | Get all infotypes summary
ddc                | GET    /v1/ddc/reports/{id}/scans/details                                     | DDC/Report                          | List All.
ddc                | GET    /v1/ddc/reports/{id}/summary                                           | DDC/Report                          | Get summary
ddc                | GET    /v1/ddc/retention-policy/executions                                    | DDC                                 | Get
ddc                | GET    /v1/ddc/retention-policy/executions/{id}                               | DDC                                 | Get
ddc                | GET    /v1/ddc/scan-executions                                                | DDC/ScanExecutions                  | List all
ddc                | GET    /v1/ddc/scan-trend-reports/{id}                                        | DDC/Report                          | Get the scan trend report info
ddc                | GET    /v1/ddc/scan-trend-reports/{id}/average-risk-trend                     | DDC/Report                          | Get the data objects average risk
ddc                | GET    /v1/ddc/scan-trend-reports/{id}/data-objects-trend                     | DDC/Report                          | Get the data objects info trend
ddc                | GET    /v1/ddc/scan-trend-reports/{id}/data-objects/details/{scanExecutionId} | DDC/Report                          | List All.
ddc                | GET    /v1/ddc/scan-trend-reports/{id}/infotypes-trend                        | DDC/Report                          | Get the infotypes info trend
ddc                | GET    /v1/ddc/scans                                                          | DDC/Scan                            | List All
ddc                | POST   /v1/ddc/scans                                                          | DDC/Scan                            | Create
ddc                | GET    /v1/ddc/scans/executed-scans                                           | DDC/Scan                            | Get
ddc                | GET    /v1/ddc/scans/scan-executions/troubleshooting-export/{id}/result       | DDC/Scan                            | Get troubleshooting info.
ddc                | GET    /v1/ddc/scans/scan-executions/troubleshooting-export/{id}/status       | DDC/Scan                            | Get troubleshooting info.
ddc                | GET    /v1/ddc/scans/scan-executions/{id}/datastores-progress                 | DDC/Scan                            | Get
ddc                | GET    /v1/ddc/scans/scan-executions/{id}/scan-trace-log/export               | DDC/Scan                            | List scan trace logs.
ddc                | GET    /v1/ddc/scans/scan-executions/{id}/troubleshooting-export              | DDC/Scan                            | Get troubleshooting info.
ddc                | GET    /v1/ddc/scans/sensitive-objects                                        | DDC/Scan                            | Get
ddc                | GET    /v1/ddc/scans/sensitive-scans                                          | DDC/Scan                            | Get
ddc                | POST   /v1/ddc/scans/validate-filter                                          | DDC/Scan                            | Validate the scan filter
ddc                | DELETE /v1/ddc/scans/{id}                                                     | DDC/Scan                            | Delete
ddc                | GET    /v1/ddc/scans/{id}                                                     | DDC/Scan                            | Get
ddc                | PUT    /v1/ddc/scans/{id}                                                     | DDC/Scan                            | Update
ddc                | POST   /v1/ddc/scans/{id}/disable                                             | DDC/Scan                            | Post
ddc                | POST   /v1/ddc/scans/{id}/enable                                              | DDC/Scan                            | Post
ddc                | POST   /v1/ddc/scans/{id}/pause                                               | DDC/Scan                            | Post
ddc                | POST   /v1/ddc/scans/{id}/resume                                              | DDC/Scan                            | Post
ddc                | POST   /v1/ddc/scans/{id}/run_now                                             | DDC/Scan                            | Post
ddc                | POST   /v1/ddc/scans/{id}/stop                                                | DDC/Scan                            | Post
ddc                | GET    /v1/ddc/server-statistics/disk-usage                                   | DDC                                 | Get server disk usage
ddc                | GET    /v1/ddc/similarity-searches                                            | DDC/SimilaritySearch                | List all
ddc                | POST   /v1/ddc/similarity-searches                                            | DDC/SimilaritySearch                | Create
ddc                | DELETE /v1/ddc/similarity-searches/{id}                                       | DDC/SimilaritySearch                | Delete
ddc                | GET    /v1/ddc/similarity-searches/{id}                                       | DDC/SimilaritySearch                | Get
ddc                | PUT    /v1/ddc/similarity-searches/{id}                                       | DDC/SimilaritySearch                | Update
ddc                | GET    /v1/ddc/similarity-searches/{id}/data-objects                          | DDC/SimilaritySearch                | Get
ddc                | GET    /v1/ddc/similarity-searches/{id}/data-objects/export                   | DDC/SimilaritySearch                | List all
ddc                | POST   /v1/ddc/similarity-searches/{id}/run                                   | DDC/SimilaritySearch                | Post
ddc                | GET    /v1/ddc/system-settings/agent-labels                                   | DDC                                 | List
ddc                | GET    /v1/ddc/system-settings/branch-locations                               | DDC                                 | List
ddc                | POST   /v1/ddc/system-settings/branch-locations                               | DDC                                 | Create
ddc                | DELETE /v1/ddc/system-settings/fam                                            | DDC                                 | Delete
ddc                | GET    /v1/ddc/system-settings/fam                                            | DDC                                 | Get
ddc                | POST   /v1/ddc/system-settings/fam                                            | DDC                                 | Create
ddc                | PUT    /v1/ddc/system-settings/fam                                            | DDC                                 | Update
ddc                | POST   /v1/ddc/system-settings/fam/connection-test                            | DDC                                 | Connection test
ddc                | GET    /v1/ddc/system-settings/hadoop/dataengine                              | DDC                                 | Get
ddc                | PUT    /v1/ddc/system-settings/hadoop/dataengine                              | DDC                                 | Update
ddc                | GET    /v1/ddc/system-settings/hadoop/hdfs                                    | DDC                                 | Get
ddc                | PUT    /v1/ddc/system-settings/hadoop/hdfs                                    | DDC                                 | Update
ddc                | GET    /v1/ddc/system-settings/hadoop/livy                                    | DDC                                 | Get
ddc                | PUT    /v1/ddc/system-settings/hadoop/livy                                    | DDC                                 | Update
ddc                | GET    /v1/ddc/system-settings/infotypes                                      | DDC                                 | List all
ddc                | POST   /v1/ddc/system-settings/infotypes                                      | DDC                                 | Create
ddc                | PATCH  /v1/ddc/system-settings/infotypes/change-precision                     | DDC                                 | Update
ddc                | GET    /v1/ddc/system-settings/infotypes/{id}                                 | DDC                                 | Get
ddc                | PUT    /v1/ddc/system-settings/infotypes/{id}                                 | DDC                                 | Update
ddc                | GET    /v1/ddc/system-settings/mlaas                                          | DDC                                 | Get
ddc                | PUT    /v1/ddc/system-settings/mlaas                                          | DDC                                 | Put
ddc                | GET    /v1/ddc/system-settings/mlaas/status                                   | DDC                                 | Get
ddc                | GET    /v1/ddc/system-settings/properties/{name}                              | DDC                                 | Get
ddc                | PATCH  /v1/ddc/system-settings/properties/{name}                              | DDC                                 | Update
ddc                | POST   /v1/ddc/system-settings/properties/{name}/reset                        | DDC                                 | Reset
ddc                | GET    /v1/ddc/system-settings/scans                                          | DDC                                 | Get
ddc                | PUT    /v1/ddc/system-settings/scans                                          | DDC                                 | Update
ddc                | GET    /v1/ddc/system-settings/sensitivity-levels                             | DDC                                 | List
ddc                | GET    /v1/ddc/system-settings/tags                                           | DDC                                 | List
ddc                | GET    /v1/ddc/system-settings/tdp/choice                                     | DDC                                 | Get
ddc                | GET    /v1/ddc/system-settings/tdp/connection-check                           | DDC                                 | Get
ddc                | GET    /v1/ddc/system-settings/tdpaas                                         | DDC                                 | Get
ddc                | POST   /v1/ddc/system-settings/tdpaas                                         | DDC                                 | Post
ddc                | PUT    /v1/ddc/system-settings/tdpaas                                         | DDC                                 | Update
ddc                | GET    /v1/ddc/system-settings/tdpaas/regions                                 | DDC                                 | Get
ddc                | GET    /v1/ddc/system/ram-available                                           | DDC                                 | Gets the current ram in the system (MB)
ddc                | GET    /v1/ddc/system/ram-recommended                                         | DDC                                 | Gets the recommended RAM to deploy DDC. (MB)
protect-app        | GET    /v1/protectapp/clients                                                 | ProtectApp/Client-Profiles          | List
protect-app        | POST   /v1/protectapp/clients                                                 | ProtectApp/Client-Profiles          | Registers
protect-app        | DELETE /v1/protectapp/clients/{name}                                          | ProtectApp/Client-Profiles          | Delete
protect-app        | GET    /v1/protectapp/clients/{name}                                          | ProtectApp/Client-Profiles          | Get
protect-app        | GET    /v1/protectapp/profiles                                                | ProtectApp/Client-Profiles          | List
protect-app        | POST   /v1/protectapp/profiles                                                | ProtectApp/Client-Profiles          | Create
protect-app        | DELETE /v1/protectapp/profiles/{name}                                         | ProtectApp/Client-Profiles          | Delete
protect-app        | GET    /v1/protectapp/profiles/{name}                                         | ProtectApp/Client-Profiles          | Get
protect-file       | GET    /v1/protectfile/accesspolicies/                                        | ProtectFile/AccessPolicies          | List
protect-file       | POST   /v1/protectfile/accesspolicies/                                        | ProtectFile/AccessPolicies          | Create
protect-file       | DELETE /v1/protectfile/accesspolicies/{id}                                    | ProtectFile/AccessPolicies          | Delete
protect-file       | GET    /v1/protectfile/accesspolicies/{id}                                    | ProtectFile/AccessPolicies          | Get
protect-file       | PATCH  /v1/protectfile/accesspolicies/{id}                                    | ProtectFile/AccessPolicies          | Update
protect-file       | GET    /v1/protectfile/accesspolicygroups/                                    | ProtectFile/AccessPolicyGroups      | List
protect-file       | POST   /v1/protectfile/accesspolicygroups/                                    | ProtectFile/AccessPolicyGroups      | Create
protect-file       | GET    /v1/protectfile/accesspolicygroups/{groupId}/accesspolicies/           | ProtectFile/AccessPolicyGroups      | List AccessPolicies
protect-file       | DELETE /v1/protectfile/accesspolicygroups/{groupId}/accesspolicies/{policyId} | ProtectFile/AccessPolicyGroups      | Remove AccessPolicy
protect-file       | POST   /v1/protectfile/accesspolicygroups/{groupId}/accesspolicies/{policyId} | ProtectFile/AccessPolicyGroups      | Add AccessPolicy
protect-file       | DELETE /v1/protectfile/accesspolicygroups/{id}                                | ProtectFile/AccessPolicyGroups      | Delete
protect-file       | GET    /v1/protectfile/accesspolicygroups/{id}                                | ProtectFile/AccessPolicyGroups      | Get
protect-file       | PATCH  /v1/protectfile/accesspolicygroups/{id}                                | ProtectFile/AccessPolicyGroups      | Update
protect-file       | GET    /v1/protectfile/clientprofiles/                                        | ProtectFile/ClientProfiles          | List
protect-file       | POST   /v1/protectfile/clientprofiles/                                        | ProtectFile/ClientProfiles          | Create
protect-file       | DELETE /v1/protectfile/clientprofiles/{id}                                    | ProtectFile/ClientProfiles          | Delete
protect-file       | GET    /v1/protectfile/clientprofiles/{id}                                    | ProtectFile/ClientProfiles          | Get
protect-file       | PATCH  /v1/protectfile/clientprofiles/{id}                                    | ProtectFile/ClientProfiles          | Update
protect-file       | GET    /v1/protectfile/clients/                                               | ProtectFile/Clients                 | List
protect-file       | GET    /v1/protectfile/clients/{clientId}/clusters/                           | ProtectFile/Clients                 | List Clusters
protect-file       | PATCH  /v1/protectfile/clients/{clientId}/fingerprint/refresh                 | ProtectFile/Clients                 | Fingerprint refresh
protect-file       | GET    /v1/protectfile/clients/{clientId}/rules/                              | ProtectFile/Clients                 | Show Rules
protect-file       | DELETE /v1/protectfile/clients/{clientId}/rules/{ruleId}                      | ProtectFile/Clients                 | Remove Rule
protect-file       | GET    /v1/protectfile/clients/{clientId}/rules/{ruleId}                      | ProtectFile/Clients                 | Get Rule
protect-file       | POST   /v1/protectfile/clients/{clientId}/rules/{ruleId}                      | ProtectFile/Clients                 | Add Rule
protect-file       | PATCH  /v1/protectfile/clients/{clientId}/rules/{ruleId}/drive_guid           | ProtectFile/Clients                 | Update Drive GUID
protect-file       | PATCH  /v1/protectfile/clients/{clientId}/rules/{ruleId}/operation            | ProtectFile/Clients                 | Deploy Rule
protect-file       | GET    /v1/protectfile/clients/{clientId}/shares/                             | ProtectFile/Client-Share            | List Shares
protect-file       | DELETE /v1/protectfile/clients/{clientId}/shares/{shareId}                    | ProtectFile/Client-Share            | Delete Link
protect-file       | GET    /v1/protectfile/clients/{clientId}/shares/{shareId}                    | ProtectFile/Client-Share            | Get Link
protect-file       | POST   /v1/protectfile/clients/{clientId}/shares/{shareId}                    | ProtectFile/Client-Share            | Create Link
protect-file       | DELETE /v1/protectfile/clients/{id}                                           | ProtectFile/Clients                 | Delete
protect-file       | GET    /v1/protectfile/clients/{id}                                           | ProtectFile/Clients                 | Get
protect-file       | PATCH  /v1/protectfile/clients/{id}                                           | ProtectFile/Clients                 | Update
protect-file       | GET    /v1/protectfile/clusters/                                              | ProtectFile/Clusters                | List
protect-file       | POST   /v1/protectfile/clusters/                                              | ProtectFile/Clusters                | Create
protect-file       | GET    /v1/protectfile/clusters/{clusterId}/clients/                          | ProtectFile/Clusters                | List Clients
protect-file       | DELETE /v1/protectfile/clusters/{clusterId}/clients/{clientId}                | ProtectFile/Clusters                | Remove Client
protect-file       | GET    /v1/protectfile/clusters/{clusterId}/clients/{clientId}                | ProtectFile/Clusters                | Get Client
protect-file       | POST   /v1/protectfile/clusters/{clusterId}/clients/{clientId}                | ProtectFile/Clusters                | Add Client
protect-file       | GET    /v1/protectfile/clusters/{clusterId}/rules/                            | ProtectFile/Clusters                | Show Rules
protect-file       | DELETE /v1/protectfile/clusters/{clusterId}/rules/{ruleId}                    | ProtectFile/Clusters                | Remove Rule
protect-file       | GET    /v1/protectfile/clusters/{clusterId}/rules/{ruleId}                    | ProtectFile/Clusters                | Get Rule
protect-file       | POST   /v1/protectfile/clusters/{clusterId}/rules/{ruleId}                    | ProtectFile/Clusters                | Add Rule
protect-file       | PATCH  /v1/protectfile/clusters/{clusterId}/rules/{ruleId}/operation          | ProtectFile/Clusters                | Deploy Rule
protect-file       | DELETE /v1/protectfile/clusters/{id}                                          | ProtectFile/Clusters                | Delete
protect-file       | GET    /v1/protectfile/clusters/{id}                                          | ProtectFile/Clusters                | Get
protect-file       | PATCH  /v1/protectfile/clusters/{id}                                          | ProtectFile/Clusters                | Update
protect-file       | GET    /v1/protectfile/rules/                                                 | ProtectFile/Rules                   | List
protect-file       | POST   /v1/protectfile/rules/                                                 | ProtectFile/Rules                   | Create
protect-file       | DELETE /v1/protectfile/rules/{id}                                             | ProtectFile/Rules                   | Delete
protect-file       | GET    /v1/protectfile/rules/{id}                                             | ProtectFile/Rules                   | Get
protect-file       | PATCH  /v1/protectfile/rules/{id}                                             | ProtectFile/Rules                   | Update
protect-file       | GET    /v1/protectfile/shares/                                                | ProtectFile/Shares                  | List
protect-file       | POST   /v1/protectfile/shares/                                                | ProtectFile/Shares                  | Create
protect-file       | DELETE /v1/protectfile/shares/{id}                                            | ProtectFile/Shares                  | Delete
protect-file       | GET    /v1/protectfile/shares/{id}                                            | ProtectFile/Shares                  | Get
protect-file       | PATCH  /v1/protectfile/shares/{id}                                            | ProtectFile/Shares                  | Update
protect-file       | GET    /v1/protectfile/shares/{shareId}/clients/                              | ProtectFile/Client-Share            | List Clients
protect-file       | GET    /v1/protectfile/shares/{shareId}/rules/                                | ProtectFile/Shares                  | Show Rules
protect-file       | DELETE /v1/protectfile/shares/{shareId}/rules/{ruleId}                        | ProtectFile/Shares                  | Remove Rule
protect-file       | GET    /v1/protectfile/shares/{shareId}/rules/{ruleId}                        | ProtectFile/Shares                  | Get Rule
protect-file       | POST   /v1/protectfile/shares/{shareId}/rules/{ruleId}                        | ProtectFile/Shares                  | Add Rule
protect-file       | PATCH  /v1/protectfile/shares/{shareId}/rules/{ruleId}/operation              | ProtectFile/Shares                  | Deploy Rule
```