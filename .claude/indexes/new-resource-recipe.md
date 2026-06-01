# Recipe: add a new resource (or data source)

This is the canonical checklist. Follow it step by step — at every step, look at the closest existing peer in the same subsystem for the exact pattern.

## 0. Find the API in swagger (skip if you already know the endpoint)
The CipherTrust Manager API spec is at [definition-beta.json](../../definition-beta.json) — **3.7M tokens, do not load it directly.** Use the pre-split index:

1. `Grep` [.claude/swagger/operations.md](../swagger/operations.md) for the resource keyword (e.g. "azure key", "rotate", "custom-key-store"). The matched lines tell you which **area** the operations live in.
2. Read the matching [.claude/swagger/areas/<area>.json](../swagger/areas/) file (typically 50–500 KB) for full request/response schemas, parameters, and operationIds.
3. Note the API path — that becomes your `URL_*` constant in step 2 below.

## 1. Pick the subsystem & file name
- CM admin/config → `internal/provider/cm/resource_cm_<thing>.go`
- AWS/Azure/GCP/OCI/SCP connection → `internal/provider/connections/resource_<cloud>_connection.go`
- AWS cloud key resource → `internal/provider/cckm/aws/resource_aws_<thing>.go`
- OCI cloud key resource → `internal/provider/cckm/oci/resource_oci_<thing>.go`
- CTE → `internal/provider/cte/resource_cte_<thing>.go`

Data source uses `data_source_…go` with the same prefix rule. List flavors append `_list` to the TF type name (e.g. `ciphertrust_aws_kms_list`).

## 2. Add a URL constant if it's a new endpoint
Open [internal/provider/common/urls.go](../../internal/provider/common/urls.go) and add the API path as a constant. Use the existing naming: `URL_<UPPER_SNAKE>`. Group with related endpoints.

## 3. Implement the resource

Use the skeleton in [conventions.md](conventions.md#resource-skeleton-the-house-style). The five methods you must implement on `resource.Resource`:
- `Metadata` — sets `resp.TypeName = req.ProviderTypeName + "_<name>"`
- `Configure` — type-asserts `*common.Client` into `r.client`
- `Schema` — attribute definitions (mark `Required` / `Optional` / `Computed`, descriptions, plan modifiers)
- `Create`, `Read`, `Update`, `Delete` — call `r.client.PostData / GetById / UpdateData / DeleteByURL` etc.

Define two tfsdk structs:
1. A **plan/state model** with `types.String`/`Int64`/`Bool` and `tfsdk:"..."` tags matching the schema
2. A **JSON model** for the CM API wire format with `json:"..."` tags

Convert between them at the boundary. For nested types, use the helpers in [common/parseAttributes.go](../../internal/provider/common/parseAttributes.go) where applicable.

## 4. Register the constructor in `provider.go`
Open [internal/provider/provider.go](../../internal/provider/provider.go) and append your constructor:
- Resources: in `Resources()` (lines 444–510), append `<subsystem>.NewResourceFoo,`
- Data sources: in `DataSources()` (lines 392–442), append `<subsystem>.NewDataSourceFoo,`

If your subsystem package isn't already imported at the top of `provider.go`, add the import. Subsystem aliases used today:
```go
aws "github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/cckm/aws"
oci "github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/cckm/oci"
cm "github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/cm"
common "github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/common"
connections "github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/connections"
cte "github.com/ThalesGroup/terraform-provider-ciphertrust/internal/provider/cte"
```

## 5. Update the local indexes
After registration, append a row to:
- [.claude/indexes/resources.md](resources.md) (or `data-sources.md`)
- This keeps the index in sync — future sessions rely on it.

## 6. Add an example
Create `examples/resources/ciphertrust_<name>/resource.tf` with a minimal working example. Doc generation pulls from this folder.

For data sources: `examples/data-sources/ciphertrust_<name>/data-source.tf`.

## 7. Regenerate docs
```sh
make generate
```
That runs `cd tools; go generate ./...` which invokes `terraform-plugin-docs`. It creates/updates `docs/resources/<name>.md` from the schema descriptions plus the example file.

## 8. Add an acceptance test
Create `internal/provider/resource_<name>_test.go` (sits next to `provider.go`, NOT inside the subsystem subfolder — see existing tests for convention). Tests gate on `TF_ACC=1` and require live CM env vars.

Run with:
```sh
make testacc
```

## 9. Build + lint
```sh
make build
make lint
make fmt
```
All must pass before opening a PR. Lint config is at [.golangci.yml](../../.golangci.yml).

## 10. Open a PR
PRs target the `1.0.1` branch (active dev), not `main`. Reference any TFIN-* ticket in the title or description if applicable.

## Common gotchas
- **404 on Read**: keep in state. Don't `resp.State.RemoveResource(ctx)` unless this is mid-Delete of the same id. See commit `43f3b14`.
- **Replication delay**: don't add a manual `time.Sleep` after a write — the `c.PostData`/`c.UpdateData` helpers already do this.
- **uuid per call**: `uuid.New().String()` at the top of each CRUD method, not at struct-init.
- **Pointer schemas**: a few resources use `&schema.BoolAttribute{...}` instead of `schema.BoolAttribute{...}`. Don't mix; copy the surrounding style.
- **Adding a field to existing schema**: also add it to the plan/state model AND the JSON model, AND populate it in Create AND Read AND Update.
