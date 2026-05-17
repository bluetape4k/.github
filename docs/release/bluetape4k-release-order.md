# bluetape4k Release Order

Repository dependency graph and release sequence for the bluetape4k organization.
Validated as of 2026-05-17.

---

## Dependency Graph

```
bluetape4k-projects (io.github.bluetape4k)
│
├── bluetape4k-exposed   ──────────────────────────────────┐
│   (io.github.bluetape4k.exposed)                        │
│                                                          │
├── bluetape4k-aws                                         │
│   (io.github.bluetape4k.aws)                             │
│                                                          ▼
├── bluetape4k-image                            bluetape4k-leader
│   (io.github.bluetape4k.image)                (io.github.bluetape4k.leader)
│
├── bluetape4k-text
│   (io.github.bluetape4k.text)
│
├── bluetape4k-graph
│   (io.github.bluetape4k.graph)
│
└── bluetape4k-javers
    (io.github.bluetape4k.javers)

All libraries above ──────────────────────────────────────►  bluetape4k-dependencies
                                                             (io.github.bluetape4k)
                                                             [version catalog aggregator]
```

**Notes:**
- `bluetape4k-graph` uses `org.jetbrains.exposed` (upstream) directly — does **not** depend on `bluetape4k-exposed`.
- `bluetape4k-leader` depends on `bluetape4k-exposed` (test helpers: `exposed-jdbc-tests`, `exposed-r2dbc-tests`).
- All repos depend on `bluetape4k-projects` as the foundational BOM.
- `bluetape4k-dependencies` is the ecosystem-wide version catalog; release it last, after all others are published.

---

## Release Tiers

### Tier 0 — Foundation (already released)

| Repository | Group ID | Version | Maven Central |
|---|---|---|---|
| `bluetape4k-projects` | `io.github.bluetape4k` | 1.8.0 | ✅ 1.8.0 |

### Tier 1 — Independent libs (can release in parallel)

All depend only on `bluetape4k-projects`. No dependencies between these repos.

| Repository | Group ID | Target Version | Maven Central |
|---|---|---|---|
| `bluetape4k-exposed` | `io.github.bluetape4k.exposed` | 1.8.0 | ❌ unreleased |
| `bluetape4k-aws` | `io.github.bluetape4k.aws` | 0.1.0 | ❌ unreleased |
| `bluetape4k-image` | `io.github.bluetape4k.image` | 0.1.0 | ❌ unreleased |
| `bluetape4k-text` | `io.github.bluetape4k.text` | 0.1.0 | ❌ unreleased |
| `bluetape4k-graph` | `io.github.bluetape4k.graph` | 0.3.0 | ❌ 0.2.0 released; 0.3.0 pending |
| `bluetape4k-javers` | `io.github.bluetape4k.javers` | 0.1.0 | ❌ unreleased |

### Tier 2 — Depends on Tier 1

| Repository | Group ID | Target Version | Blocked by |
|---|---|---|---|
| `bluetape4k-leader` | `io.github.bluetape4k.leader` | 0.1.0 | `bluetape4k-exposed` 1.8.0 |

### Tier 3 — Ecosystem catalog (release last)

| Repository | Group ID | Target Version | Notes |
|---|---|---|---|
| `bluetape4k-dependencies` | `io.github.bluetape4k` | 1.0.0 | Aggregates all library versions |

---

## Release Sequence

```
Step 1:  [released] bluetape4k-projects 1.8.0
                          │
Step 2:  ┌────────────────┼────────────────┐────────────┬────────────────┐
         ▼                ▼                ▼            ▼                ▼
     bluetape4k-   bluetape4k-aws  bluetape4k-  bluetape4k-  bluetape4k-javers
       exposed          0.1.0        image        text           0.1.0
        1.8.0                        0.1.0        0.1.0
                                                              + bluetape4k-graph
                                                                   0.3.0
         │
Step 3:  ▼
     bluetape4k-leader
          0.1.0
              │
Step 4:       ▼
     bluetape4k-dependencies
          1.0.0
```

---

## Checklist per Tier

Before releasing any Tier N library, verify that all Tier N-1 dependencies are:
- [ ] Published on Maven Central (HTTP 200 on the `.pom` URL)
- [ ] `snapshotVersion=` is empty in the source repo's `gradle.properties`
- [ ] Referenced as release version (not `-SNAPSHOT`) in the downstream catalog

```bash
# Verify dependency is on Maven Central before proceeding
curl -o /dev/null -s -w "%{http_code}" \
  "https://repo1.maven.org/maven2/<group-path>/<artifact>/<version>/<artifact>-<version>.pom"
# Must return 200
```

---

## Current Status (2026-05-17)

| Repository | Status | Notes |
|---|---|---|
| `bluetape4k-projects` 1.8.0 | ✅ Released | On Maven Central |
| `bluetape4k-exposed` 1.8.0 | 🔄 In progress | Bugs #117–#120 fixed; PR #131 merged; pre-release checklist pending |
| `bluetape4k-graph` 0.3.0 | 🔄 Prepared | `snapshotVersion=` cleared; release process pending |
| `bluetape4k-aws` 0.1.0 | ⏳ Queued | Awaiting pre-release checklist |
| `bluetape4k-image` 0.1.0 | ⏳ Queued | Awaiting pre-release checklist |
| `bluetape4k-text` 0.1.0 | ⏳ Queued | Awaiting pre-release checklist |
| `bluetape4k-javers` 0.1.0 | ⏳ Queued | Awaiting pre-release checklist |
| `bluetape4k-leader` 0.1.0 | ⏳ Blocked | Waiting for `bluetape4k-exposed` 1.8.0 |
| `bluetape4k-dependencies` 1.0.0 | ⏳ Blocked | Waiting for all Tier 1/2 releases |

---

## Key Rules

1. **Never release in wrong order.** A repo that depends on an unreleased SNAPSHOT of a sibling will fail to resolve at install time.
2. **Same version number ≠ same release.** `bluetape4k-projects 1.8.0` and `bluetape4k-exposed 1.8.0` are independent artifacts with independent release cycles. Both must be on Maven Central separately.
3. **Verify Maven Central HTTP 200, not just local build.** `./gradlew build` succeeds with SNAPSHOT from Maven Central Snapshots, but release consumers will not have access to those.
4. **Run full pre-release checklist** (`bluetape4k-pre-release-checklist.md`) before triggering any release.
5. **Tier 1 repos can be released in parallel** — they have no cross-dependencies.
6. **`bluetape4k-dependencies` always last** — it aggregates all versions; releasing it before Tier 1/2 is complete produces a broken catalog.

---

## Related Documents

- [bluetape4k-release.md](./bluetape4k-release.md) — Step-by-step release procedure
- [bluetape4k-pre-release-checklist.md](./bluetape4k-pre-release-checklist.md) — Pre-release validation checklist
