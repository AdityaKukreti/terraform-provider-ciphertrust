# Subsystem map

What lives in each subsystem package, when to use it, and where the shared bits are. Resource and data source file:line tables are in [resources.md](resources.md) and [data-sources.md](data-sources.md) — this file describes the **package shapes**.

## `internal/provider/` (top level)
- [provider.go](../../internal/provider/provider.go) — provider schema, env-var / config-file / provider-block precedence, `Resources()` (lines 444–510), `DataSources()` (lines 392–442). **Every new resource/data source must be appended to one of these two lists.**
- `provider_test.go` and the many `*_test.go` files alongside it are **acceptance tests** that target the registered resources (require `TF_ACC=1` and a live CM).

## `cm/` — CipherTrust Manager core
Everything CM-native: users, keys, groups, domains, cluster bootstrap/join, scheduler, policies, syslog, NTP, licenses, log forwarders, proxy, password policy, properties, HSM root of trust, registration tokens, SSH keys, password change, Prometheus.

- Resources: `resource_<area>.go` or `resource_cm_<area>.go`
- Data sources: `data_source_cm_<area>.go` (most are `_list` flavored)
- Shared schema: [cm/schema_cm.go](../../internal/provider/cm/schema_cm.go) (1217 lines — reusable attribute definitions, validators, plan modifiers)

When to touch it: any non-cloud CM admin/config resource.

## `connections/` — connection resources & list data sources
Five flavors of connection (AWS, Azure, GCP, OCI, SCP), each with a resource and a list data source. SCP is the only one that's purely CM (not CCKM-routing).

- Resources: `resource_<cloud>_connection.go`
- List data sources: `data_source_<cloud>_connection.go`
- Shared schema: [connections/schema_connections.go](../../internal/provider/connections/schema_connections.go)

Naming subtlety: AWS connection constructor is `NewResourceCCKMAWSConnection` and OCI's is `NewResourceCCKMOCIConnection`, but Azure/GCP just use `NewResource<Cloud>Connection`. The TF type names are all `ciphertrust_<cloud>_connection` regardless.

When to touch it: adding connection auth modes, a new cloud's connection, or fixing drift on existing connection fields.

## `cckm/` — Cloud Cloud Key Manager
Nested by cloud — currently AWS and OCI are implemented. Each cloud has its own resource files, data source files, schema file, and (for OCI) helper files for retries, logging, tags, and a `models/` package.

```
cckm/
├── aws/        — AWS keys, KMS, XKS, CloudHSM, ACLs, rotation, policy templates, key import material
│   ├── resource_aws_*.go / data_source_aws_*.go
│   ├── schema_cckm_aws.go (756 lines — shared schema)
│   └── aws_log.go
├── oci/        — OCI vaults, keys, BYOK keys, BYOK key versions, key versions, ACLs
│   ├── resource_oci_*.go / data_source_*.go
│   ├── oci_key_common.go, oci_key_version_common.go — shared CRUD helpers
│   ├── oci_retry.go — long-operation retry helpers
│   ├── oci_log.go, tags.go
│   └── models/ — OCI-specific JSON models (oci.go, keys.go, key_versions.go, vaults.go)
├── acls/       — cross-cloud ACL schema & helpers (acls.go, schema_acls.go)
├── mutex/      — concurrency primitives for CCKM ops (mutex.go)
└── utils/      — CCKM helpers (helpers.go)
```

When to touch it:
- New AWS/OCI cloud key feature → the cloud's subdir + its `schema_*.go`
- New cloud entirely → add a new subdir mirroring `aws/` or `oci/`, register in `provider.go`
- Cross-cloud ACL changes → `cckm/acls/`
- Operation that can be interrupted by replication / parallel runs → use `cckm/mutex`

## `cte/` — Transparent Encryption
Big surface: clients, client groups, guardpoints, policies + 6 rule types, profiles, user/process/resource/signature sets, CSI groups, LDT group comm service.

- Resources: `resource_cte_<area>.go`
- Data sources: `data_source_cte_<area>.go`
- Shared schema: [cte/schema_cte.go](../../internal/provider/cte/schema_cte.go) (1533 lines)
- Shared TF SDK models: [models/tfsdk_models.go](../../internal/provider/models/tfsdk_models.go) — `DataTransformationRule`, `IDTKeyRule`, `LDTKeyRule`, `SecurityRule`, `CTEPolicyMetadata`, etc.
- Shared JSON models: [models/json_models.go](../../internal/provider/models/json_models.go) — the wire formats

When to touch it: any client/guardpoint/policy/rule work. CTE rules are highly relational — touching one rule type usually means touching its data source too.

## `common/` — shared infrastructure
Loaded by every subsystem.

| File | Purpose |
|---|---|
| [common/client.go](../../internal/provider/common/client.go) | `Client` struct, `NewClient`, `NewCMClientBoot`, `CCKMProviderConfig`, `AuthStruct`, `AuthResponse`, `CipherTrustURL` default |
| [common/auth.go](../../internal/provider/common/auth.go) | Sign-in flow, token refresh |
| [common/requests.go](../../internal/provider/common/requests.go) | The CRUD helpers — see [conventions.md](conventions.md) for the full list |
| [common/urls.go](../../internal/provider/common/urls.go) | `URL_*` constants for every CM API endpoint |
| [common/strings.go](../../internal/provider/common/strings.go) | `MSG_METHOD_START` / `MSG_METHOD_END` / `ERR_METHOD_END` / `ERR_SIGNIN_MISSING_ARGS` |
| [common/utils.go](../../internal/provider/common/utils.go) | Misc helpers |
| [common/parseAttributes.go](../../internal/provider/common/parseAttributes.go) | Attribute parsing for nested types |
| [common/customModifierForListNestedAttribute.go](../../internal/provider/common/customModifierForListNestedAttribute.go) | Custom plan modifier for list-nested attributes |
| [common/customModifierForSingleNestedAttribute.go](../../internal/provider/common/customModifierForSingleNestedAttribute.go) | Custom plan modifier for single-nested attributes |

When to touch it:
- New CM API endpoint → add a `URL_*` constant in `urls.go`
- New HTTP verb / response shape → consider whether one of the existing helpers in `requests.go` fits before adding a new one
- Authentication / token lifecycle → `auth.go` and `client.go`

## `models/` — shared TF SDK + JSON models
Only two files; mostly CTE-flavored types that cross resource/data-source boundaries. CCKM OCI has its own `cckm/oci/models/` package; CCKM AWS keeps its models inline.

## Tests
Acceptance tests sit next to `provider.go` (not in the subsystem folders), e.g. [internal/provider/resource_cckm_aws_key_test.go](../../internal/provider/resource_cckm_aws_key_test.go). Each test gates on `TF_ACC=1` and the standard `CIPHERTRUST_*` env vars.

## Docs & examples
- [docs/](../../docs/) is **regenerated** by `make generate` (which runs `cd tools; go generate ./...`). Don't edit it directly.
- Source of truth: [templates/](../../templates/) (markdown templates with `{{.Description}}` injections) + [examples/](../../examples/) (`.tf` snippets referenced by the templates).
- One resource = one template + one example folder + (after regeneration) one entry in `docs/resources/`.
