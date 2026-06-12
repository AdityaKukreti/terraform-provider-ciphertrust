# Drift Detection — User Stories

Companion to `drift-detection-spike.md`. Stories are grouped by epic. Sizes are rough t-shirts; teams should re-point.

**Target release: provider 1.0.1** (current branch `1.0.1`).
**Scope reminder:** `internal/provider/cm/` (22 resources) + `internal/provider/connections/` (5 resources) = 27 resources. **Import / `terraform import` support is a separate feature** and is *not* delivered here. The import effort consumes the helpers introduced by Epic 1; coordinate so it can reuse them.

**Acceptance-criteria template for every "fix Read" story** (do not re-state for each one):

> 1. The `Read` function calls the appropriate `client.*` API and hydrates every field declared in the resource's TFSDK struct. The implementer must enumerate the schema struct (in `schema_cm.go` / `schema_connections.go`) and prove field coverage in the PR description — no assumption.
> 2. 404 / not-found error from the API → `resp.State.RemoveResource(ctx)` and no diagnostic. Uses the shared `common.IsNotFound` / `common.HandleReadError` helpers from Epic 1.
> 3. Sensitive write-only fields (where present) either use `UseStateForUnknown` plan modifier OR a `Read`-side preserve guard that does not overwrite state with the API's masked/empty value. Decision is documented in the PR.
> 4. New acceptance tests `TestAccX_no_drift` and `TestAccX_drift_delete` added and passing under `TF_ACC=1`. `TestAccX_drift_attribute` added for any field where attribute-level drift is expected to be reconciled.
> 5. PR includes a manual smoke note: "ran `terraform plan` twice in a row against an applied resource and confirmed second plan is empty."

---

## Epic 1: Foundation (shared scaffolding)

### TFIN-DD-001 — Add `common.IsNotFound` and `common.HandleReadError` helpers — **S**
**As** a provider developer
**I want** one helper that detects CM 404s and one that drops state on OOB delete
**So that** every `Read` handles OOB delete the same way.

**Acceptance criteria**
- `internal/provider/common/errors.go` (new file) exposes:
  - `IsNotFound(err error) bool` — current implementation: `strings.Contains(err.Error(), "404")` against the format produced by `client.go:157`. Inline comment links to the `Needs Verification` item in the spike.
  - `HandleReadError(ctx context.Context, err error, resp *resource.ReadResponse) (handled bool)` — if `IsNotFound(err)` calls `resp.State.RemoveResource(ctx)` and returns true; otherwise appends an `AddError` diagnostic and returns true; returns false only when `err == nil`.
- Unit tests cover: 404 body, non-404 status (401, 500), nil error, wrapped error (`fmt.Errorf("...: %w", originalErr)`).
- No behavior change to existing resources (opt-in until adopted).

### TFIN-DD-002 — Type the HTTP client errors — **M** (follow-up; not blocking Epic 2/3)
**As** a provider developer
**I want** `client.go:doRequest` to return a typed `*HTTPError{StatusCode, Body}`
**So that** status-code checks don't depend on string matching.

**Acceptance criteria**
- `common.HTTPError` struct with `StatusCode int`, `Body []byte`, implementing `error`.
- `doRequest` (both `client.go:doRequest` and `client.go:doRequestBootstrap`) return `*HTTPError` for any non-2xx; `IsNotFound` switches to `errors.As`.
- All existing string-based callers (today: only `resource_password_policy.go:177` in this scope) still work — either by keeping the `Error()` format unchanged, or by migrating the one caller.
- Unit tests cover all non-2xx branches.

### TFIN-DD-003 — Document the canonical `Read` pattern — **S**
**As** a provider developer
**I want** a one-page doc with the canonical `Read` skeleton + a checklist
**So that** new resources follow the agreed pattern without re-discovery.

