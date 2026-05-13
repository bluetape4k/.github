# bluetape4k WIP

Snapshot: 2026-05-13 KST
Scope: GitHub `bluetape4k/*` repositories, issues assigned to `debop`,
created on or after 2026-01-01.

This root queue is the ecosystem-level view. Repo-local details live in each
project `WIP.md` and should stay aligned with this file.

## Refresh Notes

Verified with `gh` on 2026-05-13 KST.

The previous WIP-refresh and merge-wait queues are complete:

- `aws` PR #56, `graph` PR #103, and `exposed` PR #63 are merged.
- `aws` PR #54/#55 and `graph` PR #97/#98/#100 are merged.
- `exposed` dependency PR #58/#59 are merged.
- `graph #99` is closed.

New work should use the updated `bluetape4k-workflow`,
`bluetape4k-design`, and `bluetape4k-patterns` skill routing.

## Reading Guide

Priority is assigned from the whole bluetape4k ecosystem view, not from
single-repo local value.

| Priority | Meaning |
|---|---|
| P0 | Merge hygiene and branch/rule blockers that keep the queue honest. |
| P1 | Foundation or correctness work that unlocks multiple downstream issues. |
| P2 | Valuable feature work after the foundations are stable. |
| P3 | Examples, docs, benchmarks, and adoption work. |
| P4 | Explicitly deferred, low leverage, or decision-only work. |

Issue selection priority:

1. Architecture or API introduction/change with broad future impact.
2. Blocking prerequisite work that unlocks other high-impact issues.
3. Independent features, ordered by difficulty and implementation value.
4. Bugs, tests, CI, and stability work that improves system reliability.
5. Examples and adoption/usability work that helps users start or migrate.
6. Documentation-only work with little or no runtime impact.

## Executive Queue

Do these in order unless a production blocker appears.

1. **Use the updated bluetape4k skill routing for all new work.**
   Start with `bluetape4k-workflow`, then load `bluetape4k-design` for broad
   design/new-module work or `bluetape4k-patterns` for Kotlin implementation.

2. **AWS API work is newly active.**
   `aws #59` introduces field-level KMS encryption and should be treated as a
   broad API/design item before lower-impact examples.

3. **Graph Neptune needs research before implementation.**
   Do `graph #113` before `graph #30`; keep examples such as `graph #111` after
   the backend/testability decision is clear.

4. **Exposed CockroachDB remains the strongest foundation lane.**
   Start with `exposed #30`, then continue `#31` and `#32`.

5. **AWS Ktor and examples follow foundation/API decisions.**
   Continue `aws #10/#11` and examples `#13/#14/#16/#17` after the higher-impact
   API work is either merged or intentionally deferred.

## Selected Next Work

Use this as the immediate working set.

| Order | Work | Lane | Status | Stop condition |
|---:|---|---|---|---|
| 1 | [aws #59](https://github.com/bluetape4k/bluetape4k-aws/issues/59) | KMS field encryption | Open | Public annotation/property API is designed, implemented, documented, and tested. |
| 2 | [graph #113](https://github.com/bluetape4k/bluetape4k-graph/issues/113) | Neptune research | Open | Local testability and implementation strategy are recorded before `graph #30`. |
| 3 | [exposed #30](https://github.com/bluetape4k/bluetape4k-exposed/issues/30) | CockroachDB foundation | Open | Scaffolding and Testcontainers smoke test land. |
| 4 | [exposed #31](https://github.com/bluetape4k/bluetape4k-exposed/issues/31) | CockroachDB dialect | Open | PostgreSQL compatibility and DDL differences are codified. |
| 5 | [exposed #32](https://github.com/bluetape4k/bluetape4k-exposed/issues/32) | CockroachDB retries | Open | Serializable transaction retry guidance and regressions land. |
| 6 | [aws #10](https://github.com/bluetape4k/bluetape4k-aws/issues/10) / [#11](https://github.com/bluetape4k/bluetape4k-aws/issues/11) | AWS Ktor foundation | Open | SQS and DynamoDB Ktor server patterns compile and test. |
| 7 | [graph #111](https://github.com/bluetape4k/bluetape4k-graph/issues/111) | Graph examples | Open | `graph-io` backed sample dataset loaders are available for domain examples. |

## Recommended WIP Limits

| Lane | Limit | Active candidates |
|---|---:|---|
| Research/design | 1 active item | `graph #113` before `graph #30`; `aws #59` needs design-level review |
| New implementation | 1 repo at a time | Prefer `aws #59` or `exposed #30`; do not start both simultaneously |
| Follow-up implementation | 2 ready items | `exposed #31/#32` only after `#30`; AWS Ktor `#10/#11` after API work |
| Examples/adoption | 1 ready item | `graph #111` or AWS examples after their foundations are stable |

## Dependency Map

### AWS

```text
#8 SigV4 (closed by PR #27)
  -> #9 Ktor S3 (closed by PR #28)
      -> #15 Ktor S3 example (closed by PR #54)
      -> #34 aws-ktor KDoc consistency (closed by PR #54)

#1 Spring Boot S3 (closed by PR #29)
  -> #12 Spring Boot S3 example (closed by PR #54)
  -> #33 S3CoroutinesTemplate KDoc (closed by PR #54)

#2 Spring Boot SQS (closed by PR #30)
#4 Spring Boot SNS (closed by PR #55)
  -> #13 Spring Boot SQS/SNS example

#5 KMS support
  -> #59 @KmsEncrypted field-level encryption

#3 Spring Boot DynamoDB (closed by PR #31)
  -> #14 Spring Boot DynamoDB example
  -> #11 Ktor DynamoDB conventions
      -> #17 Ktor DynamoDB example

#10 Ktor SQS
  -> #16 Ktor SQS example
```

### Graph

```text
#13 transaction DSL (closed)
#32 schema/index API (closed)
#34 merge/upsert (closed)
#33 batch insert (closed)
  -> #30 Neptune backend
  -> #10 extra examples

#96 graph-ktor (closed by PR #100)
  -> Ktor examples after PR #100 merge

#99 graph-spring-boot module naming (closed)
  -> should remain separate from graph-ktor

#40 weighted path suspend tests (closed by PR #98)
  -> #41 weighted path benchmark

#113 Neptune local testability research
  -> #30 Neptune backend
```

### Exposed

```text
#7 QueryLookupStrategy (closed)
#8 serializer parity (closed by PR #21)
#6 AuditableR2dbcRepository (closed by PR #22)
  -> #26 R2DBC @Query parity
  -> #4 bucket4j
  -> #5 Spring Modulith integration

#24 CockroachDB epic
  -> #30 scaffolding and smoke test
  -> #31 PostgreSQL compatibility and DDL differences
  -> #32 serializable transaction retry guidance

#25 Trino Phase 2 epic
  -> #27 DataSource connection
  -> #28 streaming/paged query API
  -> #29 batch insert/write path
```
