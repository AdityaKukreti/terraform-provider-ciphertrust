# Spike: Drift Detection for CipherTrust Manager Resources

Status: Draft (reviewed and corrected against source)
Provider release this spike targets: **1.0.1** (current branch `1.0.1`; changelog top entry `1.0.1-pre1`)
Scope: `internal/provider/cm/` (22 resource files) + `internal/provider/connections/` (5 resource files) = **27 resources**
Out of scope: import / `terraform import` support — tracked as a separate feature (see §7)
Author: (spike owner)
Date: 2026-05-19

---

## 1. Problem Statement

Terraform's contract is that a `terraform plan` against unchanged config on already-applied infrastructure must produce **no diff**. The provider achieves this only if the `Read` method:

1. Fetches the current state of the remote resource on every refresh.
2. Writes **every** attribute managed by the resource schema back into Terraform state.
3. Removes the resource from state when the API reports it no longer exists, so the next plan re-creates it.

Today, several `cm/` and `connections/` resources do not meet this contract. Out-of-band (OOB) changes made via the CM UI, `ksctl`, or the REST API are not detected by `terraform plan`, and resources deleted out of band cause the next `plan`/`apply` to fail with a read error instead of cleanly re-creating.

This spike inventories the gap, picks an implementation pattern, and scopes the rollout. **Import support (recovering OOB-created resources) is intentionally excluded** — see §7 for the dependency.

---

## 2. Audit Results

Inventory of `Read` implementations across `internal/provider/cm/` and `internal/provider/connections/`. File path and the line where `func ... Read(ctx context.Context, req resource.ReadRequest, resp *resource.ReadResponse)` starts are cited so reviewers can jump directly to source.

Severity legend:

- **CRITICAL** — `Read` body is empty or returns without calling the API. State is never refreshed; drift is invisible; OOB delete is invisible.
- **HIGH** — `Read` calls the API but discards the response body, so state is never refreshed.
- **MEDIUM** — `Read` calls the API and hydrates *most* schema fields, but is missing 404/OOB-delete handling, or skips fields that exist in the schema.
- **LOW** — `Read` hydrates the full schema; only missing OOB-delete handling.

### 2.1 `internal/provider/cm/` (22 resources)

| Resource | File:Read line | Severity | Verified findings |
|---|---|---|---|
| `cm_group` | `resource_cm_group.go:137` | CRITICAL | Body is `{}`. |
| `cm_key` | `resource_cm_key.go:1078` | CRITICAL | Body is `{}`. Largest resource (~1300 lines). |
| `cm_ssh_key` | `resource_cm_ssh_key.go:104` | CRITICAL | Body is `{}`. (Schema is minimal: `id`, `key`.) |
| `cm_user_pwd_change` | `resource_cm_user_pwd_change.go:100` | CRITICAL | Body is `{}`. **Treat as an action, not a drift-tracked resource** — see §6. |
| `cm_reg_token` | `resource_cm_reg_token.go:170` | CRITICAL | Loads state then returns without calling the API. |
| `hsm_rot` | `resource_hsm_rot.go:169` | HIGH | Calls `GetById` but discards the response body (`_,`). No state hydration. |
| `cm_user` | `resource_cm_user.go:198` | MEDIUM | Hydrates most fields; has bespoke "preserve config value when API echoes username as nickname" branching (lines 247–251); no 404 handling. |
| `cm_domain` | `resource_cm_domain.go:217` | MEDIUM | Hydrates most fields; no 404 handling. `Meta` (`meta_data`) and `Admins` handling needs verification against API echo behavior. |
| `cm_cluster` | `resource_cm_cluster.go:359` | MEDIUM | Hydrates `node_count`, `node_id`, `status_code`, `status_description`; **does not hydrate `nodes` (list)**; no 404 handling. |
| `cm_prometheus` | `resource_cm_prometheus.go:102` | LOW | Hydrates the full singleton schema (`enabled`, `token`); singleton-with-no-ID is intentional; only missing 404 handling. |
| `cm_interface` | `resource_interface.go:408` | MEDIUM | Hydrates a small subset (`id`, `name`, `created_at`, `updated_at`, `mode`, `cert_user_field`, `auto_gen_ca_id`). Schema has ~25 fields — most are not hydrated. No 404 handling. |
| `cm_license` | `resource_license.go:142` | MEDIUM | Hydrates listed fields. Uses `URL_DOMAIN` (`api/v1/domains`) — see §10, *Needs Verification*. No 404 handling. |
| `cm_log_forwarder` | `resource_log_forwarder.go:275` | MEDIUM | Does **not** hydrate `elasticsearch_params`, `loki_params`, `syslog_params`, `updated_at`. No 404 handling. |
| `cm_ntp` | `resource_ntp.go:131` | MEDIUM | Hydrates `id`, `host`, `key`; no 404 handling. |
| `cm_password_policy` | `resource_password_policy.go:240` | LOW | Hydrates the full schema except `id`; no 404 handling on Read (note: `Create` at line 177 already has a `strings.Contains(err, "404")` block for a different purpose). |
| `cm_policy` | `resource_policy.go:205` | MEDIUM | Hydrates listed fields. `updated_at` is not in this resource's schema (no false-positive). No 404 handling. |
| `cm_policy_attachments` | `resource_policy_attachments.go:168` | MEDIUM | Hydrates `id`, `uri`, `account`, `created_at`. Schema may have additional fields — needs per-field verification when story is implemented. No 404 handling. |
| `cm_property` | `resource_property.go:129` | MEDIUM | Hydrates `name`, `value`, `description`; no 404 handling. |
| `cm_proxy` | `resource_proxy.go:130` | MEDIUM | Has `containsMaskedPassword` preserve logic for `http_proxy`/`https_proxy` (lines 158–169) and same in Update (lines 250–261). Missing 404 handling. |
| `cm_scheduler` | `resource_scheduler.go:442` | MEDIUM | Delegates field hydration to `getParamsFromResponse` (line 754) plus three direct field sets. Coverage relative to full scheduler schema needs verification when the per-resource story is implemented. No 404 handling. |
| `cm_syslog` | `resource_syslog.go:160` | MEDIUM | Conditionally hydrates `message_format`/`port` only when state was non-null — a refresh after OOB add of those fields will not pick them up. No 404 handling. |
| `cm_trial_license` | `resource_trial_license.go:143` | MEDIUM | Hydrates listed fields; no 404 handling. |

