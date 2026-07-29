# AGENTS.md - bluetape4k Workspace Root

This directory is the local workspace for the bluetape4k GitHub organization.
Each child directory is an independent Git repository. This file applies to all
repositories below this directory; repo-local `AGENTS.md` files add narrower
rules and take precedence inside their own repo.

Keep conversations with the user in Korean. Keep agent-facing guidance and
memory such as `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `.omx/notepad.md`, and
`~/.codex/memories/*` in concise English unless a repo-local document explicitly
requires different wording.

Use audience-based document language. This table is the canonical workspace
policy; repo-local `AGENTS.md` files and skills may narrow it but should not
silently reverse it.

| Primary reader | Artifacts | Default language | Notes |
|---|---|---|---|
| User in chat | Conversation with `debop` | Korean | Use Korean unless the user asks otherwise. |
| End user | Library `README.md`, `README.ko.md`, future localized README files | Multilingual | Keep library `README.md` English and update existing localized README files together. |
| Example learner | README files, work documents, KDoc, and diagrams in repositories listed under **Workshops and examples** | README and diagrams bilingual; work docs and KDoc Korean | Keep English/Korean pairs source-equivalent; preserve technical identifiers. |
| Kotlin API reader | Library and internal KDoc | Korean | Preserve code identifiers, API names, commands, URLs, and exact error text. |
| Contributor (public, human) | CHANGELOG, release notes, GitHub issues, GitHub PR titles/bodies, pushed commit messages | English | Delivery metadata remains English. |
| Engineer (internal human-readable) | `docs/superpowers/specs/`, `docs/superpowers/plans/`, `docs/superpowers/research/`, `docs/lessons/` | Repository category | Use English by default in library and infrastructure repositories; repositories listed under **Workshops and examples** require Korean. |
| AI agent | `CLAUDE.md`, `AGENTS.md`, `SKILL.md`, `.omx/notepad.md`, `~/.codex/memories/*`, agent memory | English | Keep concise English for token efficiency and cross-tool reuse. |
| Blog/article reader | `bluetape4k.github.io` blog/articles | Locale-specific | Follow the blog skill: Korean-first for Korean posts, English parity when bilingual. |
| Diagram/image reader | Generated diagram labels and visual assets | English by default | Repositories under **Workshops and examples** require source-equivalent English and Korean diagram assets when reader-facing text is present. |

- Conversations with the user: Korean.
- Library user documentation: multilingual where applicable. Keep library
  `README.md` in English and preserve/update existing localized README files
  such as `README.ko.md`; additional locales such as Japanese or Chinese may be
  added over time.
- Workshop and example documentation: bilingual README and diagrams plus
  Korean work documents and KDoc. In repositories listed under **Workshops and
  examples**, provide `README.md` in English and `README.ko.md` in Korean with
  equivalent content. Write work documents such as specs, plans, research
  notes, lessons, and KDoc in Korean. For diagrams with reader-facing text,
  provide source-equivalent English and Korean SVG/PNG assets; text-free
  diagrams may be shared. Keep code, identifiers, commands, API names, URLs,
  and exact error text in their original form.
- KDoc is Korean-first across the workspace, including public and internal
   declarations in library, infrastructure, workshop, and example repositories.
   Write every new or meaningfully updated KDoc in Korean while preserving code,
   identifiers, commands, API names, URLs, and exact error text. Do not translate
   untouched legacy KDoc solely to satisfy this forward-applying rule. CHANGELOG
   entries, release notes, GitHub issues, GitHub PR titles/bodies, and pushed
   commit messages remain English unless the user explicitly requests otherwise.
- Internal human-readable work documents follow the repository category. Use
  English by default for specs, plans, research notes, and lessons in library
  and infrastructure repositories. Repositories listed under **Workshops and
  examples** require Korean for these artifacts.
- Agent memory and agent-facing guidance must be English for token efficiency,
  LLM consistency, and cross-tool reuse.

## Repo-Local AGENTS Overlays

This workspace root `AGENTS.md` is the common operating contract for every
repository under `/Users/debop/work/bluetape4k`. Repo-local `AGENTS.md` files
must be thin overlays: they should first direct agents to read and follow this
workspace guide, then keep only repository-specific layout, commands, module
maps, domain rules, and local exceptions.

Do not duplicate common workspace rules in child repositories. Keep shared
language policy, README locale policy, diagram/chart policy, GitHub
issue/PR metadata policy, workflow/skill routing, Kover/Codecov visibility,
Testcontainers sequencing, module-registration checklists, and common
documentation artifact paths here. If a repo-local file needs to narrow one of
these rules, state only the narrower exception and why it exists.

Nested `AGENTS.md` files must inherit both the workspace root guide and their
nearest repo-local guide. They should contain only the extra constraints for
their subdirectory.

## Repositories

### Kotlin/JVM libraries

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

### Go, Rust, and Python libraries

| Directory | Purpose |
|---|---|
| `bluetape-go/` | Go backend utilities and distributed infrastructure packages |
| `bluetape-rs/` | Rust backend primitives for the bluetape ecosystem |
| `bluetape-py/` | Python backend, testing, logging, and operations libraries |

### Organization infrastructure

| Directory | Purpose |
|---|---|
| `.github/` | Organization profile, issue/PR templates, and GitHub community files |
| `bluetape-skills/` | Canonical installable Codex skills and shared workflow references |
| `bluetape4k-wiki/` | Private shared source for bluetape4k engineering knowledge |
| `bluetape4k.github.io/` | GitHub Pages site and ecosystem documentation entrypoint |

### Workshops and examples

| Directory | Purpose |
|---|---|
| `bluetape4k-workshop/` | Backend examples using bluetape4k libraries |
| `bluetape-go-workshop/` | Runnable web application examples using bluetape-go |
| `bluetape-rs-workshop/` | Runnable backend examples using bluetape-rs |
| `exposed-workshop/` | JetBrains Exposed ORM examples |
| `exposed-r2dbc-workshop/` | Exposed R2DBC examples |
| `clinic-appointment/` | Clinic appointment example app |
| `timefold-workshop/` | Timefold Solver workshop |

Every repository listed in this section targets Korean developers. Korean is
the required language for its work documents and KDoc. README files remain
bilingual: `README.md` in English and `README.ko.md` in Korean, with
source-equivalent content. Diagrams with reader-facing text also require
source-equivalent English and Korean SVG/PNG assets. This category-level
rule matches the workspace Korean KDoc default, but it does not change the
English policy for agent-facing guidance or public GitHub delivery metadata.

## Kotlin Dependency Catalog Governance

- All `bluetape4k-*` library repositories must treat
  `bluetape4k-dependencies` as the source of truth for centrally governed
  dependency, plugin, and compatibility-line versions.
- `bluetape4k-*` repositories should import
  `bluetape4k-dependencies/gradle/libs.versions.toml` from a checked-out
  `bluetape4k-dependencies` git ref and read centrally governed aliases from
  that catalog instead of pinning the same versions in repo-local
  `gradle/libs.versions.toml`.
- Local version catalogs may keep repository-local aliases and coordinates, but
  centrally governed versions should not be duplicated locally unless the
  exception is temporary, documented, and linked to a release/governance issue.
- Start shared version changes in `bluetape4k-dependencies` first, cut a
  release-train catalog ref such as `catalog/YYYY-MM-DD-NN`, then update
  downstream `bluetape4k-*` repositories and CI to read that checked-out ref.
- Treat `bluetape4k-github` GNO results as governance evidence when the same
  issue or PR pattern appears across repositories. Repeated merged PRs such as
  Kover hard-gate removals mean the root rule should be report-only coverage
  unless a new explicit policy decision says otherwise.

## Knowledge Retrieval

- When looking for similar implementations, prior examples, benchmark results,
  discussions, plans, specs, lessons, or scattered project documentation, query
  GNO first before filesystem search.
- For workflow, coverage, release, module-registration, or skill-maintenance
  changes, query both `bluetape4k-github` and `bluetape4k-docs` before editing:
  issues/PRs show where the process failed in review, while lessons/specs show
  the durable rule to promote.
- Follow the user-scope GNO command selection rules. For routine lookup, prefer
  `gno query "<query>" -c <collection> --fast --no-rerank`.
- Use `gno query "<query>" -c bluetape4k-docs --fast --no-rerank` for workspace
  documentation and examples. This collection indexes all Markdown files under
  `/Users/debop/work/bluetape4k` with `**/*.md`, including repository README
  and CHANGELOG files, subject to its configured exclusions.
- Use `gno query "<query>" -c wiki --fast --no-rerank` for personal or cross-project
  knowledge under `~/.codex/wiki`.
- In Codex App sessions with context-mode available, use context-mode MCP tools
  for large reads/searches/log analysis so raw shell output does not flood the
  model context.
- For repo-local code lookup, use CodeGraph first when the question is
  structural: symbol definition, class/function/object/property location,
  signature/source, callers, callees, impact radius, or current implementation
  context. Do not run `rg` for a code symbol until the matching CodeGraph tool
  has been attempted and its result considered.
- Before any source-tree `rg` search, perform this guard: if the query names or
  implies a code symbol or relationship, stop and use CodeGraph first. Use `rg`
  first only for literal text, comments, log messages, filenames, generated
  files, build output, or when CodeGraph is unavailable/not initialized.
- Use MinishLab Semble or `~/.cargo/bin/semble_rs` after CodeGraph when
  natural-language, ranked snippets, or dependency lookup are more useful than
  raw text matches.
- If GNO, CodeGraph, or Semble are unavailable, stale, or return weak matches,
  fall back to `rg` and mention the indexing/tooling gap when it affects the
  answer.

## Language Stacks

### Kotlin/JVM

- Kotlin 2.3+.
- Java 21 for core repos; Java 25 for experimental and several newer repos.
- Gradle multi-module builds, usually registered by `settings.gradle.kts` helper functions.
- Spring Boot 3.x for older/core modules; Spring Boot 4.x for newer/experimental modules.
- Kotlin coroutines first for async work.
- Tests: JUnit 5, MockK, bluetape4k-assertions, Testcontainers singleton launchers.
- Common compiler flags: `-Xjsr305=strict`, `-jvm-default=enable`,
  `-Xinline-classes`, `-Xcontext-parameters`.

### Go

- Use standard Go modules and the repository Makefile or task runner as the
  command authority.
- Run targeted package tests first, then repository tests, race detection, and
  lint when the change touches concurrency or shared infrastructure.
- Follow `bluetape-go-patterns` for implementation, review, testing, packaging,
  and release conventions.

### Rust

- Use Cargo workspace commands and repository-local feature definitions as the
  build authority.
- Run targeted tests first, then workspace tests, Clippy, and formatting checks.
- Follow `bluetape-rs-patterns` for implementation, review, testing, packaging,
  and release conventions.

### Python

- Use the repository's `pyproject.toml` and lockfile as dependency and tooling
  authorities.
- Run targeted tests first, then the repository's configured lint, type, and
  packaging checks.
- Follow `bluetape-py-patterns` for implementation, review, testing, packaging,
  and release conventions.

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
- All `data class` declarations must implement `java.io.Serializable` and define `serialVersionUID`.

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
style already used by the repo. Write every new or meaningfully updated KDoc in
Korean across library, infrastructure, workshop, and example repositories.
Internal classes and data-class constructor properties should also have Korean
KDoc when they encode contracts or non-obvious state. Include:

- One-line summary.
- Contract/behavior section.
- Kotlin usage example when useful.

## README Rules

For library and infrastructure repositories and their modules, keep user-facing
README files multilingual. New repositories, new modules, rewritten root
README files, and substantial README refreshes must create or update both:

- `README.md`
- `README.ko.md`

Repositories listed under **Workshops and examples** also follow this bilingual
README requirement: `README.md` is English and `README.ko.md` is Korean, with
source-equivalent content. Their work documents and KDoc must be written in
Korean.

Additional localized README files such as `README.ja.md` or `README.zh.md` may
be added over time. Each README must include a language switch directly below
the title using the `English | 한국어` form. Use the current page as plain text
and the other locale as a relative link, for example `English |
[한국어](README.ko.md)` in `README.md` and `[English](README.md) | 한국어` in
`README.ko.md`.

Use `$bluetape-writer` for Korean README prose review and localization. In
multilingual repositories, keep `README.md` English and keep `README.ko.md`
source-equivalent, not abbreviated.

README and benchmark result documents should include diagrams and charts as
much as practical when they reduce cognitive load or summarize measured data.
Use `$bluetape-diagram` for README diagrams, benchmark charts, Mermaid/ASCII
conversion, visual asset placement, PNG/SVG generation, and rendered visual
validation. Treat Mermaid or ASCII as source sketches, not final README
artifacts; README files should embed generated PNG assets with matching SVG
sources, following the diagram skill's output contract. In repositories listed
under **Workshops and examples**, diagrams containing reader-facing text must
provide source-equivalent English and Korean SVG/PNG assets; text-free diagrams
may be shared.

Module README structure should cover architecture, core features, usage
examples, configuration options, dependency instructions, and benchmark evidence
when available.

## Project Documentation Artifacts

Store durable project design/history artifacts in repo-local docs paths:

- Specs: `docs/superpowers/specs/YYYY-MM-DD-{slug}-design.md`
- Plans: `docs/superpowers/plans/YYYY-MM-DD-{slug}-plan.md`
- Research notes, when needed: `docs/superpowers/research/YYYY-MM-DD-{slug}-research.md`
- Lessons Learned / work retrospectives: `docs/lessons/YYYY-MM-DD-{slug}.md`
- Use lowercase ASCII kebab-case slugs; include `issue-{number}-` when the
  artifact is tied to a GitHub issue.
- Create or update `docs/lessons/YYYY-MM-DD-{slug}.md` only when it is useful
  for durable project learning, required by a selected workflow, or explicitly
  requested by the user. Keep it short for small work, and include the context,
  decision, outcome, verification evidence, and what future agents should do
  differently.
- Consolidate `docs/lessons/` entries only when explicitly requested or when a
  selected workflow requires a retrospective cleanup step.
- Treat `.omx/plans`, `.omx/notepad.md`, chat summaries, and runtime notes as
  transient. Promote durable decisions and lessons into `docs/superpowers/` or
  `docs/lessons/`.
- Specs, plans, research notes, and lessons are internal working artifacts and
  may be written in Korean.

## Planning Approval

For `bluetape-workflow` or any other workflow that has an explicit planning
phase, stop at the first concrete plan and ask the user to approve it before
editing source files, creating durable planning artifacts, committing, opening
PRs, dispatching workflows, merging, publishing, or deleting branches/worktrees.

Read-only discovery, issue/PR metadata inspection, local status checks, and
drafting the plan are allowed before approval. Do not treat autonomy or
"continue" language as permission to skip this first plan approval gate.

## Build and Coverage

- Kover is the standard coverage tool. Do not introduce Jacoco.
- Target 80% production coverage unless integration-heavy modules justify a
  lower threshold.
- Exclude non-production source sets such as `benchmark` and `generated`.
- Do not add ktlint auto-format hooks; use IntelliJ formatting and `.editorconfig`.
- If `.github/workflows/ci.yml` changes, check whether nightly workflow changes
  are also required.
- When adding a new module, update the repository's CI and Nightly workflows so
  the module's tests run in the appropriate scope. Container-backed module tests
  should usually be added to Full Nightly rather than the daily smoke path.
- Treat coordinated central dependency/catalog upgrades as broad-impact
  maintenance: upgrade `bluetape4k-dependencies` first, then merge/publish
  prerequisite core repositories before syncing downstream consumer catalogs and
  PRs.

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
- Update `README.md` and any required localized README files according to the
  repository's governing language policy when behavior or public API changes.
- Add or update Korean KDoc for new/changed public API and non-obvious internal
  contracts.
- For added, renamed, moved, or removed modules, verify the full registration
  chain: `settings.gradle.kts`, README locale set, repo-local `AGENTS.md`
  module list, CI path filters/jobs, Nightly or examples workflow, summary
  `needs`, coverage artifacts, BOM/catalog constraints, and `./gradlew projects`.
- Run Testcontainers-backed verification serially across modules, worktrees,
  and delegated agents. If a workflow or test fails first and passes on retry,
  investigate lifecycle, container, or timing risk before marking it noise.
- Keep Kover XML and Codecov visibility, but do not add or restore hard Kover
  thresholds unless an explicit policy decision exists.

## Cross-Repo Shared Guards

- Before issue, PR, workflow, release, dependency, benchmark, guidance, or
  module-registration work, query current repository evidence in
  `bluetape4k-github` and `bluetape4k-docs` when available.
- Before merging after CI turns green, re-read PR reviews and review threads;
  unresolved or newer user review comments reopen the merge gate.
- For module additions, moves, renames, removals, or artifact renames, keep the
  registration chain synchronized: `settings.gradle.kts`, README locale set,
  repo-local module lists, CI path filters/jobs, Nightly or examples workflow,
  summary `needs`, coverage artifacts, BOM/catalog constraints, and
  `./gradlew projects` or the repo-equivalent project listing.
- Keep Kover XML and Codecov visibility as the default coverage signal. Do not
  add or restore hard Kover thresholds unless an explicit policy decision says
  to do so.
- Run Testcontainers-backed, real database, native, JNI, emulator, and other
  heavyweight integration checks sequentially across modules, worktrees, and
  delegated agents unless a repo-local rule proves parallel execution is safe.

## Git Workflow

- `develop` is the default integration branch; do not push directly.
- `main` is release-only and updated through `develop -> main` PRs.
- Use GitHub rebase merge as the default PR merge strategy unless the user explicitly requests another strategy.
- Prefer feature branches under `.worktrees/<branch>`.
- Do not use `codex/` for local worktree names or branch names. Use conventional
  prefixes such as `feat/`, `fix/`, `docs/`, `refactor/`, `test/`, `build/`, or
  `chore/`.
- Commits commonly use prefixes such as `feat:`, `fix:`, `refactor:`, `build:`,
  `docs:`, `chore:`, `test:`, `perf:`.
- Commit text that will be pushed to GitHub must be English. Keep the intent
  line concise.

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

RTK is retired in this workspace. Do not invoke it, recommend it, or
reintroduce command wrappers or rewrite hooks for it. Use raw commands or the
explicit repository helpers above.

GitHub/CI preference:

- Use `ci-status --limit N` for the current repo's latest GitHub Actions runs.
- Use `ci-status --watch` when asked to monitor an in-progress run.
- Use `all-ci-status` for cross-repo library CI summaries.
- Use `repo-status`, `repo-diff`, and `repo-log` for compact repository context.
- Use `worktree-new` and `worktree-list` for normal worktree operations.
- Use `clean-branches` and `all-clean-branches` only when branch/worktree
  cleanup is explicitly requested, because they delete local branches and remove
  associated worktrees.
- For documentation-only PRs, do not wait for heavyweight CI unless branch
  protection explicitly requires it. Verify locally with content review plus
  `git diff --check`; run repository-specific documentation builds only when
  rendered docs or the public website are affected.
- Treat GitHub `Automatic Dependency Submission` / `submit-gradle` checks as
  non-blocking for documentation-only PRs unless GitHub branch protection marks
  them required.

## Skill Routing

For every bluetape ecosystem repository under this workspace, including
libraries, workshops, examples, infrastructure, and the GitHub Pages site, use
the installed bluetape4k skills as the project source of truth. Do not duplicate
their detailed checklists here; load the relevant skill and its references
before implementation.

- `bluetape-workflow`: first-stop router. Classify work as Type A Full
  Feature, B Fast Track, C Bug Fix, D Code Review, E Maintenance, P Publish, or
  F Self Improve, then load the canonical leaf skill.
- Canonical leaf skills are `bluetape-full-feature`,
  `bluetape-fast-track`, `bluetape-bugfix`, `code-review`,
  `bluetape-maintenance`, `bluetape-publish-jvm` or
  `bluetape-publish-go`, and `bluetape-self-improve`.
- Every executable workflow row is a checkbox with `Action`, `Evidence`, and
  `Failure`. An unchecked row blocks dependents; missing, stale, or `UNKNOWN`
  evidence is FAIL; `SKIPPED` is forbidden; `N/A` requires concrete scope
  evidence. Report `Required checks: X/Y; N/A: N; Blocked: N`.
- `bluetape-full-feature`: use for new modules, services/subsystems, broad
  APIs, large refactors, new dependencies, or multi-layer changes. It owns the
  spec/plan/review/DoD workflow and new-module checks.
- `bluetape-kotlin-patterns`: use for Kotlin implementation or review. Its
  references cover testing, Spring Boot auto-configuration, new-module setup,
  and final checklist/IDE diagnostics.
- `bluetape-go-patterns`, `bluetape-rs-patterns`, and
  `bluetape-py-patterns`: use for implementation, review, testing, packaging,
  and release work in the matching language ecosystem.
- Historical specs, plans, and lessons may name `bluetape4k-design`,
  `bluetape4k-patterns`, `bluetape-bugfix-workflow`, or `bugfix-workflow`.
  Interpret them as `bluetape-full-feature`, `bluetape-kotlin-patterns`, and
  `bluetape-bugfix`; do not skip the workflow or recreate an alias merely
  because a historical artifact uses an old name.
- `bluetape-self-improve`: use only for explicit benchmark-guided
  self-improvement requests with a measurable baseline, candidate loop, and stop
  condition.
- `bluetape-writer`: use for Korean README prose, blog posts, article
  localization, Korean naturalness review, and bilingual content parity.
- `bluetape-diagram`: use for README diagrams, benchmark result charts,
  Mermaid/ASCII conversion, visual QA, generated PNG/SVG assets, and any public
  diagram or chart embedded in README, docs, blog, or website pages.
- Add domain skills when the touched area requires them: `ecc-kotlin-patterns`,
  `ecc-kotlin-exposed`, `ecc-springboot-kotlin`, `ecc-kotlin-testing`,
  `kotlin-coroutines-skill`, `kotlin-spring`, or `kotlin-expert`.
- Superpowers skills and artifacts are part of the workflow contract. When a
  selected bluetape4k workflow references a Superpowers skill, plan, spec,
  research note, or lesson, load and follow that skill or artifact before
  editing, reviewing, opening PRs, merging, or publishing.
- For workflow or skill-maintenance requests, read relevant repo-local
  `docs/lessons/*.md` files before changing durable guidance.

## GitHub Issue And Pull Request Workflow

These rules apply to every bluetape ecosystem repository under this workspace,
including `bluetape4k-*`, `bluetape-go*`, `bluetape-rs*`, `bluetape-py*`,
`bluetape-skills`, workshop/example repositories, `.github`, and
`bluetape4k.github.io`.

- Assign GitHub issues and pull requests to `debop` by default unless the user
  explicitly says otherwise. Use `--assignee debop` with `gh issue create` and
  `gh pr create`, or the equivalent GitHub API `assignees` field. If a
  repository rejects the assignee, report that blocker instead of creating an
  unassigned issue or PR silently.
- When creating an issue, set the appropriate milestone and detailed labels.
  Inspect the repository's existing milestones and labels first; prefer precise
  topic labels such as `examples`, `workshop`, `ktor`, `spring-boot`, `r2dbc`,
  `exposed`, `documentation`, `testing`, `performance`, or `maintenance` when
  they exist or can be inferred safely from the work scope.
- For any PR that resolves or follows an issue, read the linked issue metadata
  first and set the PR milestone to the issue milestone. Mirror the issue
  assignee and relevant labels onto the PR when GitHub supports those fields for
  the repository.
- After issue or PR creation, verify the live metadata with `gh issue view` or
  `gh pr view` before reporting the work complete.
