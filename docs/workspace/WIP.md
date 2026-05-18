# bluetape4k WIP

Snapshot: 2026-05-18 KST
Scope: GitHub `bluetape4k/*` repositories, issues assigned to `debop`,
created on or after 2026-01-01.

This root queue is the ecosystem-level view. Repo-local details live in each
project `WIP.md` and should stay aligned with this file.

## Refresh Notes

Verified with `gh` on 2026-05-18 KST.

**New issues registered on 2026-05-18 (round 1 — surface scan):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [projects #539](https://github.com/bluetape4k/bluetape4k-projects/issues/539) | projects | chore: remove deprecated BinaryKafkaCodecs (JDK RCE) | P1 |
| [projects #540](https://github.com/bluetape4k/bluetape4k-projects/issues/540) | projects | test: GrpcServer / AbstractGrpcServer lifecycle tests | P1 |
| [exposed #161](https://github.com/bluetape4k/bluetape4k-exposed/issues/161) | exposed | bug: R2DBC write-behind finally — data loss on cancellation | P0 |
| [leader #304](https://github.com/bluetape4k/bluetape4k-leader/issues/304) | leader | fix: runCatching{} swallows CancellationException in ExposedJdbc lock/elector | P1 |
| [graph #156](https://github.com/bluetape4k/bluetape4k-graph/issues/156) | graph | fix: FalkorDBGraphSuspendOperations.graphExists() swallows CancellationException | P1 |
| [graph #157](https://github.com/bluetape4k/bluetape4k-graph/issues/157) | graph | fix: FalkorDB/MemgraphGraphSchemaManager overly broad runCatching{} | P2 |

**New issues registered on 2026-05-18 (round 2 — deep audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [projects #541](https://github.com/bluetape4k/bluetape4k-projects/issues/541) | projects | perf: FutureToCompletableFutureWrapper spawns one virtual thread per object | P2 |
| [projects #542](https://github.com/bluetape4k/bluetape4k-projects/issues/542) | projects | bug: ResilientNearCacheDecorator.close() silently discards delegate failure | P1 |
| [exposed #162](https://github.com/bluetape4k/bluetape4k-exposed/issues/162) | exposed | bug: AbstractJdbcCaffeineRepository.findAll() runCatching{} swallows all exceptions | P1 |
| [exposed #163](https://github.com/bluetape4k/bluetape4k-exposed/issues/163) | exposed | bug: AbstractR2dbcCaffeineRepository.close() cancels scope before write-behind flush | P1 |
| [leader #305](https://github.com/bluetape4k/bluetape4k-leader/issues/305) | leader | bug: ExposedJdbcLock.tryLock() uses currentTimeMillis() — NTP causes infinite loop | P1 |
| [leader #306](https://github.com/bluetape4k/bluetape4k-leader/issues/306) | leader | bug: ExposedJdbcGroupLock.tryLock() same currentTimeMillis() deadline bug | P1 |
| [graph #158](https://github.com/bluetape4k/bluetape4k-graph/issues/158) | graph | bug: Neo4jGraphSuspendOperations.suspendTransaction() runBlocking inside withContext(IO) | P1 |
| [aws #145](https://github.com/bluetape4k/bluetape4k-aws/issues/145) | aws | feat: S3 listObjectsV2 auto-pagination Flow extension (truncates at 1000) | P2 |

Previous WIP-refresh and merge-wait queues are complete:

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

1. **Fix P0 data-loss bug in R2DBC write-behind first.**
   `exposed #161` — finally block calls suspend `flushBatch()` without
   `NonCancellable`. Silent data loss under any coroutine cancellation.

2. **Fix CancellationException suppression in leader and graph.**
   `leader #304` (ExposedJdbc lock/elector) and `graph #156` (FalkorDB
   graphExists) both swallow `CancellationException` via `runCatching{}`.
   Fix before expanding either module.

3. **Use the updated bluetape4k skill routing for all new work.**
   Start with `bluetape4k-workflow`, then load `bluetape4k-design` for broad
   design/new-module work or `bluetape4k-patterns` for Kotlin implementation.

4. **AWS API work is newly active.**
   `aws #59` introduces field-level KMS encryption and should be treated as a
   broad API/design item before lower-impact examples.

5. **Graph Neptune needs research before implementation.**
   Do `graph #113` before `graph #30`; keep examples such as `graph #111` after
   the backend/testability decision is clear.

6. **Exposed CockroachDB remains the strongest foundation lane.**
   Start with `exposed #30`, then continue `#31` and `#32`.

7. **AWS Ktor and examples follow foundation/API decisions.**
   Continue `aws #10/#11` and examples `#13/#14/#16/#17` after the higher-impact
   API work is either merged or intentionally deferred.

## Selected Next Work

Use this as the immediate working set.

| Order | Work | Lane | Status | Stop condition |
|---:|---|---|---|---|
| 1 | [exposed #161](https://github.com/bluetape4k/bluetape4k-exposed/issues/161) | R2DBC write-behind finally NonCancellable | Open | `finally` block wraps `flushBatch()` in `withContext(NonCancellable)`; regression test added. |
| 2 | [exposed #163](https://github.com/bluetape4k/bluetape4k-exposed/issues/163) | R2DBC write-behind close() race | Open | `close()` waits for `writeBehindJob.join()` before `scope.cancel()`; tested with slow flush. |
| 3 | [projects #542](https://github.com/bluetape4k/bluetape4k-projects/issues/542) | ResilientNearCacheDecorator.close() leak | Open | `runCatching{}` replaced with logged try/catch; resource leak verified absent. |
| 4 | [leader #304](https://github.com/bluetape4k/bluetape4k-leader/issues/304) | ExposedJdbc CancellationException fix | Open | All 6 `runCatching{}` sites replaced with explicit rethrow; tests pass. |
| 5 | [leader #305](https://github.com/bluetape4k/bluetape4k-leader/issues/305) / [#306](https://github.com/bluetape4k/bluetape4k-leader/issues/306) | ExposedJdbc[Group]Lock nanoTime fix | Open | All `currentTimeMillis()` deadline sites replaced with `nanoTime()`; lock timeout verified monotonic. |
| 6 | [graph #158](https://github.com/bluetape4k/bluetape4k-graph/issues/158) | Neo4j suspendTransaction runBlocking | Open | `runBlocking` removed; async Neo4j driver or `withContext` bridge used. |
| 7 | [graph #156](https://github.com/bluetape4k/bluetape4k-graph/issues/156) | FalkorDB graphExists cancellation fix | Open | `runCatching{}` replaced; suspend function propagates cancellation correctly. |
| 8 | [exposed #162](https://github.com/bluetape4k/bluetape4k-exposed/issues/162) | AbstractJdbcCaffeineRepository.findAll() | Open | `runCatching{}` replaced with logged catch; cache warming failure visible in logs. |
| 9 | [aws #59](https://github.com/bluetape4k/bluetape4k-aws/issues/59) | KMS field encryption | Open | Public annotation/property API is designed, implemented, documented, and tested. |
| 5 | [graph #113](https://github.com/bluetape4k/bluetape4k-graph/issues/113) | Neptune research | Open | Local testability and implementation strategy are recorded before `graph #30`. |
| 6 | [exposed #30](https://github.com/bluetape4k/bluetape4k-exposed/issues/30) | CockroachDB foundation | Open | Scaffolding and Testcontainers smoke test land. |
| 7 | [exposed #31](https://github.com/bluetape4k/bluetape4k-exposed/issues/31) | CockroachDB dialect | Open | PostgreSQL compatibility and DDL differences are codified. |
| 8 | [exposed #32](https://github.com/bluetape4k/bluetape4k-exposed/issues/32) | CockroachDB retries | Open | Serializable transaction retry guidance and regressions land. |
| 9 | [aws #10](https://github.com/bluetape4k/bluetape4k-aws/issues/10) / [#11](https://github.com/bluetape4k/bluetape4k-aws/issues/11) | AWS Ktor foundation | Open | SQS and DynamoDB Ktor server patterns compile and test. |
| 10 | [graph #111](https://github.com/bluetape4k/bluetape4k-graph/issues/111) | Graph examples | Open | `graph-io` backed sample dataset loaders are available for domain examples. |

## Recommended WIP Limits

| Lane | Limit | Active candidates |
|---|---:|---|
| Correctness / bug fix | 3 active items | `exposed #161`+`#163` (P0/P1) first; then `leader #305/#306` + `graph #158` |
| Resource safety | 1 active item | `projects #542` (close leak) alongside correctness lane |
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

#156 FalkorDB graphExists() CancellationException fix
#157 FalkorDB/Memgraph SchemaManager broad runCatching fix
  -> correctness baseline for graph-falkordb and graph-memgraph

#158 Neo4jGraphSuspendOperations.suspendTransaction() runBlocking inside withContext(IO) (P1)
  -> IO thread starvation under concurrent transaction load
  -> long-term: migrate to async Neo4j driver
```

### Exposed

```text
#7 QueryLookupStrategy (closed)
#8 serializer parity (closed by PR #21)
#6 AuditableR2dbcRepository (closed by PR #22)
  -> #26 R2DBC @Query parity
  -> #4 bucket4j
  -> #5 Spring Modulith integration

#119 runCatching{} in close() swallows CancellationException
#161 R2DBC write-behind finally block — data loss on cancellation (P0)
  -> fix #161 first (NonCancellable in finally)
  -> then fix #163 (close() waits for job before scope.cancel())
  -> related: #120 non-atomic cache miss handling

#162 AbstractJdbcCaffeineRepository.findAll() runCatching{} swallows cache errors (P1)
  -> independent of #161; fix in same PR or separately

#163 AbstractR2dbcCaffeineRepository.close() race — scope cancelled before flush (P1)
  -> depends on #161 being fixed first

#24 CockroachDB epic
  -> #30 scaffolding and smoke test
  -> #31 PostgreSQL compatibility and DDL differences
  -> #32 serializable transaction retry guidance

#25 Trino Phase 2 epic
  -> #27 DataSource connection
  -> #28 streaming/paged query API
  -> #29 batch insert/write path
```

### Leader

```text
#304 runCatching{} CancellationException suppression in ExposedJdbc lock/elector (P1)
  -> fix before expanding leader-exposed-jdbc
  -> related: #271 runBlocking bridges removal

#305 ExposedJdbcLock.tryLock() currentTimeMillis() → nanoTime() (P1)
#306 ExposedJdbcGroupLock.tryLock() same deadline bug (P1)
  -> fix #305 and #306 together in one PR
  -> monotonic clock required for reliable lock timeout in cloud environments

#269 remove @Deprecated APIs after 0.1.0 GA
#270 promote StringTruncateSupport
#271 replace runBlocking bridges with suspend interface
  -> unblocked after #304

#228 leader-dynamodb DynamoDB backend
#229 k8s operator leader pattern example
#231 K3sServer + Lease-based integration example
```

### Projects

```text
#475 remove !! operator (86 sites in production code)
  -> ongoing; do not start new modules using !!

#491 PropsMapper nullable numeric bug
#539 remove deprecated BinaryKafkaCodecs — JDK RCE (P1)
  -> audit usages -> escalate to ERROR -> remove
  -> related: #492 serialization trust profiles

#540 GrpcServer / AbstractGrpcServer lifecycle tests (P1)
  -> core infrastructure; zero test coverage currently

#541 FutureToCompletableFutureWrapper virtual thread per object (P2)
  -> replace with shared Executors.newVirtualThreadPerTaskExecutor()

#542 ResilientNearCacheDecorator.close() swallows exception silently (P1)
  -> replace runCatching{} with logged try/catch
  -> check ResilientSuspendNearCacheDecorator for same pattern
```

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
      -> #145 S3 listObjectsV2 auto-pagination Flow extension (P2)
           -> implement listAllObjects() using SDK v2 paginator
           -> after #59 KMS work; both are aws-coroutine API additions

#3 Spring Boot DynamoDB (closed by PR #31)
  -> #14 Spring Boot DynamoDB example
  -> #11 Ktor DynamoDB conventions
      -> #17 Ktor DynamoDB example

#10 Ktor SQS
  -> #16 Ktor SQS example
```
