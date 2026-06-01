# CipherTrust Swagger - pre-split index

Source: [definition-beta.json](../../definition-beta.json) (~14.8 MB / ~3.7M tokens - DO NOT load).

Per-area JSON splits under [areas/](areas/) reference a shared [definitions.json](definitions.json) (~635 KB) via `$ref`.
For most resource lookups, load only the area file - resolve `$ref`s by greping `definitions.json` for the specific `D####` name.

For a searchable list of every operation across all areas, see [operations.md](operations.md).

## Areas

| Area | Ops | Paths | Size (KB) | Description |
|---|---:|---:|---:|---|
| [`auth-users`](areas/auth-users.json) | 58 | 37 | 85 | Authentication, users, groups, domains, permissions |
| [`cckm-aws`](areas/cckm-aws.json) | 100 | 80 | 199 | CCKM AWS - keys, KMS, custom key stores, XKS |
| [`cckm-azure`](areas/cckm-azure.json) | 77 | 57 | 156 | CCKM Azure - keys, certificates, secrets |
| [`cckm-google`](areas/cckm-google.json) | 116 | 87 | 274 | CCKM Google Cloud - keys, Workspace CSE, EKM |
| [`cckm-hsm`](areas/cckm-hsm.json) | 21 | 14 | 39 | CCKM HSM Luna keys |
| [`cckm-microsoft`](areas/cckm-microsoft.json) | 18 | 12 | 32 | CCKM Microsoft DKE |
| [`cckm-misc`](areas/cckm-misc.json) | 42 | 27 | 58 | CCKM smaller integrations (catch-all) |
| [`cckm-oracle`](areas/cckm-oracle.json) | 61 | 47 | 114 | CCKM Oracle Cloud Infrastructure keys, vaults |
| [`cckm-sap`](areas/cckm-sap.json) | 67 | 47 | 103 | CCKM SAP Data Custodian keys, HYOK |
| [`cckm-sfdc`](areas/cckm-sfdc.json) | 47 | 31 | 67 | CCKM Salesforce tenant secrets |
| [`cm-admin`](areas/cm-admin.json) | 49 | 30 | 69 | CM admin - Certificate Authority, SSH keys, Interfaces, SNMP, NAE-XML, Quorum |
| [`cm-keys`](areas/cm-keys.json) | 44 | 27 | 179 | CM core keys API (/v1/vault) |
| [`cm-logs`](areas/cm-logs.json) | 18 | 14 | 32 | Audit records, logger config, syslog records |
| [`cm-misc`](areas/cm-misc.json) | 132 | 86 | 216 | Misc CM endpoints not in another bucket |
| [`cm-ops`](areas/cm-ops.json) | 43 | 33 | 89 | Operational: licensing, backups, migrations, scheduler |
| [`cm-system`](areas/cm-system.json) | 107 | 76 | 147 | System, configs, cluster |
| [`connections`](areas/connections.json) | 168 | 99 | 236 | All connectionmgmt endpoints (AWS/Azure/GCP/OCI/SCP/etc.) |
| [`cte`](areas/cte.json) | 210 | 135 | 430 | CipherTrust Transparent Encryption - clients, policies, rules, profiles, guardpoints |
| [`data-protection`](areas/data-protection.json) | 114 | 61 | 191 | Data Protection - BDT jobs/policies, Crypto, key formats |
| [`ddc`](areas/ddc.json) | 183 | 150 | 207 | Data Discovery & Classification |
| [`protect-app`](areas/protect-app.json) | 8 | 4 | 16 | ProtectApp |
| [`protect-file`](areas/protect-file.json) | 64 | 33 | 92 | ProtectFile clients, clusters |

**Shared definitions:** [definitions.json](definitions.json) (635 KB, 494 entries)

## How to use this

1. **Decide which area you need.** When adding a resource, the area name usually maps to the provider subsystem (e.g. CCKM Azure -> `cckm-azure`).
2. **Read the area file.** Each contains operation paths with inlined schemas (small ones) and `"$ref": "../definitions.json#/D####"` (large/shared ones).
3. **Resolve refs on demand.** When you hit a `$ref` you need, grep `definitions.json` for `"D####":` and read those lines only. Do NOT load the entire definitions.json.
4. **Search across all areas:** grep [operations.md](operations.md) for the keyword (path fragment, tag, summary text, or operationId), then jump to the area file.
5. **DO NOT load `definition-beta.json` directly.** It is ~3.7M tokens.

## Regenerating

Run `python .claude/swagger/scripts/regenerate.py` after Thales publishes a new `definition-beta.json`.
