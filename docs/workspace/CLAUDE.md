# CLAUDE.md - bluetape4k Workspace Root

This directory is the local workspace for all repositories in the
**bluetape4k GitHub organization**. Each child directory is an independent Git
repository, and repo-local `CLAUDE.md` files may add narrower rules. This file
applies to all repositories below this workspace.

## Document Language Policy (CRITICAL)

Choose the language by primary audience:

| Primary reader | Artifacts | Language |
|---|---|---|
| End user | README locale set | Multilingual |
| Contributor (public, human) | KDoc, GitHub PR/issue/commit, CHANGELOG, release notes | English |
| AI agent | `CLAUDE.md`, `AGENTS.md`, `SKILL.md`, agent memory, notepad | English |
| Engineer (internal human-readable) | `docs/superpowers/specs/`, `docs/superpowers/plans/`, `docs/superpowers/research/`, `docs/lessons/` | Korean OK |

Rules:

- Conversations with the user remain Korean.
- Library-user README documentation is multilingual. Keep `README.md` in
  English, preserve existing localized README files such as `README.ko.md`, and
  allow future locales such as `README.ja.md` or `README.zh.md`.
- README files are not subject to an English-only policy. Do not delete Korean,
  Japanese, Chinese, or other localized README files for policy reasons.
- Public contributor-facing artifacts are English: KDoc, CHANGELOG entries,
  release notes, GitHub issue titles/bodies, GitHub PR titles/bodies, and commit
  messages pushed to GitHub.
- Agent-facing guidance and memory are English: `CLAUDE.md`, `AGENTS.md`,
  `**/SKILL.md`, `~/.claude/projects/**/memory/*.md`,
  `~/.codex/memories/*`, `.omx/notepad.md`, and similar instruction/memory
  surfaces primarily read by AI tools.
- Internal human-readable project artifacts may be Korean:
  `docs/superpowers/specs/`, `docs/superpowers/plans/`,
  `docs/superpowers/research/`, and `docs/lessons/`.
- Historical Korean KDoc or Korean agent-facing docs do not need a bulk rewrite.
  Apply this policy when creating new content or meaningfully editing existing
  content.

The old rule "public API KDoc is Korean by default" is superseded. New or
meaningfully changed public API KDoc must be English.

## Repositories

### bluetape4k libraries

| Directory | Purpose |
|---|---|
| `bluetape4k-projects/` | Core Kotlin/JVM backend libraries: core, coroutines, data, infra, Spring Boot 3/4, virtual threads |
| `bluetape4k-experimental/` | Experimental Kotlin 2.3 + Java 25 + Spring Boot 4 modules; unpublished |
| `bluetape4k-aws/` | AWS SDK v2 and AWS Kotlin SDK wrappers with coroutines, Spring Boot 4, Ktor 3 |
| `bluetape4k-image/` | Image processing with scrimage and libvips backends |
| `bluetape4k-javers/` | Javers audit/diff with Redis, Kafka, and Exposed integration |
| `bluetape4k-leader/` | Distributed leader election APIs: blocking, async, coroutine, virtual-thread; Redis backend |
| `bluetape4k-text/` | Korean/Japanese tokenizers, language detection, Aho-Corasick search |
| `bluetape4k-graph/` | Graph DB integrations: Neo4j, Memgraph, AGE, TinkerPop, FalkorDB |
| `bluetape4k-exposed/` | JetBrains Exposed ORM wrappers and bluetape4k integration extensions |
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
- Java 21 for core repositories; Java 25 for experimental and several newer repositories.
- Gradle multi-module builds, usually registered through `settings.gradle.kts`
  helper functions such as `includeModules()`.
- Spring Boot 3.x for older/core modules; Spring Boot 4.x for newer/experimental modules.
- Kotlin coroutines first for async work.
- Tests use JUnit 5, MockK, bluetape4k-assertions, and Testcontainers singleton launchers.
- Common compiler flags: `-Xjsr305=strict`, `-jvm-default=enable`,
  `-Xinline-classes`, `-Xcontext-parameters`.

## Kotlin Editing Workflow (MANDATORY)

Before editing a Kotlin class, inspect references and impact when tools are
available (`ide_find_references`, `get_impact_radius_tool`, or equivalent).

After editing any `.kt` file:

1. Run `ide_diagnostics` and check import errors plus unresolved `@Deprecated` warnings.
2. Fix import errors with `ide_optimize_imports`.
3. Resolve `@Deprecated` warnings with `lsp_code_actions`; do not leave them unresolved.
4. Compile and test only after diagnostics are clean.

## Core Design Rules

### Validation and exception types

- `assertXxx()` means `AssertionError` for internal invariants. Do not use it in new code.
- `requireXxx()` means `IllegalArgumentException` for caller input validation. Prefer bluetape4k `require*` extensions.
- Do not change existing exception types casually; tests often depend on them.

```kotlin
fun add(keyword: String): Builder = apply {
    keyword.requireNotBlank("keyword")
}
```

### Coroutines

- Prefer Kotlin coroutines for async work.
- Wrap blocking APIs in `withContext(Dispatchers.IO)`.
- Do not use `runBlocking` in production code except tightly controlled lazy initialization.
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
- All `data class` declarations must implement `java.io.Serializable` and define `serialVersionUID`.

### Same-type parameters

Wrap two or more same-typed parameters in a named data class to avoid positional mistakes.

```kotlin
data class AspectRatio(val width: Int, val height: Int)
fun smartCrop(ratio: AspectRatio): Image
```

