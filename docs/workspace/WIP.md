# bluetape4k WIP

Snapshot: 2026-05-10 KST
Scope: GitHub `bluetape4k/*` repositories, issues assigned to `debop`, created on or after 2026-01-01.
Open count after refresh: 73 issues.

This root queue is the ecosystem-level view. Repo-local details live in each
project `WIP.md` and should stay aligned with this file.

## Refresh Notes

Verified against GitHub on 2026-05-10 KST.

Recently completed and removed from active work:

- `projects #333` cache module reorganization
- `dependencies #8` first official Spring Boot alias policy
- `exposed #3`, `#7`
- `graph #13`, `#32`, `#34`
- `aws #8`
- `leader #73`, `#77`

Implemented and waiting for PR merge:

- `exposed #8` -> PR #21 `[fix] Align exposed-fastjson2 serializer facade` (issue already closed)
- `exposed #6` -> PR #22 `[feat] Add AuditableR2dbcRepository`
- `graph #33` -> PR #78 `[feat] Add batch insert API and backend implementations`

Open PRs to watch:

- `bluetape4k-exposed` PR #21, #22
- `bluetape4k-graph` PR #78
- `exposed-workshop` PR #20
- `exposed-r2dbc-workshop` PR #11

## Reading Guide

Priority is assigned from the whole bluetape4k ecosystem view, not from
single-repo local value.

| Priority | Meaning |
|---|---|
| P0 | Direction-setting work or merge blockers that keep the queue honest. |
| P1 | Foundation or correctness work that unlocks multiple downstream issues. |
| P2 | Valuable feature work after the foundations are stable. |
| P3 | Examples, docs, benchmarks, and adoption work. |
| P4 | Explicitly deferred, low leverage, or decision-only work. |

Difficulty is a planning estimate:

| Difficulty | Meaning |
|---|---|
| S | Small, isolated, likely one focused PR. |
| M | Medium, local design and tests required. |
| L | Large, multi-module or backend-specific implementation. |
| XL | Cross-repo, breaking, or program-level work. |

## Executive Queue

Do these in order unless a production blocker appears.

1. **Close merge-waiting work before opening more WIP.**
   `exposed #8`, `exposed #6`, and `graph #33` already have clean PRs. Keep
   them linked and merge/close before starting another broad backend feature
   when possible.

2. **Continue AWS foundations now that S3 is merged.**
   `aws #8` is closed by PR #27, `aws #9` is closed by PR #28, and
   `aws #1` is closed by PR #29. Continue with Spring Boot SQS/DynamoDB
   (`#2/#3`), then Ktor SQS/DynamoDB (`#10/#11`) or the newly unblocked
   examples (`#12/#15`).

3. **Continue leader lease safety with the remaining Redis group gap.**
   `leader #73/#77` are closed. The new concrete gap is `leader #151`, then
   `#79/#74` can build on the settled lease semantics.

4. **Keep examples behind their owning APIs.**
   AWS, graph, leader, image, JaVers, and workshop examples should wait until
   the corresponding foundation issue closes or has a merged PR.

## Selected Next Work

Use this as the immediate working set.

