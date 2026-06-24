# CipherTrust Terraform Provider — Domain Knowledge

This file is injected into every AI prompt to ground analysis in provider-specific conventions.

## Resource & Data Source Naming

Pattern: `ciphertrust_<platform>_<object>`

Examples:
- `ciphertrust_aws_key`, `ciphertrust_aws_kms` — AWS key management
- `ciphertrust_azure_key`, `ciphertrust_azure_vault` — Azure Key Vault
- `ciphertrust_gcp_key`, `ciphertrust_gcp_key_ring` — GCP Cloud KMS
- `ciphertrust_oci_key` — Oracle Cloud Infrastructure
- `ciphertrust_hsm_luna_partition` — Luna Network HSM
- `ciphertrust_cte_policy`, `ciphertrust_cte_resource_group` — CipherTrust Transparent Encryption
- `ciphertrust_dsm_key` — Data Security Manager
- `ciphertrust_cm_key` — CipherTrust Manager native keys
- `ciphertrust_interface`, `ciphertrust_user`, `ciphertrust_group` — Manager administration

Data sources mirror the resource name: `data "ciphertrust_aws_key" "..." { ... }`

## Framework: Terraform Plugin Framework (NOT SDK v2)

All resources and data sources use **Terraform Plugin Framework** (`github.com/hashicorp/terraform-plugin-framework`), NOT the older SDK v2.

**Correct imports:**
```go
"github.com/hashicorp/terraform-plugin-framework/resource"
"github.com/hashicorp/terraform-plugin-framework/resource/schema"
"github.com/hashicorp/terraform-plugin-framework/types"
"github.com/hashicorp/terraform-plugin-framework/diag"
```

**Correct resource interface methods:** `Metadata`, `Schema`, `Create`, `Read`, `Update`, `Delete`, `Configure`, `ImportState`

**Correct error reporting:**
```go
resp.Diagnostics.AddError("Summary", "Detail: "+err.Error())  // ✅ correct
diag.Errorf("message")                                          // ❌ SDK v2 pattern
```

## Critical Anti-Patterns to Flag

| Anti-pattern | Why it's wrong |
|---|---|
| `diag.Errorf(...)` | SDK v2 only; Plugin Framework uses `resp.Diagnostics.AddError` |
| Storing `ctx` in a struct | Context must be passed per-call, not stored |
| Ignoring `state.Set` errors | Every `resp.State.Set(ctx, &data)` must check returned diag |
| Missing `RequiresReplace()` on immutable attributes | Causes silent in-place updates instead of resource replacement |
| `InsecureSkipVerify: true` | Never acceptable; always verify TLS |
| Logging credential values | `tflog` must never log token/key/password values |
| `resource.UseStateForUnknown()` on mutable fields | Masks drift; only use on computed-only fields |

## Schema Patterns

```go
// Sensitive credentials — always mark Sensitive
schema.StringAttribute{
    Required:  true,
    Sensitive: true,  // ← mandatory for passwords, tokens, keys
}

// Computed-only (server-assigned)
schema.StringAttribute{
    Computed: true,
    PlanModifiers: []planmodifier.String{
        stringplanmodifier.UseStateForUnknown(),
    },
}

// Immutable (forces replacement on change)
schema.StringAttribute{
    Required: true,
    PlanModifiers: []planmodifier.String{
        stringplanmodifier.RequiresReplace(),
    },
}
```

## Test Naming Conventions

- **Acceptance tests:** `TestAcc_<ResourceType>_<Scenario>` — require live CipherTrust Manager; tagged `//go:build acc`
- **Unit tests:** `TestUnit_<FunctionName>_<Scenario>` — no external dependencies
- **Example:** `TestAcc_AWSKey_CreateAndDestroy`, `TestUnit_FlattenLabels_EmptyInput`

Use table-driven tests. All acceptance tests must call `acctest.PreCheck(t)` to skip when credentials are absent.

## Breaking Change Signals (flag immediately)

- Schema attribute removed → existing `.tfstate` files cannot be applied
- Attribute type changed (`types.String` → `types.Int64`) → state type mismatch
- `RequiresReplace()` removed from previously immutable attribute → silent in-place update where replacement is required
- Resource type name string changed in `Metadata()` → all existing state references break
- `Sensitive: true` removed from credential field → credential leak risk in state/logs

## Security Requirements

- All credential attributes (`password`, `token`, `api_key`, `secret`, `private_key`) must have `Sensitive: true`
- Never set `InsecureSkipVerify: true` in HTTP clients — always validate TLS
- Never log credential values via `tflog` or `fmt.Printf`
- Use `types.StringValue("")` to clear sensitive values in state when resource is deleted

## Documentation Requirements

Every resource and data source must have:
- `docs/resources/<name>.md` or `docs/data-sources/<name>.md`
- `examples/resources/<name>/resource.tf` or `examples/data-sources/<name>/main.tf`
- `Subcategory` frontmatter matching the platform (e.g., `AWS`, `Azure`, `GCP`, `CipherTrust Manager`)

## CipherTrust Manager API Patterns

- Base URL: configured per-provider via `ciphertrust_manager` connection resource
- Auth: token-based; token refresh is handled by the provider's HTTP client wrapper
- Key operations typically hit `/v1/cckm/<platform>/keys`
- Connection resources (`ciphertrust_aws_connection`) must be created before key resources that depend on them
- Platform-specific endpoints differ (Azure Managed HSM uses `managedhsm.azure.net`, not `vault.azure.net`)