**Acceptance criteria**
- Doc under `internal/provider/common/README.md` (or appended to `CONTRIBUTING.md` if one exists).
- Contains the `Read` skeleton from spike §3, the "things that must be hydrated" checklist (every TFSDK field; computed timestamps if present; sensitive-write-only handling), and a pointer to the spike.

---

## Epic 2: Fix CRITICAL / HIGH resources (Read missing or no-op)

### TFIN-DD-010 — Implement `Read` for `ciphertrust_cm_group` — **M**
**Schema fields to hydrate** (verified against `schema_cm.go:54`): `id`, `name`, `description`, `app_metadata`, `client_metadata`, `user_metadata`. (There is **no** `created_at`/`updated_at`/`users_count` field in this schema; do not invent them.)

**Implementation notes**
- Use `client.GetById(URL_GROUP, state.ID)` — verify the API supports lookup by ID; if not, `state.Name` is the alternative.
- Map-type fields (`app_metadata`, `client_metadata`, `user_metadata`) need `types.MapValueFrom` per the existing pattern in `resource_cm_user.go:253`.

Acceptance: per the Epic-level template above.

### TFIN-DD-011 — Implement `Read` for `ciphertrust_cm_key` — **L**
*Largest single story. ~50 schema fields; sensitive material handling required.*

**Schema fields to hydrate** (verified against `schema_cm.go:162`): `id`, `activation_date`, `algorithm`, `archive_date`, `assign_self_as_owner`, `cert_type`, `compromise_date`, `compromise_occurrence_date`, `curveid`, `deactivation_date`, `default_iv`, `description`, `destroy_date`, `empty_material`, `encoding`, `format`, `generate_key_id`, `hkdf_create_parameters`, `id_size`, `key_id`, `mac_sign_bytes`, `mac_sign_key_identifier`, `mac_sign_key_identifier_type`, `material`, `muid`, `object_type`, `name`, `meta`, `padded`, `password`, `process_start_date`, `protect_stop_date`, `revocation_reason`, `revocation_message`, `rotation_frequency_days`, `secret_data_encoding`, `secret_data_link`, `signing_algo`, `key_size`, `unexportable`, `undeletable`, `state`, `template_id`, `usage_mask`, `uuid`, `wrap_key_id_type`, `wrap_key_name`, `wrap_public_key`, `wrap_public_key_padding`, `wrapping_encryption_algo`, `wrapping_hash_algo`, `wrapping_method`, `xts`, `aliases`, `public_key_parameters`, `wrap_hkdf`, `wrap_pbe`, `wrap_rsaaes`, `labels`, `all_versions`, `remove_from_state_on_destroy`.

**Sensitive / write-only fields requiring explicit decision per the Epic template**: `material`, `password`, `wrap_public_key` (and any wrap-key parameters that carry secret material). The CM API does not echo `material` after create; pick `UseStateForUnknown` or `Read`-side preserve and document.

**Acceptance** (in addition to the template):
- `TestAccCMKey_drift_attribute_label` mutates a key label via the SDK and asserts apply reconciles.
- The PR includes a per-field coverage table.

### TFIN-DD-012 — Implement `Read` for `ciphertrust_cm_ssh_key` — **S**
**Schema fields to hydrate** (verified against `schema_cm.go:450`): `id`, `key`. *Only two fields exist*; do not add `name`/`public_key`/`user_id` claims (those are not in the schema).

**Open question** (resolve before starting): the CM SSH-key endpoint may or may not return the key body itself on GET — confirm so we know whether to treat `key` as a sensitive write-only field (preserve via `UseStateForUnknown`) or hydrate it from the response.

Acceptance: per the Epic-level template above.

### TFIN-DD-013 — Implement `Read` for `ciphertrust_cm_reg_token` — **M**
**Schema fields to hydrate** (verified against `schema_cm.go:393`): `id`, `token`, `ca_id`, `cert_duration`, `client_management_profile_id`, `label`, `labels`, `lifetime`, `max_clients`, `name_prefix`. (Note the schema has **both** `label` and `labels` — both must be handled.)