### 2.2 `internal/provider/connections/` (5 resources)

| Resource | File:Read line | Severity | Verified findings |
|---|---|---|---|
| `aws_connection` | `resource_aws_connection.go:301` | MEDIUM | Hydrates many fields inline; no 404 handling. |
| `azure_connection` | `resource_azure_connection.go:311` | MEDIUM | Delegates to `getAzureParamsFromResponse` + sets `name` directly; no 404 handling. |
| `gcp_connection` | `resource_gcp_connection.go:193` | MEDIUM | Delegates to `getGcpParamsFromResponse` + sets `name`/`key_file`; no 404 handling. |
| `oci_connection` | `resource_oci_connection.go:261` | MEDIUM | Delegates to `getOciParamsFromResponse`; no 404 handling. |
| `scp_connection` | `resource_scp_connection.go:277` | MEDIUM | Delegates to `getParamsFromResponse` + sets `auth_method`/`host`/`path_to`/`public_key`/`username`; no 404 handling. |

### 2.3 Cross-cutting gaps (verified)

- **No 404 / OOB-delete handling in any `Read`** in `cm/` or `connections/`. The only `404` string-match in the whole subtree lives at `resource_password_policy.go:177` — and that is inside the **`Create`** function (lines 101–239), not `Update` or `Read`.
- **No `ImportState` implementation in `cm/` or `connections/`.** (Note: `internal/provider/cckm/aws/` and `internal/provider/cckm/oci/` *do* implement `ImportState` on multiple resources — e.g. `resource_aws_kms.go:233`, `resource_aws_key.go:639`, `resource_oci_vault.go:311`. So the pattern exists in this codebase; it has just never been applied in `cm/`/`connections/`.)
- **Client errors are string-formatted**: `internal/provider/common/client.go:157` returns `fmt.Errorf("status: %d, body: %s", res.StatusCode, body)`. The only way to detect 404 today is `strings.Contains(err.Error(), "404")`, which is what `password_policy.go:177` does.

---

## 3. Terraform Plugin Framework: Drift-Detection Pattern