### Error handling

- Use `runCatching {}` only when the block has no suspend calls.
- In suspend functions, use manual try/catch and rethrow `CancellationException`.
- Do not silently swallow errors.

## Tests

- Use JUnit 5, MockK, and bluetape4k-assertions.
- Add `@TestInstance(TestInstance.Lifecycle.PER_CLASS)` to test base classes.
- Use `runTest` for suspend tests.
- Use descriptive backtick test names.
- Prefer bluetape4k-assertions comparison matchers over boolean assertions.
- Use `assertFailsWith<T> { }` for exception checks.
- Use `coInvoking { suspendCall } shouldThrow T::class` only for suspend-specific patterns.
- Do not use JUnit `assertThrows`, `invoking { } shouldThrow`, or `kotlin.test.assertFailsWith` in new tests.

For new modules, include:

- `src/test/resources/junit-platform.properties`
- `src/test/resources/logback-test.xml`

Place tests for Kotlin `internal` symbols in the same package path as the source.

### Testcontainers

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

## KDoc

Public classes, interfaces, objects, and extension functions need English KDoc:

- One-line summary.
- `## Behavior / Contract` section for contracts and edge cases.
- Kotlin usage example when useful.

Convert existing Korean KDoc to English when the API is meaningfully edited or refactored.

## README

README files are library-user documentation and remain multilingual.

- Keep `README.md` in English.
- Preserve and update existing localized README files such as `README.ko.md`.
- Allow future locale files such as `README.ja.md` or `README.zh.md`.
- When README content changes, update `README.md` plus the existing locale README set.

Recommended module README structure:

1. Architecture, including a Mermaid diagram when useful.
2. Core features.
3. Usage examples.
4. Configuration options.
5. Dependency instructions.

Use Mermaid diagrams for README architecture. Do not use Vega-Lite for README diagrams.

## Build and Coverage

- Kover is the standard coverage tool. Do not introduce Jacoco.
- Target 80% production coverage unless integration-heavy modules justify a lower threshold.
- Exclude non-production source sets such as `benchmark` and `generated`.
- Do not add ktlint auto-format hooks; use IntelliJ formatting and `.editorconfig`.
- If `.github/workflows/ci.yml` changes, check whether `nightly-tests.yml` also needs updates.

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

- [ ] IDE diagnostics: zero errors and no unresolved deprecations in touched code.
- [ ] Compile and test affected modules.
- [ ] Update `README.md` plus existing localized README files when behavior or public API changes.
- [ ] Add or update English KDoc for new/changed public API.

## Before Creating A PR (MANDATORY)

- [ ] Module tests passed; report the command, pass count when available, and elapsed time.
- [ ] Run `oh-my-claudecode:code-reviewer`; resolve HIGH/CRITICAL findings before push.
- [ ] PR title/body are English.
- [ ] PR body includes test results, rationale, and verification commands.
- [ ] `README.md` plus existing localized README files are updated when needed.
- [ ] English KDoc is complete for new/changed public API.
- [ ] Work happened in a worktree such as `.worktrees/<branch>/` when code changed.

## Git Workflow

- `develop` is the default integration branch; do not push directly.
- `main` is release-only and updated through `develop -> main` PRs.
- Prefer feature branches under `.worktrees/<branch>`.
- Do not use `codex/` for local worktree names or branch names. Use conventional
  prefixes such as `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `build/`, or
  `chore/`.
- Commit messages pushed to GitHub must be English and should use prefixes such
  as `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, or `perf:`.
- PR titles/bodies, GitHub issue titles/bodies, CHANGELOG entries, and release
  notes must be English.
- One issue maps to one PR when practical; use squash-merge.

## Skill Routing

Use the installed bluetape4k skills as the project source of truth. Do not
duplicate their detailed checklists here; load the relevant skill and its
references before implementation.

- `bluetape4k-workflow`: first-stop router for bluetape4k work. It classifies
  Full Design, Fast Track, Bug Fix, Code Review, and Maintenance work, then
  selects the lightest safe lane and verification level.
- `bluetape4k-design`: use for new modules, new services/subsystems, broad API
  design, large refactors, new dependencies, or multi-layer changes. It owns the
  spec/plan/advisor-review/DoD workflow and new-module checks.
- `bluetape4k-patterns`: use for Kotlin implementation or review in this
  ecosystem. Its current references cover testing, Spring Boot auto-config,
  new-module setup, and final checklist/IDE diagnostics.
- Add domain skills when the touched area requires them: `ecc-kotlin-patterns`,
  `ecc-kotlin-exposed`, `ecc-springboot-kotlin`, `ecc-kotlin-testing`,
  `kotlin-coroutines-skill`, `kotlin-spring`, or `kotlin-expert`.
- For workflow or skill-maintenance requests, read relevant repo-local
  `docs/lessons/*.md` files before changing durable guidance.

## Workspace Scripts

Prefer workspace helper scripts before raw commands when they are available:

| Script | Purpose |
|---|---|
| `all-status` | Cross-repo git status summary |
| `all-pull` | Cross-repo `git pull --rebase`, skipping repos without upstream |
| `all-clean-branches` | Remove gone branches and stale worktrees |
| `all-ci-status` | Latest CI status summary for library repos |

Per-repo helper commands may be available on `PATH`: `repo-status`,
`repo-diff`, `repo-test-summary`, `clean-branches`, `worktree-new`,
`worktree-list`, and `ci-status`.
