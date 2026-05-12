# Nightly Workflow Governance

This document classifies bluetape4k repository Nightly workflows for Issue #2.
The target model is a gated workflow:

- PR/CI: fast changed-scope feedback.
- Daily Nightly: smoke checks with high signal and bounded cost.
- Weekly Full Nightly: expensive integration, container, coverage, and example checks.
- Manual dispatch: selectable `scope` inputs for targeted validation.

## Scope Semantics

Heavy repositories expose:

- `scope=smoke`: compile, detekt, and non-container or low-cost core tests.
- `scope=full`: everything from smoke plus expensive container, external runtime,
  example, or broad coverage jobs.

Scheduled runs use:

- `0 19 * * 1-6`: daily smoke, KST 04:00 Tuesday-Sunday.
- `0 19 * * 0`: weekly full, KST 04:00 Monday.

## Repository Classification

| Repository | Classification | Daily smoke | Weekly full |
|---|---|---|---|
| `bluetape4k-aws` | Split daily/full | Build, detekt, Spring Boot module tests | LocalStack AWS SDK/Kotlin/Ktor and examples |
| `bluetape4k-experimental` | Intentionally simple | Existing build/test path | Same path; unpublished experimental repo |
| `bluetape4k-exposed` | Split daily/full | H2/core/serialization/cache/low-cost modules | PostgreSQL, MySQL, Redis, ClickHouse, Trino, BigQuery, matrix example jobs |
| `bluetape4k-graph` | Split daily/full | Core, TinkerGraph, Spring starter | Neo4j, Memgraph, Apache AGE, FalkorDB, examples |
| `bluetape4k-image` | Split daily/full | Scrimage/core image tests | libvips API, Java 21 vips, Java 25 vips |
| `bluetape4k-javers` | Split daily/full | `javers-core` | Redis and Kafka persistence |
| `bluetape4k-leader` | Split daily/full | Core, H2, Micrometer | Redis, PostgreSQL, MySQL, MongoDB, Hazelcast, ZooKeeper, examples, Spring Boot, Ktor |
| `bluetape4k-projects` | Existing reference split | Build, detekt, core tests, representative Testcontainers smoke groups | Weekly full schedule and targeted repo-local scopes |
| `bluetape4k-text` | Lightweight simple | Existing tokenizer/language/search tests | Same path; no container-heavy jobs found |
| `bluetape4k-workshop` | Split daily/full | Build only | Full example/testcontainers path |

## Central Dispatch

The organization `.github` repository dispatches the common `smoke` or `full`
scope input to repositories that support selective Nightly execution.
Repositories without a scope input stay intentionally simple and receive no
extra dispatch inputs. Repository-specific scopes, such as
`bluetape4k-projects` `testcontainers`, `graphdb`, and `aws`, remain available
through the repository-local workflow dispatch UI.

## Follow-Up Criteria

- Keep expensive new Nightly jobs behind `scope=full` unless there is a written
  operational reason to run them daily.
- When a repository adds a new module, update its repository-local Nightly
  workflow in the same PR or an immediate follow-up PR so the new module's tests
  run in the appropriate smoke/full scope.
- Add a manual `scope` input when a repository gains heavy integration tests.
- Keep coverage artifacts available for full runs; smoke coverage is optional
  unless the repository depends on it for a quality gate.
- Review `bluetape4k-projects` smoke runtime again after several scheduled
  runs; it still includes representative container checks by design.
