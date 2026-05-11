# AGENTS.md - bluetape4k Workspace Root

This directory is the local workspace for the bluetape4k GitHub organization.
Each child directory is an independent Git repository. This file applies to all
repositories below this directory; repo-local `AGENTS.md` files add narrower
rules and take precedence inside their own repo.

Keep conversations with the user in Korean. Keep agent-facing guidance such as
`AGENTS.md` in concise English unless a repo-local document explicitly requires
Korean wording.

## Repositories

### bluetape4k libraries

| Directory | Purpose |
|---|---|
| `bluetape4k-projects/` | Core Kotlin/JVM backend libraries: core, coroutines, data, infra, Spring Boot 3/4, virtual threads |
| `bluetape4k-experimental/` | Experimental Kotlin 2.3 + Java 25 + Spring Boot 4 modules; unpublished |
| `bluetape4k-exposed/` | JetBrains Exposed extensions: JDBC/R2DBC repositories, cache, serialization, Spring Boot auto-config |
| `bluetape4k-aws/` | AWS SDK v2 and AWS Kotlin SDK wrappers with coroutines, Spring Boot 4, Ktor 3 |
| `bluetape4k-image/` | Image processing with scrimage and libvips backends |
| `bluetape4k-javers/` | Javers audit/diff with Redis, Kafka, and Exposed integration |
| `bluetape4k-leader/` | Distributed leader election APIs: blocking, async, coroutine, virtual-thread; Redis backend |
| `bluetape4k-text/` | Korean/Japanese tokenizers, language detection, Aho-Corasick search |
| `bluetape4k-graph/` | Graph DB integrations: Neo4j, Memgraph, AGE, TinkerPop, FalkorDB |
| `bluetape4k-dependencies/` | BOM for coordinated bluetape4k ecosystem versions |

### Workshops and examples

| Directory | Purpose |
|---|---|
| `bluetape4k-workshop/` | Backend examples using bluetape4k libraries |
| `exposed-workshop/` | JetBrains Exposed ORM examples |
| `exposed-r2dbc-workshop/` | Exposed R2DBC examples |
| `ocean-workshop/` | Ocean/weather data visualization with Kotlin, Spring Boot 4, bluetape4k |
| `clinic-appointment/` | Clinic appointment example app |
| `timefold-workshop/` | Timefold Solver workshop |
| `kotlin-dev-agent/` | Kotlin development agent experiment |

## Shared Stack

- Kotlin 2.3+.
- Java 21 for core repos; Java 25 for experimental and several newer repos.
- Gradle multi-module builds, usually registered by `settings.gradle.kts` helper functions.
- Spring Boot 3.x for older/core modules; Spring Boot 4.x for newer/experimental modules.
- Kotlin coroutines first for async work.
- Tests: JUnit 5, MockK, bluetape4k-assertions, Testcontainers singleton launchers.
- Common compiler flags: `-Xjsr305=strict`, `-jvm-default=enable`,
  `-Xinline-classes`, `-Xcontext-parameters`.

## Mandatory Kotlin Workflow

Before editing a Kotlin class, inspect references and impact when tools are
available (`ide_find_references`, `get_impact_radius_tool`, or equivalent).

After editing any `.kt` file:

1. Run IDE diagnostics when available.
2. Fix import errors with IDE import optimization when available.
3. Resolve `@Deprecated` warnings with an appropriate quick fix; do not leave
   unresolved deprecation warnings in touched code.
4. Compile and test only after diagnostics are clean.

## Core Design Rules

### Validation and exception types

- `assertXxx()` means `AssertionError` for internal invariants. Do not use it in
  new code.
- `requireXxx()` means `IllegalArgumentException` for caller input validation.
  Prefer bluetape4k `require*` extensions.
- Do not change existing exception types casually; tests often depend on them.

```kotlin
fun add(keyword: String): Builder = apply {
    keyword.requireNotBlank("keyword")
}
```

### Coroutines

- Prefer Kotlin coroutines for async work.
- Wrap blocking APIs in `withContext(Dispatchers.IO)`.
- Do not use `runBlocking` in production code except tightly controlled lazy
  initialization.