Plugin-framework dependency pinned in `go.mod` (do not confuse with the provider's own release version): `github.com/hashicorp/terraform-plugin-framework v1.13.0`, with `terraform-plugin-framework-validators v0.13.0` and `terraform-plugin-framework-timeouts v0.5.0`. All APIs referenced below (`resp.State.RemoveResource`, `UseStateForUnknown`, `ResourceWithImportState`, …) exist at framework v1.13.0.

The framework calls `Read` during every `terraform plan` (refresh phase) and `terraform apply`. The canonical `Read` does four things, in order:

```go
func (r *resourceX) Read(ctx context.Context, req resource.ReadRequest, resp *resource.ReadResponse) {
    // 1. Load prior state (we need the ID to look the resource up)
    var state XModel
    resp.Diagnostics.Append(req.State.Get(ctx, &state)...)
    if resp.Diagnostics.HasError() { return }

    // 2. Fetch from the API
    body, err := r.client.GetById(ctx, reqID, state.ID.ValueString(), common.URL_X)
    if err != nil {
        // 3a. OOB delete -> drop from state, do NOT return an error
        if common.IsNotFound(err) {
            resp.State.RemoveResource(ctx)
            return
        }
        resp.Diagnostics.AddError("Error reading X", err.Error())
        return
    }

    // 3b. Hydrate every managed attribute from the response
    hydrateXFromResponse(body, &state)

    // 4. Persist
    resp.Diagnostics.Append(resp.State.Set(ctx, &state)...)
}
```

Framework rules the current code violates (only items confirmed against the source are listed):

- **Computed attributes must be set on every Read.** If a `Computed` field is left null after a Read, the next plan will show a diff. Several resources (e.g. `cm_log_forwarder`'s `updated_at`, `cm_interface`'s ~20 unhydrated fields) skip schema fields entirely.
- **Optional+Computed attributes that the API auto-populates need an explicit strategy.** `cm_user.Read` already discovered this for `Nickname`/`Name` and works around it with conditional branches (lines 239–251) rather than a plan modifier. Either approach is valid; we should pick one and apply it consistently.
- **Sensitive write-only fields the API never returns** (e.g. `cm_proxy`'s embedded password, `cm_user.Password`, `cm_key.Material`) must not be blindly overwritten with the API's response. `cm_proxy` already does this with `containsMaskedPassword` (`resource_proxy.go:320`). The `Sensitive: true` schema attribute marks them in plan output, but does **not** by itself suppress drift — that requires either a plan modifier (`UseStateForUnknown`) or conditional preserve logic in `Read`.
- **404 must remove the resource from state**, not raise a diagnostic, otherwise OOB delete causes a hard error on the next plan.

---

## 4. Implementation Options

### Option A — Surgical: fix each Read in place
Touch each resource individually, add the missing field assignments, add 404 handling.

- Pros: minimal blast radius per change; easy to review; can ship per-resource.
- Cons: repeats the same 27 nearly-identical 404 blocks; perpetuates the pattern where every Read open-codes `gjson.Get` per field; no shared invariants enforced.

### Option B — Helper-driven: extract shared Read scaffolding
Add helpers to `internal/provider/common/`:
- `IsNotFound(err error) bool` — wraps the current string match (`strings.Contains(err.Error(), "404")`), with a TODO to switch to typed errors once `client.go:doRequest` exposes status codes.
- `HandleReadError(ctx, err, resp *resource.ReadResponse) (handled bool)` — encapsulates "if 404 drop state, else AddError".
- Per-resource `hydrateXFromResponse(...)` helpers (the pattern already exists for connections via `getAzureParamsFromResponse`, `getGcpParamsFromResponse`, etc.).

- Pros: consistent behavior; trivial to audit; smaller per-resource PRs; establishes an idiom for future resources.
- Cons: requires touching `common/` (one PR up front before per-resource PRs); helpers need their own unit tests.

### Option C — Full rewrite: typed HTTP client + generic resource scaffolding
Replace `doRequest`'s `fmt.Errorf("status: %d, ...")` with typed errors (`*HTTPError{StatusCode, Body}`, `NotFoundError`, …) and introduce a generic `ReadFunc[Model any]` adapter.

- Pros: cleanest end state; opens the door to retries, structured error reporting, OpenTelemetry spans.
- Cons: highest scope and risk; touches every CRUD method in every resource; not justified by a drift-detection spike alone.

### Recommendation — **Option B**, with Option C as a follow-up

It fixes the user-visible bug (drift not detected; OOB delete crashes plan) and establishes one pattern reviewers can enforce. Estimated effort: ~1 sprint for shared scaffolding + CRITICAL/HIGH resources; a second sprint to sweep MEDIUM resources and add acceptance coverage.

---

## 5. Out-of-Band (OOB) Change Handling

### 5.1 OOB attribute change (resource still exists, fields drift)

Default behavior with a correct `Read`: drift surfaces in the next `plan` and `apply` reconciles it back to config. **This is the desired behavior** for most attributes — Terraform is the source of truth.

Exceptions (do NOT overwrite from config):

- **Server-generated read-only fields** present in many schemas: `id`, `uri`, `account`, `createdAt`/`created_at`, `updatedAt`/`updated_at`, `application`, `devAccount`/`dev_account`. These are `Computed` and must always be hydrated from the API. (Note: not every schema has these — e.g. `cm_user`, `cm_group`, `cm_key` do **not** include `created_at`/`updated_at` in their TFSDK structs.)
- **Sensitive write-only fields** the API doesn't return or returns masked: `password` (multiple resources), `cm_key.Material`, `cm_key.Password`, embedded auth in `cm_proxy.HTTPProxy`/`HTTPSProxy`. Preserve via plan modifier (`UseStateForUnknown`) or conditional preserve logic in `Read` (the `cm_proxy` approach).
- **Drift-allowed fields** (per-resource policy decision, not a code decision): `user_metadata`, `app_metadata`, `client_metadata`, key-level labels. Often touched by other tools. Default proposal: enforce overwrite to config; revisit per-resource if product owner pushes back.

### 5.2 OOB delete (resource removed via UI/ksctl/API)

`Read` must detect the 404 and call `resp.State.RemoveResource(ctx)`. On the next plan, Terraform shows a `+` create. No diagnostic is raised.

Implementation: shared `common.IsNotFound(err)` helper (string-match today; typed when Option C lands).

### 5.3 OOB create (resource exists in CM but not in Terraform state) — **out of scope**

See §7. Recovering OOB-created resources requires `ImportState`, which is being tracked as a separate feature. This spike does not deliver import.

---

## 6. Edge Cases & Non-Resources

Some entries in `cm/` are actions or singletons, not normal CRUD resources:

- **`cm_user_pwd_change`** — one-shot action. `Create` performs a password change; `Read`/`Update`/`Delete` are intentionally no-ops (`resource_cm_user_pwd_change.go:100,104,108`). Recommendation: keep `Read` empty, but document explicitly in the resource docs that drift is not tracked and re-applying does not re-trigger the action.
- **`hsm_rot`** — root-of-trust setup, also one-shot (`Update` is documented as not supported at line 197). Read should at least confirm the HSM record still exists and detect OOB delete (today it discards the API response).
- **`cm_cluster`** — represents the local node's cluster membership. Read should hydrate `nodes` list (today missing) and treat node removal as drift.
- **`cm_prometheus`** — singleton config (no per-instance ID). Current Read correctly doesn't load prior state; only needs 404 handling.
- **`cm_license`** — see §10, *Needs Verification*. Whole CRUD uses `URL_DOMAIN`; correctness is unverified.

---

## 7. Dependency: Import Feature (separate effort)

Recovering OOB-created resources is a **separate feature** and is **not delivered by this spike**. However, the stories below have one cross-cutting dependency on import:

- **`TestAccX_drift_delete` does not require import.** It exercises only `Read`'s 404 path. No dependency.
- **`TestAccX_no_drift` does not require import.** No dependency.
- **The "recover an OOB-created resource" user journey requires import** and is blocked until the import feature lands. Track separately.

If both efforts ship in the same release, the import work can reuse the `common.IsNotFound` and `common.HandleReadError` helpers introduced here. Coordinate the helper API in `internal/provider/common/` to avoid two parallel patterns.

---

## 8. Acceptance Test Strategy

Drift detection is invisible in code review without tests that exercise the refresh cycle. Per-resource:

1. **`TestAccX_no_drift`** — `Create` via Terraform, then `PlanOnly: true, ExpectNonEmptyPlan: false`. Catches perpetual-diff regressions caused by Optional+Computed fields with API defaults. **This is the highest-leverage test** — it would have surfaced every CRITICAL row in §2 immediately.
2. **`TestAccX_drift_delete`** — `Create` via Terraform, delete via the SDK client (or raw HTTP), then a `RefreshState: true` step, then a plan step that expects a `+ create`. Verifies the 404 path.
3. **`TestAccX_drift_attribute`** — `Create` via Terraform, mutate one attribute via the SDK client, then `RefreshState: true` + `ExpectNonEmptyPlan: true`, then a non-refresh step that asserts apply restored the attribute.

Make `TestAccX_no_drift` a required CI gate for every new resource going forward (see Epic 5 in stories).

---

## 9. Risks

- **Schema-level changes** (adding `UseStateForUnknown` plan modifiers, switching `Optional` to `Optional+Computed`) can cause state-file diffs for existing users. Prefer behavior fixes in `Read` first; only touch schemas when the field genuinely cannot be reconciled otherwise.
- **404 string-matching is fragile** if CM error bodies change format. Acceptance: tolerate the fragility now; track follow-up to type the client errors (Option C).
- **Acceptance tests require a live CipherTrust Manager.** The repo's existing test pattern uses `TF_ACC=1`-gated tests. Drift tests will need network access to a CM instance and may need additional credentials beyond what current `TestAcc*` tests use (specifically the ability to mutate via the SDK client outside of Terraform). Verify the test harness supports this before sizing Epic 3.
- **Per-resource drift tolerance is a product policy decision** (which fields to enforce vs tolerate). Surface the list of `metadata`-style fields to product before sizing.
- **`cm_proxy`'s masked-password approach silently keeps stale state** if the operator rotates the password out-of-band: the API returns the new masked value, our code preserves the old plan value, and drift is never surfaced. This is a pre-existing behavior, not a regression — but call it out so reviewers don't propagate the pattern blindly without considering alternatives (e.g. a `password_wo` write-only attribute).

---

## 10. Needs Verification / Unable to Validate

Items the spike could not confirm from source alone. These must be resolved before the matching stories begin work.

1. **`cm_license` endpoint.** All CRUD operations in `resource_license.go` use `common.URL_DOMAIN` (`api/v1/domains`) — same constant used by `resource_cm_domain.go`. No `URL_LICENSE` / `URL_LICENSES` constant exists in `internal/provider/common/urls.go`. This could be:
   - (a) An intentional reuse where licenses are exposed via the domains endpoint; or
   - (b) A bug that has gone unnoticed because nobody runs the resource.
   Action: confirm with CM API owners / try the resource against a real CM instance before writing the Read fix.

2. **Per-resource "every schema field" coverage.** For each MEDIUM-severity resource, the per-story work must enumerate the TFSDK struct fields and compare against what `Read` currently sets. The spike does this only for a sample (`cm_log_forwarder`, `cm_interface`, `cm_cluster`); the rest must be verified at story-implementation time, not assumed.

3. **CM API 404 body format.** The `common.IsNotFound` helper assumes the error string contains `"404"`. We need to confirm this is true for all CM endpoints (e.g. `/api/v1/usermgmt/users/<id>`, `/api/v1/domains/<id>`, …). If any endpoint returns a different status (e.g. 410 Gone, or a 200 with `{"error": "not_found"}`), the helper needs to grow.

4. **Acceptance-test harness capability.** Whether the existing `TF_ACC=1` test framework can issue out-of-band mutations via the SDK client during a TestStep needs confirmation. If not, a thin test-only helper will be needed.

5. **`hsm_rot`, `cm_cluster` lifecycle.** Whether these resources actually support a meaningful `Read` against CM in the field (vs. being write-only setup steps) needs confirmation from the team that owns them.

6. **Per-resource sensitive-field policy.** Which fields should use `UseStateForUnknown` vs `containsMaskedPassword`-style preserve vs unconditional re-hydration is a per-resource decision. The spike lists candidates (§5.1) but does not finalize them.

---

## 11. Deliverables (spike → stories)

1. `common.IsNotFound` + `common.HandleReadError` helpers, with unit tests.
2. Fix the 5 CRITICAL + 1 HIGH resources first (`cm_group`, `cm_key`, `cm_ssh_key`, `cm_reg_token`, `cm_user_pwd_change` *doc only*, `hsm_rot`).
3. Sweep the MEDIUM resources to add 404 handling and missing field hydration.
4. Add `TestAccX_no_drift`, `TestAccX_drift_attribute`, `TestAccX_drift_delete` per resource.
5. CI gate: fail PRs that add a resource without `TestAccX_no_drift`.
6. Resolve every item in §10 before its matching story enters "ready".

See `docs/spikes/drift-detection-stories.md` for the broken-down stories.
