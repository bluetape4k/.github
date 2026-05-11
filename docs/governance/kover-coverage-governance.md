# Kover Coverage Governance

## Purpose

Kover is the standard coverage tool for bluetape4k repositories. Coverage
reports are useful only when they either enforce a threshold or explicitly
document why the repository remains report-only.

## Threshold Tiers

| Tier | Target | Applies to |
|---|---:|---|
| Core library | 80% line coverage | Stable public APIs with mostly unit-testable behavior. |
| Integration-heavy library | 60-70% line coverage | Modules dominated by external services, containers, native runtimes, or framework wiring. |
| Report-only transition | No failing gate yet | Repositories with Kover reports but no validated baseline. Must include a follow-up threshold plan. |
| Workshop/demo | No production gate | Example repositories. Tests should compile/run, but coverage is informational. |

## Repository Inventory

| Repository | Current state | Policy | CI/Nightly signal |
|---|---|---|---|
| `bluetape4k-aws` | Kover XML reports in Nightly; no verify bounds. | Report-only transition due AWS/LocalStack integration cost. Baseline first, then 70% for pure client modules and lower documented bounds for Spring/Ktor integration modules. | Nightly uploads module coverage artifacts. |
| `bluetape4k-experimental` | No stable Kover gate. | Documented exception: unpublished experimental Java 25/Spring Boot 4 work. Add gates only before publishing. | CI/Nightly test signal only. |
| `bluetape4k-exposed` | Kover reports plus module excludes; no broad verify bounds. | Report-only transition due multi-database integration surface. Start with core/cache/batch baselines before broad gates. | CI/Nightly upload coverage artifacts. |
| `bluetape4k-graph` | Aggregate Kover reports; benchmark/examples excluded. | Report-only transition. Gate graph-io/core and pure wrappers first; DB backends need lower integration-heavy bounds. | Nightly uploads coverage artifacts. |
| `bluetape4k-image` | Aggregate Kover reports; native/libvips variants included as reports. | Report-only transition. Gate pure image module first; native variants need platform-specific exceptions. | Nightly uploads coverage artifacts. |
| `bluetape4k-javers` | Aggregate Kover reports; no verify bounds. | Report-only transition. Gate core first, Redis/Kafka persistence after baseline. | Nightly uploads coverage artifacts. |
| `bluetape4k-leader` | `leader-core`, `leader-micrometer`, `leader-zookeeper` enforce 80%; `leader-spring-boot` enforces 60%. | Enforced for validated modules; other backends remain documented integration-heavy exceptions. | Nightly runs `koverVerify` for the enforced modules. |
| `bluetape4k-projects` | Broad Kover report aggregation; no broad verify enforcement. | Report-only transition across most modules. Existing low-baseline findings must become module-level follow-ups before failing gates are enabled. | Nightly aggregates Kover XML artifacts. |
| `bluetape4k-text` | Kover reports in Nightly; benchmark package excluded in `text-search`. | Report-only transition. Tokenizer/text-search modules are good candidates for 80% gates after baseline. | Nightly uploads module coverage artifacts. |
| `bluetape4k-workshop` | No production Kover gate. | Documented exception: workshop/demo repository. Coverage is informational only. | Nightly test signal only. |

## Required Repo-Local Policy

Each listed repository owns `docs/governance/kover-coverage-policy.md` with:

- current Kover status
- enforced modules and thresholds, if any
- documented exceptions
- threshold follow-up plan
- CI/Nightly task contract

## Promotion Rule

Do not add failing `koverVerify` bounds until a module has a recent measured
baseline and a realistic improvement path. Once a bound exists, CI or Nightly
must execute the corresponding `koverVerify` task.