- Always rethrow `CancellationException` before broad exception handling.
- Do not use `runCatching {}` around suspend calls; it can swallow cancellation.

```kotlin
try {
    doSomething()
} catch (e: CancellationException) {
    throw e
} catch (e: Exception) {
    log.warn(e) { "Operation failed" }
}
```

### Virtual threads

Do not use `@Synchronized` or `synchronized {}` in virtual-thread-aware code.
Use `reentrantLock()` or another explicit concurrency primitive.

### AtomicFU

Use atomicfu only for class-level properties. For local variables in tests or
functions, use `java.util.concurrent.atomic.*`.

### Null safety and immutability

- Do not use `!!`.
- Prefer `?.`, `?:`, and explicit `requireNotNull`/`require*` validation.
- Prefer `val`.
- Return new instances instead of mutating existing state.
- Model options/state as `data class` values.

### Same-type parameters

Wrap two or more same-typed parameters in a named data class to avoid positional
mistakes.

```kotlin
data class AspectRatio(val width: Int, val height: Int)
fun smartCrop(ratio: AspectRatio): Image
```

## Tests

- Use JUnit 5, MockK, and bluetape4k-assertions.
- Add `@TestInstance(TestInstance.Lifecycle.PER_CLASS)` to test base classes.
- Use `runTest` for suspend tests.
- Use descriptive backtick test names.
- Prefer bluetape4k-assertions comparison matchers over boolean assertions.
- Use `assertFailsWith<T> { }` for exception checks.
- Use `coInvoking { suspendCall } shouldThrow T::class` only for suspend-specific
  bluetape4k-assertions patterns.
- Do not use JUnit `assertThrows`, `invoking { } shouldThrow`, or
  `kotlin.test.assertFailsWith` in new tests.

For new modules, include:

- `src/test/resources/junit-platform.properties`
- `src/test/resources/logback-test.xml`

Place tests for Kotlin `internal` symbols in the same package path as the source.

## Testcontainers

Do not instantiate `GenericContainer` directly for infrastructure already
wrapped by bluetape4k. Use `XxxServer.Launcher.xxx` singleton patterns from
`bluetape4k-testcontainers`. `@Testcontainers` is usually unnecessary.

```kotlin
abstract class AbstractRedisTest {
    companion object : KLogging() {
        val redis = RedisServer.Launcher.redis
        val redisUrl: String get() = redis.url
    }
}
```

## Public API Documentation

Public classes, interfaces, objects, and extension functions need KDoc in the
style already used by the repo. Include:

- One-line summary.
- Contract/behavior section.
- Kotlin usage example when useful.

## README Rules

For bluetape4k modules, keep English and Korean README files together:

- `README.md`
- `README.ko.md`

Each README must include the language switch directly below the title. Module
README structure should cover architecture, core features, usage examples,
configuration options, and dependency instructions. Mermaid diagrams are
preferred for architecture. Do not use Vega-Lite for README diagrams.

## Project Documentation Artifacts

Store durable project design/history artifacts in repo-local docs paths:

- Specs: `docs/superpowers/specs/YYYY-MM-DD-{slug}-design.md`
- Plans: `docs/superpowers/plans/YYYY-MM-DD-{slug}-plan.md`
- Research notes, when needed: `docs/superpowers/research/YYYY-MM-DD-{slug}-research.md`
- Lessons Learned / work retrospectives: `docs/lessons/YYYY-MM-DD-{slug}.md`
- Use lowercase ASCII kebab-case slugs; include `issue-{number}-` when the
  artifact is tied to a GitHub issue.
- After a large task completes, or when a reusable lesson is identified during
  work, create or update a concise `docs/lessons/YYYY-MM-DD-{slug}.md` entry
  automatically. Include the context, decision, outcome, verification evidence,
  and what future agents should do differently.
- At the end of each substantial workday or multi-task session, consolidate new
  `docs/lessons/` entries: merge duplicates, keep event-specific evidence in the
  lesson, and promote repeatable rules to `AGENTS.md` or the relevant
  skill/reference.
- Treat `.omx/plans`, `.omx/notepad.md`, chat summaries, and runtime notes as
  transient. Promote durable decisions and lessons into `docs/superpowers/` or
  `docs/lessons/`.