**Sensitive-field decision**: `token` is sensitive write-only (the registration token issued at create time). Pick `UseStateForUnknown` or preserve.

Acceptance: per the Epic-level template above.

### TFIN-DD-014 — Fix `Read` for `ciphertrust_hsm_rot` to hydrate state — **M**
**Schema fields to hydrate** (verified against `HSMSetupTFSDK` in `schema_cm.go`): `id`, `type`, `conn_info`, `initial_config`, `reset`, `delay`, `sub_type`, `config`. *Some of these are create-only inputs* (e.g. `reset`, `delay`, `initial_config`) — the CM HSM API likely does not echo them. Per-field decision is required.

**Lifecycle caveat** (per spike §6): `hsm_rot` is largely one-shot (`Update` is documented as not supported at `resource_hsm_rot.go:197`). The minimum bar for this story is: detect OOB deletion of the HSM record and remove from state; do not invent drift reconciliation for fields the API can't echo.

Acceptance: per the Epic-level template above, modified so that `TestAccHSMRot_drift_attribute` is **not** required (only `_no_drift` and `_drift_delete`). Gated by `TF_ACC_HSM=1` since this requires an HSM-capable test fixture.

### TFIN-DD-015 — Document `ciphertrust_cm_user_pwd_change` as a non-drift-tracked action — **XS**
*Not an implementation story; a docs story.*
- Add a clear "this resource is a one-shot action and does not track drift; re-running `terraform apply` will not re-trigger the password change" note to `docs/resources/cm_user_pwd_change.md`.
- Optional: mark `Create` to add a `RequiresReplace` or `force_new` strategy if product wants idempotency. Leave the actual decision to a separate refactor story; this story is doc-only.

---

## Epic 3: Sweep MEDIUM resources

One story per resource. Each follows the **Epic-level acceptance template** plus its specific schema scope.

### `internal/provider/cm/`

- TFIN-DD-020 — `ciphertrust_cm_user` (`resource_cm_user.go:198`) — **M**
  - Already MEDIUM. Add 404 handling. Decide whether to keep the bespoke `Nickname`/`Name` branches (lines 239–251) or replace with `UseStateForUnknown`. `Password` field must use `UseStateForUnknown` or `Read`-side preserve.
- TFIN-DD-021 — `ciphertrust_cm_domain` (`resource_cm_domain.go:217`) — **M**
  - Add 404 handling. Verify `meta_data` and `admins` (list) round-trip correctly.
- TFIN-DD-022 — `ciphertrust_cm_cluster` (`resource_cm_cluster.go:359`) — **M**
  - Hydrate `nodes` (currently missing). Decide if a node leaving the cluster OOB is "drift" or an inherent state change that warrants `RequiresReplace`. Coordinate with the team that owns clustering.
- TFIN-DD-023 — `ciphertrust_cm_prometheus` (`resource_cm_prometheus.go:102`) — **S**
  - Already LOW; only needs 404 handling and a `_no_drift` test.
- TFIN-DD-024 — `ciphertrust_cm_interface` (`resource_interface.go:408`) — **L**
  - Schema has ~25 fields (see `CMInterfaceTFSDK` in `schema_cm.go`); current Read hydrates ~7. This is the second-largest story after `cm_key`. Includes nested structs (`meta`, `trusted_cas`, `certificate`, `local_auto_gen_attributes`) and a list (`tls_ciphers`).
- TFIN-DD-025 — `ciphertrust_cm_license` (`resource_license.go:142`) — **M** *(BLOCKED on spike §10 item 1)*
  - Resolve whether `URL_DOMAIN` is correct for licenses *before* starting. Do not assume it is a bug; do not assume it is correct.
- TFIN-DD-026 — `ciphertrust_cm_log_forwarder` (`resource_log_forwarder.go:275`) — **M**
  - Hydrate `elasticsearch_params`, `loki_params`, `syslog_params`, `updated_at` (currently skipped).
