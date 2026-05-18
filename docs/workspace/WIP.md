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

**New issues registered on 2026-05-18 (round 3 — qmd-backed projects audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [projects #543](https://github.com/bluetape4k/bluetape4k-projects/issues/543) | projects | bug: BehaviorSubject.emitError aborts notification on collector cancellation | P1 |
| [projects #544](https://github.com/bluetape4k/bluetape4k-projects/issues/544) | projects | perf: evaluate FlowEvent value-class wrappers for Kotlin 2 hot paths | P2 |

**New issues registered on 2026-05-18 (round 4 — qmd-backed aws audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [aws #147](https://github.com/bluetape4k/bluetape4k-aws/issues/147) | aws | bug: forceDeleteBucket cannot empty versioned S3 buckets | P1 |

**New issues registered on 2026-05-18 (round 5 — qmd-backed exposed audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [exposed #165](https://github.com/bluetape4k/bluetape4k-exposed/issues/165) | exposed | bug: ExposedJdbcBatchJobRepository retry path can throw NoSuchElementException | P2 |

**New issues registered on 2026-05-18 (round 6 — qmd-backed leader audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [leader #308](https://github.com/bluetape4k/bluetape4k-leader/issues/308) | leader | bug: Mongo locks use wall-clock deadlines for tryLock timeout | P1 |
| [leader #309](https://github.com/bluetape4k/bluetape4k-leader/issues/309) | leader | bug: Lettuce lock and slot acquisition use wall-clock deadlines | P1 |

**New issues registered on 2026-05-18 (round 7 — qmd-backed graph audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [graph #160](https://github.com/bluetape4k/bluetape4k-graph/issues/160) | graph | bug: AGE, Memgraph, and TinkerGraph suspendTransaction still bridge through runBlocking | P1 |

**New issues registered on 2026-05-18 (round 8 — qmd-backed image audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [image #61](https://github.com/bluetape4k/bluetape4k-image/issues/61) | image | chore: remove typo compatibility APIs before 0.1.x stabilization | P2 |

**New issues registered on 2026-05-18 (round 9 — qmd-backed javers audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [javers #62](https://github.com/bluetape4k/bluetape4k-javers/issues/62) | javers | bug: persistent JaVers repositories lose head commit across rebuilds | P1 |

**New issues registered on 2026-05-18 (round 10 — qmd-backed text audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [text #67](https://github.com/bluetape4k/bluetape4k-text/issues/67) | text | bug: matchesAsFlow materializes all Aho-Corasick matches before emitting | P1 |

**New issues registered on 2026-05-18 (round 11 — qmd-backed dependencies audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [dependencies #39](https://github.com/bluetape4k/bluetape4k-dependencies/issues/39) | dependencies | bug: sync-dependabot-ignores default workspace is one directory too high | P1 |

**New issues registered on 2026-05-18 (round 12 — qmd-backed experimental audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [experimental #45](https://github.com/bluetape4k/bluetape4k-experimental/issues/45) | experimental | bug: CI and Nightly run on JDK 21 while the repo contract is Java 25 | P1 |

**New issues registered on 2026-05-18 (round 13 — qmd-backed workshop audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [workshop #120](https://github.com/bluetape4k/bluetape4k-workshop/issues/120) | workshop | bug: R2DBC WebFlux tests stay disabled after manual schema workaround | P2 |

**New issues registered on 2026-05-18 (round 14 — qmd-backed exposed-workshop audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [exposed-workshop #70](https://github.com/bluetape4k/exposed-workshop/issues/70) | exposed-workshop | bug: routing datasource registry does not close tenant Hikari pools | P2 |

**New issues registered on 2026-05-18 (round 15 — qmd-backed exposed-r2dbc-workshop audit):**

| Issue | Repo | Title | Severity |
|-------|------|-------|----------|
| [exposed-r2dbc-workshop #54](https://github.com/bluetape4k/exposed-r2dbc-workshop/issues/54) | exposed-r2dbc-workshop | bug: withTables can swallow coroutine cancellation during cleanup | P2 |

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

4. **AWS S3 correctness is newly active.**
   `aws #147` fixes a real bucket-cleanup contract gap for versioned buckets;
   treat it as the AWS correctness lane before more S3 examples.

5. **JaVers Redis persistence needs a restart-safety fix.**
   `javers #62` covers persistent Redis-backed repositories whose stored
   snapshots survive rebuilds while `getHeadId()` remains memory-only.

6. **Text-search Flow contract is active.**
   `text #67` fixes or documents the gap between `matchesAsFlow()` streaming
   claims and its eager `parseText(text)` materialization.

7. **Dependency governance checks must not silently no-op.**
   `dependencies #39` fixes the default workspace for Dependabot ignore sync
   before more central version upgrades.

8. **Experimental CI must validate the Java 25 contract.**
   `experimental #45` aligns CI/Nightly runtime with the repository's Java 25
   proving-ground role before promotion work.

9. **Workshop R2DBC tests must pass for real, not pending.**
   `workshop #120` restores `spring-data/r2dbc-webflux` coverage before adding
   more Spring Data R2DBC examples.

10. **Exposed workshop routing datasource must own pool shutdown.**
   `exposed-workshop #70` fixes the example-level Hikari lifecycle gap before
   expanding routing datasource variants.

11. **Exposed R2DBC workshop shared tests must preserve cancellation.**
   `exposed-r2dbc-workshop #54` fixes shared `withTables()` cleanup before
   expanding multi-database R2DBC examples.

12. **Graph Neptune needs research before implementation.**
   Do `graph #113` before `graph #30`; keep examples such as `graph #111` after
   the backend/testability decision is clear.

13. **Exposed CockroachDB remains the strongest foundation lane.**
   Start with `exposed #30`, then continue `#31` and `#32`.

14. **AWS database adapters and examples follow foundation/API decisions.**
   Continue `aws #74` before `#75/#76/#77`, then use `#82` for adoption examples.

## Selected Next Work

Use this as the immediate working set.

| Order | Work | Lane | Status | Stop condition |
|---:|---|---|---|---|
| 1 | [exposed #161](https://github.com/bluetape4k/bluetape4k-exposed/issues/161) | R2DBC write-behind finally NonCancellable | Open | `finally` block wraps `flushBatch()` in `withContext(NonCancellable)`; regression test added. |
| 2 | [exposed #163](https://github.com/bluetape4k/bluetape4k-exposed/issues/163) | R2DBC write-behind close() race | Open | `close()` waits for `writeBehindJob.join()` before `scope.cancel()`; tested with slow flush. |
| 3 | [projects #542](https://github.com/bluetape4k/bluetape4k-projects/issues/542) | ResilientNearCacheDecorator.close() leak | Open | `runCatching{}` replaced with logged try/catch; resource leak verified absent. |
| 4 | [projects #543](https://github.com/bluetape4k/bluetape4k-projects/issues/543) | BehaviorSubject emitError cancellation | Open | Parent cancellation still propagates, but collector-local cancellation does not abort remaining terminal notifications. |
| 5 | [leader #304](https://github.com/bluetape4k/bluetape4k-leader/issues/304) | ExposedJdbc CancellationException fix | Open | All 6 `runCatching{}` sites replaced with explicit rethrow; tests pass. |
| 6 | [leader #305](https://github.com/bluetape4k/bluetape4k-leader/issues/305) / [#306](https://github.com/bluetape4k/bluetape4k-leader/issues/306) | ExposedJdbc[Group]Lock nanoTime fix | Open | All `currentTimeMillis()` deadline sites replaced with `nanoTime()`; lock timeout verified monotonic. |
| 7 | [leader #308](https://github.com/bluetape4k/bluetape4k-leader/issues/308) / [#309](https://github.com/bluetape4k/bluetape4k-leader/issues/309) | Mongo/Lettuce monotonic timeout fixes | Open | Blocking/async/suspend acquisition loops use monotonic wait budgets. |
| 8 | [graph #158](https://github.com/bluetape4k/bluetape4k-graph/issues/158) / [#160](https://github.com/bluetape4k/bluetape4k-graph/issues/160) | suspendTransaction runBlocking bridges | Open | `runBlocking` removed from suspend transaction paths; cancellation does not pin IO workers. |
| 9 | [graph #156](https://github.com/bluetape4k/bluetape4k-graph/issues/156) | FalkorDB graphExists cancellation fix | Open | `runCatching{}` replaced; suspend function propagates cancellation correctly. |
| 10 | [javers #62](https://github.com/bluetape4k/bluetape4k-javers/issues/62) | Persistent repository head restoration | Open | Lettuce/Redisson rebuild regression keeps `headId` aligned with persisted commit metadata. |
| 11 | [text #67](https://github.com/bluetape4k/bluetape4k-text/issues/67) | Aho-Corasick Flow eager materialization | Open | `matchesAsFlow()` either streams with early cancellation or its public contract is corrected. |
| 12 | [dependencies #39](https://github.com/bluetape4k/bluetape4k-dependencies/issues/39) | Dependabot ignore sync default workspace | Open | Default run discovers sibling repos or fails loudly when no target files are found. |
| 13 | [experimental #45](https://github.com/bluetape4k/bluetape4k-experimental/issues/45) | Java 25 CI/Nightly contract | Open | CI/Nightly run on JDK 25 or include an explicit Java 25 verification lane. |
| 14 | [workshop #120](https://github.com/bluetape4k/bluetape4k-workshop/issues/120) | R2DBC WebFlux disabled tests | Open | Targeted test command reports real passing tests instead of 44 pending tests. |
| 15 | [exposed-workshop #70](https://github.com/bluetape4k/exposed-workshop/issues/70) | Routing datasource Hikari lifecycle | Open | Registry-owned tenant pools are closed on Spring shutdown; regression test proves cleanup. |
| 16 | [exposed-r2dbc-workshop #54](https://github.com/bluetape4k/exposed-r2dbc-workshop/issues/54) | `withTables()` cancellation cleanup | Open | CancellationException propagates from shared suspend cleanup; ordinary cleanup failures remain visible. |
| 17 | [exposed #162](https://github.com/bluetape4k/bluetape4k-exposed/issues/162) | AbstractJdbcCaffeineRepository.findAll() | Open | `runCatching{}` replaced with logged catch; cache warming failure visible in logs. |
| 18 | [exposed #165](https://github.com/bluetape4k/bluetape4k-exposed/issues/165) | JDBC batch retry missing-row failure | Open | Unique-violation re-query uses `firstOrNull()` with explicit diagnostic failure instead of `.first()`. |
| 19 | [aws #147](https://github.com/bluetape4k/bluetape4k-aws/issues/147) | S3 versioned bucket force delete | Open | Versioned object versions/delete markers are removed or unsupported versioning is explicitly rejected. |
| 20 | [aws #74](https://github.com/bluetape4k/bluetape4k-aws/issues/74) | Exposed-first AWS database foundation | Open | Shared database properties and named registry contract land before framework adapters. |
| 21 | [graph #113](https://github.com/bluetape4k/bluetape4k-graph/issues/113) | Neptune research | Open | Local testability and implementation strategy are recorded before `graph #30`. |
| 22 | [exposed #30](https://github.com/bluetape4k/bluetape4k-exposed/issues/30) | CockroachDB foundation | Open | Scaffolding and Testcontainers smoke test land. |
| 23 | [exposed #31](https://github.com/bluetape4k/bluetape4k-exposed/issues/31) | CockroachDB dialect | Open | PostgreSQL compatibility and DDL differences are codified. |
| 24 | [exposed #32](https://github.com/bluetape4k/bluetape4k-exposed/issues/32) | CockroachDB retries | Open | Serializable transaction retry guidance and regressions land. |
| 25 | [image #61](https://github.com/bluetape4k/bluetape4k-image/issues/61) | Image API typo/deprecation cleanup | Open | Typo aliases are removed or documented with removal targets before 0.1.x API stabilization. |
| 26 | [graph #111](https://github.com/bluetape4k/bluetape4k-graph/issues/111) | Graph examples | Open | `graph-io` backed sample dataset loaders are available for domain examples. |

## Recommended WIP Limits

| Lane | Limit | Active candidates |
|---|---:|---|
| Correctness / bug fix | 3 active items | `exposed #161`+`#163` (P0/P1) first; then `leader #305/#306`, `graph #158`, `javers #62`, `text #67`, `dependencies #39`, or `experimental #45` |
| Resource safety | 1 active item | `projects #542` (close leak) alongside correctness lane |
| Research/design | 1 active item | `graph #113` before `graph #30`; `aws #74` needs design-level review |
| New implementation | 1 repo at a time | Prefer `aws #147`, `aws #74`, or `exposed #30`; do not start multiple foundation lanes simultaneously |
| Follow-up implementation | 2 ready items | `exposed #31/#32` only after `#30`; AWS `#75/#76/#77` only after `#74` |
| Examples/adoption | 1 ready item | `graph #111` or `aws #82` after their foundations are stable |

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

#3 Spring Boot DynamoDB (closed by PR #31)
  -> #14 Spring Boot DynamoDB example
  -> #11 Ktor DynamoDB conventions
      -> #17 Ktor DynamoDB example

#10 Ktor SQS
  -> #16 Ktor SQS example

#145 S3 listObjectsV2 auto-pagination Flow extension
  -> #147 forceDeleteBucket versioned bucket cleanup
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

#160 AGE/Memgraph/TinkerGraph suspendTransaction() runBlocking inside suspend path (P1)
  -> align fix strategy with #158 across remaining suspend backends
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

#165 ExposedJdbcBatchJobRepository retry path can throw NoSuchElementException (P2)
  -> align JDBC catch-and-retry missing-row behavior with R2DBC #117 fix

#24 CockroachDB epic
  -> #30 scaffolding and smoke test
  -> #31 PostgreSQL compatibility and DDL differences
  -> #32 serializable transaction retry guidance

#25 Trino Phase 2 epic
  -> #27 DataSource connection
  -> #28 streaming/paged query API
  -> #29 batch insert/write path
```

### JaVers

```text
#62 persistent Redis repository head restoration (P1)
  -> Lettuce/Redisson rebuild tests must preserve headId from stored metadata
  -> fix before expanding Redis-backed production examples

#3 javers-exposed JDBC repository
  -> #4 javers-ddd AggregateRoot / DomainEvent helpers
      -> #5 examples/javers-exposed-ddd CQRS / Event Sourcing demo
```

### Text

```text
#67 matchesAsFlow eager materialization (P1)
  -> fix streaming implementation or correct the public Flow contract
  -> preserve Aho-Corasick match ordering and offset behavior
```

### Dependencies

```text
#39 sync-dependabot-ignores default workspace bug (P1)
  -> governance checks discover sibling repositories by default
  -> then #34 MyBatis Dynamic SQL 2.x and #35 Timefold Solver 2.x upgrades
```

### Experimental

```text
#45 CI/Nightly JDK 21 vs Java 25 repo contract (P1)
  -> align workflow runtime or add an explicit Java 25 verification lane
  -> keep promotion work blocked until Java 25 behavior is actually checked
```

### Workshop

```text
#120 R2DBC WebFlux disabled tests (P2)
  -> wire deterministic schema/data initialization
  -> remove broad @Disabled from service/controller/handler integration tests
  -> targeted Gradle test should report passing tests, not pending tests
```

### Exposed Workshop

```text
#70 routing datasource Hikari lifecycle (P2)
  -> close registry-owned tenant pools on Spring shutdown
  -> apply same ownership rule before #49 Ktor routing datasource example
```

### Exposed R2DBC Workshop

```text
#54 withTables cancellation-safe cleanup (P2)
  -> rethrow CancellationException from suspend cleanup paths
  -> shared baseline before broad R2DBC multi-database example expansion
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

#308 MongoLock / MongoSuspendLock currentTimeMillis() deadline bug (P1)
#309 Lettuce lock and slot currentTimeMillis() deadline bug (P1)
  -> apply the same monotonic wait-budget rule across blocking/async/suspend acquisition loops

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