## Build and Coverage

- Kover is the standard coverage tool. Do not introduce Jacoco.
- Target 80% production coverage unless integration-heavy modules justify a
  lower threshold.
- Exclude non-production source sets such as `benchmark` and `generated`.
- Do not add ktlint auto-format hooks; use IntelliJ formatting and `.editorconfig`.
- If `.github/workflows/ci.yml` changes, check whether nightly workflow changes
  are also required.

## Spring Boot Auto-Configuration

- If a `compileOnly` type appears in a bean signature, guard it with
  `@ConditionalOnClass(name = ["fqcn"])`.
- Ordering annotations apply only to classes directly registered in
  `AutoConfiguration.imports`; split ordered phases into separate auto-config
  classes and register all of them.
- Use an `INHERIT` sentinel for annotation defaults when a property-level global
  default must be distinguishable from an explicit annotation value.
- Apply `@ConditionalOnProperty` to every auto-configuration phase class, not
  only the entrypoint.

## Exposed 1.2+ Rules

- Import top-level operators such as `eq`, `and`, `less`, `greaterEq`.
- Do not import `SqlExpressionBuilder.eq`; it is an error-level deprecated path.
- Watch for implicit receiver shadowing inside `insert {}`, `update {}`, and
  `deleteWhere {}`; extract locals when column names collide with properties.

## Code Change Checklist

- IDE diagnostics: zero errors and no unresolved deprecations in touched code.
- Compile and test affected modules.
- Update `README.md` and `README.ko.md` when behavior or public API changes.
- Add or update KDoc for new/changed public API.

## Git Workflow

- `develop` is the default integration branch; do not push directly.
- `main` is release-only and updated through `develop -> main` PRs.
- Prefer feature branches under `.worktrees/<branch>`.
- Commits commonly use prefixes such as `feat:`, `fix:`, `refactor:`, `build:`,
  `docs:`, `chore:`, `test:`, `perf:`.
- Korean commit text is acceptable, but keep the intent line concise.

## Workspace Scripts

Prefer the helper scripts in `~/.local/bin` for GitHub, CI, status, diff, log,
and worktree operations before falling back to raw `git`/`gh` commands. They are
designed to keep output compact for agent sessions.

Workspace-level scripts may also live under `bin/`:

| Script | Purpose |
|---|---|
| `all-status` | Cross-repo git status summary |
| `all-pull` | Cross-repo `git pull --rebase`, skipping repos without upstream |
| `all-clean-branches` | Remove gone branches and stale worktrees |
| `all-ci-status` | Latest CI status summary for library repos |

Per-repo helper commands may be available on `PATH`: `repo-status`,
`repo-diff`, `repo-test-summary`, `clean-branches`, `worktree-new`,
`worktree-list`, `ci-status`.

GitHub/CI preference:

- Use `ci-status --limit N` for the current repo's latest GitHub Actions runs.
- Use `ci-status --watch` when asked to monitor an in-progress run.
- Use `all-ci-status` for cross-repo library CI summaries.
- Use `repo-status`, `repo-diff`, and `repo-log` for compact repository context.
- Use `worktree-new` and `worktree-list` for normal worktree operations.
- Use `clean-branches` and `all-clean-branches` only when branch/worktree
  cleanup is explicitly requested, because they delete local branches and remove
  associated worktrees.

## Recommended Skills

- `bluetape4k-patterns`: Kotlin implementation/review rules.
- `bluetape4k-workflow`: classify bluetape4k work type and choose the lightest
  safe lane.
- `design`: new feature, new module, or significant refactor.
- `coroutines-kotlin`: coroutine, Flow, Channel, structured concurrency work.
- `kotlin-spring`: Spring Boot + Kotlin integration.
- `kotlin-expert`: advanced Kotlin API or DSL design.

## GitHub Issue And Pull Request Workflow

When creating GitHub issues or pull requests for bluetape4k repositories,
assign them to `debop` by default unless the user explicitly says otherwise.
Use `--assignee debop` with `gh issue create` and `gh pr create`, or the
equivalent GitHub API `assignees` field. If a repository rejects the assignee,
report that blocker instead of creating an unassigned issue or PR silently.