- TFIN-DD-027 — `ciphertrust_cm_ntp` (`resource_ntp.go:131`) — **S**
- TFIN-DD-028 — `ciphertrust_cm_password_policy` (`resource_password_policy.go:240`) — **S**
  - Already LOW; only add 404 handling on Read and a `_no_drift` test. Do not regress the existing `Create`-time 404 handling at line 177.
- TFIN-DD-029 — `ciphertrust_cm_policy` (`resource_policy.go:205`) — **M**
- TFIN-DD-030 — `ciphertrust_cm_policy_attachments` (`resource_policy_attachments.go:168`) — **M**
  - Enumerate full schema (not done in spike).
- TFIN-DD-031 — `ciphertrust_cm_property` (`resource_property.go:129`) — **S**
- TFIN-DD-032 — `ciphertrust_cm_proxy` (`resource_proxy.go:130`) — **M**
  - Preserve the existing `containsMaskedPassword` logic (`resource_proxy.go:320`). Add 404 handling. **Acknowledge the spike-§9 risk**: OOB password rotation goes undetected with the current preserve approach; either accept and document, or design a follow-up.
- TFIN-DD-033 — `ciphertrust_cm_scheduler` (`resource_scheduler.go:442`) — **L**
  - Schema is large (`CreateJobConfigParamsTFSDK` + per-job-type nested params). Audit `getParamsFromResponse` at line 754 for coverage; extend as needed.
- TFIN-DD-034 — `ciphertrust_cm_syslog` (`resource_syslog.go:160`) — **M**
  - Remove the `if !state.MessageFormat.IsNull()` / `if !state.Port.IsNull()` guards — they suppress drift for OOB-added values. Replace with unconditional hydration.
- TFIN-DD-035 — `ciphertrust_cm_trial_license` (`resource_trial_license.go:143`) — **S**

### `internal/provider/connections/`

- TFIN-DD-040 — `ciphertrust_aws_connection` (`resource_aws_connection.go:301`) — **M**
- TFIN-DD-041 — `ciphertrust_azure_connection` (`resource_azure_connection.go:311`) — **M**
  - Audit `getAzureParamsFromResponse` for full schema coverage.
- TFIN-DD-042 — `ciphertrust_gcp_connection` (`resource_gcp_connection.go:193`) — **M**
  - Audit `getGcpParamsFromResponse`. `key_file` is a sensitive write-only field (the GCP service-account JSON) — requires explicit decision.
- TFIN-DD-043 — `ciphertrust_oci_connection` (`resource_oci_connection.go:261`) — **M**
- TFIN-DD-044 — `ciphertrust_scp_connection` (`resource_scp_connection.go:277`) — **M**
  - `public_key` and any private-key/password are sensitive write-only.

---

## Epic 4: Process & CI

### TFIN-DD-060 — Add CI gate for `TestAccX_no_drift` — **S**
**As** a maintainer
**I want** new resource PRs to fail CI unless they ship a `_no_drift` acceptance test
**So that** we don't regress.

**Acceptance criteria**
- Script (Makefile target or GitHub Actions step) scans `internal/provider/**/resource_*.go` and asserts a matching `TestAccX_no_drift` exists in `internal/provider/*_test.go`.
- Documented in `CONTRIBUTING.md` (or repo README) so contributors know.
- Initial allowlist for resources not yet covered, shrinking as Epic 2/3 stories land.

### TFIN-DD-061 — Drift-detection runbook for support — **S**
**As** a support engineer
**I want** a short doc explaining what users see when CM resources drift
**So that** I can answer "why does my plan show a diff after I changed it in the UI?"

**Acceptance criteria**
- Doc under `docs/` covers: what drift looks like in plan output, how to ignore (`lifecycle.ignore_changes`), how to reconcile via `apply`, and a pointer to the import feature (separate effort) for OOB-created resources.