| Order | Work | Lane | Status | Stop condition |
|---:|---|---|---|---|
| 1 | [exposed #8](https://github.com/bluetape4k/bluetape4k-exposed/issues/8) | Serializer correctness | PR #21 open, CI passed; issue already closed | PR merges so code and issue state match. |
| 2 | [exposed #6](https://github.com/bluetape4k/bluetape4k-exposed/issues/6) | R2DBC foundation | PR #22 open, CI passed | PR merges and issue closes. |
| 3 | [graph #33](https://github.com/bluetape4k/bluetape4k-graph/issues/33) | Graph foundation | PR #78 open, CI passed | PR merges and issue closes. |
| 4 | [leader #151](https://github.com/bluetape4k/bluetape4k-leader/issues/151) | Leader lease safety | Ready; replaces Redis group gap from `#77` | Lettuce/Redisson group minLeaseTime uses slot-token TTL semantics. |
| 5 | [aws #2](https://github.com/bluetape4k/bluetape4k-aws/issues/2) | AWS Spring foundation | Ready | Spring Boot SQS listener/template is implemented and covered. |
| 6 | [aws #3](https://github.com/bluetape4k/bluetape4k-aws/issues/3) | AWS Spring foundation | Ready | DynamoDB coroutine repository foundation is implemented and covered. |
| 7 | [aws #12](https://github.com/bluetape4k/bluetape4k-aws/issues/12) / [#15](https://github.com/bluetape4k/bluetape4k-aws/issues/15) | AWS examples | Unblocked by PR #29 / #28 merge | Examples compile/test in Nightly. |

If excluding merge-waiting items, the next three implementation candidates are
`leader #151`, `aws #2`, and `aws #3`.

## Recommended WIP Limits

| Lane | Limit | Active candidates |
|---|---:|---|
| Merge wait | 3 | `exposed #8`, `exposed #6`, `graph #33` |
| Architecture / repo split | 1 XL item | `projects #257`; `projects #262` remains deferred |
| AWS foundation | 1 L item | `aws #2/#3`, then `#10/#11`; `#12/#15` are unblocked examples |
| Leader safety | 1 L item | `leader #151`, then `#79/#74` |
| Examples/docs | 2 S/M items | only after their owning core issue is closed |

## Dependency Map

### Repository Architecture

```text
projects #280 policy decision (closed)
  -> dependencies #8 first official Spring Boot alias policy (closed)
  -> projects #263 spring-boot3 removal + spring-boot4 -> spring-boot rename (closed)
      -> exposed #3 spring-boot3 removal + spring-boot4 -> spring-boot rename (closed)
  -> projects #110 infra deprecated inventory (closed)
  -> projects #257 monorepo split tracker
      -> projects #262 data repo split (deferred)
```

### AWS

```text
aws #8 SigV4 plugin (closed)
  -> aws #9 Ktor S3 client (closed by PR #28)
      -> aws #15 Ktor S3 example (unblocked; PR #28 seeded a compile-tested module)

aws #1 Spring Boot S3 (closed by PR #29)
  -> aws #12 Spring Boot S3 example (unblocked)
  -> image #5 S3/CDN/Spring Boot integration

aws #2 Spring Boot SQS
aws #4 Spring Boot SNS
  -> aws #13 Spring Boot SQS/SNS example

aws #3 Spring Boot DynamoDB
  -> aws #14 Spring Boot DynamoDB example
  -> aws #11 Ktor DynamoDB conventions
      -> aws #17 Ktor DynamoDB example

aws #10 Ktor SQS
  -> aws #16 Ktor SQS example
```

### Graph

```text
graph #13 transaction DSL (closed)
graph #32 schema/index API (closed)
graph #34 merge/upsert (closed)
graph #33 batch insert (PR #78 open)
  -> graph #30 Neptune backend
  -> graph #10 extra example modules
      -> workshop #11 knowledge graph
      -> workshop #12 fraud detection
      -> workshop #13 recommendation

graph #40 weighted path suspend tests
  -> graph #41 weighted path benchmark

graph #17/#18/#19 repository automation
  -> safer large graph changes
```

### Leader

```text
leader #73 watchdog / lease auto-extend (closed)
leader #77 minLeaseTime backend TTL delegation (closed)
  -> leader #151 Redis group minLeaseTime slot-token TTL
      -> leader #79 explicit lease extension API
      -> leader #74 Flux/Flow support

leader #39 useDbTime
  -> depends on Exposed JDBC/R2DBC backend maturity

leader #50 audit contract
leader #72 @LeaderGroupElection leaderId
  -> operational examples and metrics polish
```

### Image / JaVers / Workshop

```text
image #4 CAPTCHA
image #1 OCR
image #2 face/object detection
  -> image #3 classification, if model/runtime packaging is settled

aws #1 Spring Boot S3 (closed by PR #29)
  -> image #5 S3/CDN/Spring Boot integration

javers #3 Exposed snapshot repository
  -> javers #4 DDD helpers
      -> javers #5 CQRS/Event Sourcing example

graph #10 / leader #36
  -> workshop graph/leader runnable examples
```

## Active Priority Backlog

### P0 - Direction And Merge Hygiene

| Issue | Difficulty | Impact | Notes |
|---|---:|---|---|
| [projects #257](https://github.com/bluetape4k/bluetape4k-projects/issues/257) | XL | High | Program tracker for split-repo strategy; keep updated as phases close. |
| [exposed #8](https://github.com/bluetape4k/bluetape4k-exposed/issues/8) | S | Medium | PR #21 open and CI passed; issue is already closed. |
| [exposed #6](https://github.com/bluetape4k/bluetape4k-exposed/issues/6) | M | Medium | PR #22 open; keep out of new implementation queue until merged. |
| [graph #33](https://github.com/bluetape4k/bluetape4k-graph/issues/33) | L | High | PR #78 open; unlocks graph examples/Neptune after merge. |

### P1 - Foundation Work

| Issue | Difficulty | Impact | Notes |
|---|---:|---|---|
| [aws #2](https://github.com/bluetape4k/bluetape4k-aws/issues/2) | L | High | Spring Boot SQS listener/template. |
| [aws #3](https://github.com/bluetape4k/bluetape4k-aws/issues/3) | L | High | DynamoDB coroutine repository foundation. |
| [leader #151](https://github.com/bluetape4k/bluetape4k-leader/issues/151) | L | High | Redis group slot-token TTL redesign for `minLeaseTime`. |
| [leader #79](https://github.com/bluetape4k/bluetape4k-leader/issues/79) | M | High | Explicit lease extension API after lease semantics settle. |
| [leader #74](https://github.com/bluetape4k/bluetape4k-leader/issues/74) | L | High | Flux/Flow support should build on watchdog/minLeaseTime semantics. |

### P2 - Feature Expansion

| Issue | Difficulty | Impact | Notes |
|---|---:|---|---|
| [exposed #4](https://github.com/bluetape4k/bluetape4k-exposed/issues/4) | L | Medium | Bucket4j + Exposed; do after R2DBC PRs merge. |
| [exposed #5](https://github.com/bluetape4k/bluetape4k-exposed/issues/5) | L | Medium | Spring Modulith integration. |
| [graph #17](https://github.com/bluetape4k/bluetape4k-graph/issues/17) | M | Medium | Build cache optimization. |
| [graph #18](https://github.com/bluetape4k/bluetape4k-graph/issues/18) | M | Medium | CI quality gates. |
| [graph #19](https://github.com/bluetape4k/bluetape4k-graph/issues/19) | S | Medium | Dependabot/Renovate. |
| [graph #49](https://github.com/bluetape4k/bluetape4k-graph/issues/49) | L | Medium | graph-okio encrypted streaming. |
| [image #4](https://github.com/bluetape4k/bluetape4k-image/issues/4) | M | Medium | Self-contained CAPTCHA module. |
| [javers #3](https://github.com/bluetape4k/bluetape4k-javers/issues/3) | L | Medium | Exposed snapshot repository, prerequisite for JaVers lane. |
| [projects #149](https://github.com/bluetape4k/bluetape4k-projects/issues/149) | M | Medium | Vector utilities foundation. |
| [projects #151](https://github.com/bluetape4k/bluetape4k-projects/issues/151) | L | Medium | LLM/vector Testcontainers support. |

### P3 - Examples, Docs, Benchmarks

Examples and benchmark work remains valuable but should follow the owning core
APIs unless the issue is explicitly independent:

- `projects #323/#324/#325` can be one small docs PR.
- `graph #40` should precede `graph #41`.
- `aws #12/#15` are unblocked by S3 merges; `#13/#14/#16/#17` still wait for their service integrations.
- `workshop #9/#10/#11/#12/#13` wait for graph/leader foundations.
