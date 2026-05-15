# bluetape4k

[English](./README.md) | [한국어](./README.ko.md)

Kotlin/JVM backend libraries, infrastructure adapters, and workshops held together with just enough blue tape to make distributed systems behave.

<p align="center">
  <img src="./assets/bluetape4k-workbench.png" alt="A humorous bluetape4k engineering workbench where blue tape organizes backend components" width="900" />
</p>

## What We Build

`bluetape4k` is a Kotlin-first backend ecosystem for pragmatic server-side development:

- coroutine-friendly APIs for blocking, async, and reactive integration points
- Spring Boot 4 and Java 21/25 era infrastructure modules
- persistence, caching, graph, image, text, AWS, audit, and leader-election utilities
- real workshop projects that keep examples close to production constraints
- tests built around JUnit 5, Testcontainers, Kover, and repeatable Gradle builds

The goal is not to hide complexity. The goal is to give Kotlin developers sharp, well-tested tools for the complexity they actually have.

## bluetape4k Libraries

| Repository | What it is for |
|---|---|
| [`bluetape4k-projects`](https://github.com/bluetape4k/bluetape4k-projects) | Core Kotlin/JVM libraries: core utilities, coroutines, data access, infrastructure helpers, Spring Boot support, and virtual-thread-aware components. |
| [`bluetape4k-experimental`](https://github.com/bluetape4k/bluetape4k-experimental) | Experimental modules for newer runtime combinations such as Kotlin 2.3, Java 25, Spring Boot 4, and emerging infrastructure patterns. |
| [`bluetape4k-exposed`](https://github.com/bluetape4k/bluetape4k-exposed) | JetBrains Exposed extensions for JDBC/R2DBC repositories, cache integration, serialization, and Spring Boot auto-configuration. |
| [`bluetape4k-aws`](https://github.com/bluetape4k/bluetape4k-aws) | AWS SDK v2 and AWS Kotlin SDK helpers with coroutine, Ktor, and Spring Boot integration patterns. |
| [`bluetape4k-image`](https://github.com/bluetape4k/bluetape4k-image) | Image processing adapters around scrimage and libvips for JVM services that need practical image pipelines. |
| [`bluetape4k-javers`](https://github.com/bluetape4k/bluetape4k-javers) | JaVers audit/diff integration with Redis, Kafka, Exposed, and application event workflows. |
| [`bluetape4k-leader`](https://github.com/bluetape4k/bluetape4k-leader) | Distributed leader election APIs for blocking, async, coroutine, and virtual-thread execution models, with Redis-backed coordination. |
| [`bluetape4k-text`](https://github.com/bluetape4k/bluetape4k-text) | Korean/Japanese tokenization, language detection, and Aho-Corasick search utilities. |
| [`bluetape4k-graph`](https://github.com/bluetape4k/bluetape4k-graph) | Graph database integrations for Neo4j, Memgraph, Apache AGE, TinkerPop, and FalkorDB. |
| [`bluetape4k-dependencies`](https://github.com/bluetape4k/bluetape4k-dependencies) | A coordinated BOM for aligning dependency versions across the bluetape4k ecosystem. |

## Workshops and Examples

| Repository | What you can learn from it |
|---|---|
| [`bluetape4k-workshop`](https://github.com/bluetape4k/bluetape4k-workshop) | Backend examples that show how bluetape4k modules fit together in application code. |
| [`exposed-workshop`](https://github.com/bluetape4k/exposed-workshop) | JetBrains Exposed ORM examples covering schema modeling, transactions, testing, and multi-database verification. |
| [`exposed-r2dbc-workshop`](https://github.com/bluetape4k/exposed-r2dbc-workshop) | Exposed R2DBC examples for coroutine-friendly relational persistence. |
| [`timefold-workshop`](https://github.com/bluetape4k/timefold-workshop) | Timefold Solver examples for constraint-solving and scheduling problems. |

## Concrete Case: clinic-appointment

[`clinic-appointment`](https://github.com/bluetape4k/clinic-appointment) is a concrete application built as a private-clinic appointment management system.

It demonstrates how the ecosystem can be applied beyond library code:

- appointment state transitions from request to completion, including cancellation and reassignment
- Timefold Solver scheduling for doctors, rooms, equipment, business hours, and hard/soft constraints
- Spring Boot 4 REST APIs with JWT authentication, Flyway migrations, and Swagger UI
- Redis-backed leader election for high-availability notification delivery
- Resilience4j circuit breaker, retry, and bulkhead patterns for operational reliability
- Angular frontend for appointment search, creation, and status changes
- modular backend structure across domain, events, solver, notification, API, and frontend layers

It is the kind of app where the blue tape stops being a joke and starts being a reliability strategy.

## Engineering Defaults

- Kotlin-first, coroutine-first APIs
- Gradle multi-module builds
- Java 21 for core libraries, Java 25 for newer experimental/application work
- Spring Boot 4.x is the supported Spring Boot line
- JUnit 5, MockK, Testcontainers, and Kover
- README documentation in English and Korean for bluetape4k modules
- small, reviewable changes with explicit verification

## Start Here

- Want core utilities and Spring infrastructure? Start with [`bluetape4k-projects`](https://github.com/bluetape4k/bluetape4k-projects).
- Working with Exposed? Start with [`bluetape4k-exposed`](https://github.com/bluetape4k/bluetape4k-exposed), then compare examples in [`exposed-workshop`](https://github.com/bluetape4k/exposed-workshop).
- Need a real application reference? Read [`clinic-appointment`](https://github.com/bluetape4k/clinic-appointment).
- Exploring graph, image, text, AWS, audit, or leader election modules? Pick the matching repository above.

---

Made for Kotlin backend engineers who know that architecture is cleaner when the tape is blue, documented, tested, and applied only where it belongs.