### TFIN-DD-062 — Observability for `Read` failures — **S** *(optional, recommend doing it)*
**As** an operator running Terraform in CI
**I want** `Read` failures and OOB-delete detections logged at a consistent level
**So that** dashboards / log searches catch a misbehaving CM endpoint without parsing diagnostic text.

**Acceptance criteria**
- `HandleReadError` emits `tflog.Debug` for the 404/RemoveResource path with a stable message prefix (e.g. `"drift: removed from state"`).
- `HandleReadError` emits `tflog.Error` for non-404 read failures with the same prefix scheme.
- No PII / secrets logged.

---

## Epic 5 (cross-cutting): Resolve "Needs Verification" items from spike §10

These are gating items for the matching Epic 2/3 stories. Resolve them in this epic (or inline in the matching story's "research" sub-task) **before** opening the implementation PR.

- TFIN-DD-070 — Confirm correct CM endpoint for `cm_license` (spike §10 item 1). **Blocks TFIN-DD-025.**
- TFIN-DD-071 — Confirm CM API returns recognizable 404 for all endpoints used by `cm/` + `connections/` (spike §10 item 3). **Blocks Epic 1 acceptance of `IsNotFound`.**
- TFIN-DD-072 — Confirm acceptance-test harness can issue out-of-band mutations via the SDK client during a `TestStep` (spike §10 item 4). **Blocks the `_drift_attribute` and `_drift_delete` tests across Epic 2/3.** If unsupported, scope an internal test helper.
- TFIN-DD-073 — Confirm `hsm_rot` and `cm_cluster` Read semantics with the owning teams (spike §10 item 5). **Blocks TFIN-DD-014, TFIN-DD-022.**
- TFIN-DD-074 — Surface the list of sensitive-write-only / drift-tolerated fields to product for a per-resource policy decision (spike §10 item 6). **Soft-blocks** every story that includes sensitive fields (`cm_user`, `cm_key`, `cm_ssh_key`, `cm_reg_token`, `cm_proxy`, `gcp_connection`, `scp_connection`).

---

## Suggested rollout order

1. **Sprint 1**: Epic 5 (verification) in parallel with Epic 1 (foundation). End state: helpers in place; ambiguous decisions resolved; no resource changes shipped yet.
2. **Sprint 2**: Epic 2 (CRITICAL + HIGH) using the helpers from Epic 1. End state: the worst offenders refresh state and detect OOB delete.
3. **Sprint 3**: Epic 3 — sweep MEDIUM resources. End state: full drift detection across `cm/` + `connections/`.
4. **Sprint 4 (overlap)**: Epic 4 (CI gate, runbook, observability). End state: no regression possible.

Total: ~30 stories. ~3 sprints with one engineer, ~1.5 sprints with two if Epic 5 has cleared.

---

## Dependencies on other features

- **Import feature** (separate effort): consumes `common.IsNotFound` / `common.HandleReadError` from TFIN-DD-001. No reverse dependency — drift work does not block import. Recommend the two efforts coordinate on the helper API in `internal/provider/common/` to avoid duplicate work.
- **Typed HTTP errors** (TFIN-DD-002, follow-up): can land after Epic 2/3; the string-based `IsNotFound` is the bridge.

---

## Out of scope (explicit)

- `terraform import` support for any `cm/`/`connections/` resource (separate feature).
- Refactor of `resource_cm_user_pwd_change` from "action shaped as resource" to a different pattern (separate refactor; this spike only documents the current behavior).
- CCKM, CTE resources (different folders; if their drift behavior is also broken, a sibling spike is warranted).
- Migration/state-upgrade work — none of the proposed changes alter the schema; no `StateUpgraders` are needed. **If** a story chooses to add a plan modifier that changes how a field behaves on refresh, the story owner must verify that existing state files don't show a one-time diff after upgrade; that risk is called out per-story rather than blanket.
