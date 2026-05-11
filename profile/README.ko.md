# bluetape4k

[English](./README.md) | [한국어](./README.ko.md)

`bluetape4k`는 Kotlin/JVM 백엔드 라이브러리, 인프라 어댑터, 워크숍 예제를 모아 둔 조직입니다. 복잡한 분산 시스템을 파란 테이프로 대충 붙여 놓는다는 농담처럼 보이지만, 실제로는 문서화되고 테스트된 도구로 복잡도를 제어하는 것을 목표로 합니다.

<p align="center">
  <img src="./assets/bluetape4k-workbench.png" alt="파란 테이프가 백엔드 컴포넌트를 정리하는 bluetape4k 작업대 일러스트" width="900" />
</p>

## 무엇을 만들고 있나

`bluetape4k`는 Kotlin 중심의 실용적인 서버 개발 생태계입니다.

- blocking, async, reactive 경계를 다루는 coroutine-friendly API
- Spring Boot 3/4, Java 21/25 시대의 인프라 모듈
- persistence, caching, graph, image, text, AWS, audit, leader election 유틸리티
- 실제 제약을 반영한 workshop 프로젝트
- JUnit 5, Testcontainers, Kover, Gradle 기반의 반복 가능한 검증

목표는 복잡도를 숨기는 것이 아니라, Kotlin 개발자가 실제로 마주치는 복잡도를 다룰 수 있는 날카롭고 검증된 도구를 제공하는 것입니다.

## bluetape4k 라이브러리

| Repository | 역할 |
|---|---|
| [`bluetape4k-projects`](https://github.com/bluetape4k/bluetape4k-projects) | core utilities, coroutines, data access, infrastructure helpers, Spring Boot 지원, virtual-thread-aware 컴포넌트를 포함한 핵심 Kotlin/JVM 라이브러리입니다. |
| [`bluetape4k-experimental`](https://github.com/bluetape4k/bluetape4k-experimental) | Kotlin 2.3, Java 25, Spring Boot 4 등 최신 런타임 조합과 새로운 인프라 패턴을 실험하는 모듈입니다. |
| [`bluetape4k-exposed`](https://github.com/bluetape4k/bluetape4k-exposed) | JetBrains Exposed용 JDBC/R2DBC repository, cache, serialization, Spring Boot auto-configuration 확장입니다. |
| [`bluetape4k-aws`](https://github.com/bluetape4k/bluetape4k-aws) | AWS SDK v2와 AWS Kotlin SDK를 coroutine, Ktor, Spring Boot 환경에서 쓰기 위한 래퍼와 통합 패턴입니다. |
| [`bluetape4k-image`](https://github.com/bluetape4k/bluetape4k-image) | scrimage와 libvips 기반의 JVM 이미지 처리 어댑터입니다. |
| [`bluetape4k-javers`](https://github.com/bluetape4k/bluetape4k-javers) | JaVers audit/diff를 Redis, Kafka, Exposed, application event 흐름과 연결하는 모듈입니다. |
| [`bluetape4k-leader`](https://github.com/bluetape4k/bluetape4k-leader) | blocking, async, coroutine, virtual thread 실행 모델을 지원하는 분산 leader election API와 Redis coordination 구현입니다. |
| [`bluetape4k-text`](https://github.com/bluetape4k/bluetape4k-text) | 한국어/일본어 tokenizer, language detection, Aho-Corasick 검색 유틸리티입니다. |
| [`bluetape4k-graph`](https://github.com/bluetape4k/bluetape4k-graph) | Neo4j, Memgraph, Apache AGE, TinkerPop, FalkorDB 등 graph database 통합 모듈입니다. |
| [`bluetape4k-dependencies`](https://github.com/bluetape4k/bluetape4k-dependencies) | bluetape4k 생태계의 dependency version을 맞추기 위한 BOM입니다. |

## 워크숍과 예제

| Repository | 배울 수 있는 내용 |
|---|---|
| [`bluetape4k-workshop`](https://github.com/bluetape4k/bluetape4k-workshop) | bluetape4k 모듈들을 실제 application code에서 조합하는 백엔드 예제입니다. |
| [`exposed-workshop`](https://github.com/bluetape4k/exposed-workshop) | JetBrains Exposed ORM의 schema modeling, transaction, testing, multi-database 검증 예제입니다. |
| [`exposed-r2dbc-workshop`](https://github.com/bluetape4k/exposed-r2dbc-workshop) | coroutine-friendly relational persistence를 위한 Exposed R2DBC 예제입니다. |
| [`timefold-workshop`](https://github.com/bluetape4k/timefold-workshop) | constraint solving과 scheduling 문제를 다루는 Timefold Solver 예제입니다. |

## 구체적인 사례: clinic-appointment

[`clinic-appointment`](https://github.com/bluetape4k/clinic-appointment)는 개인병원 환자 예약 관리 시스템 예제입니다.

라이브러리 수준을 넘어 실제 애플리케이션에서 bluetape4k 계열 설계가 어떻게 쓰이는지 보여줍니다.

- 요청부터 완료까지의 appointment state transition, cancellation, reassignment
- 의사, 진료실, 장비, 영업시간, hard/soft constraint를 고려한 Timefold Solver scheduling
- JWT 인증, Flyway migration, Swagger UI를 포함한 Spring Boot 4 REST API
- Redis-backed leader election을 이용한 고가용성 notification delivery
- Resilience4j circuit breaker, retry, bulkhead 기반 운영 안정성 패턴
- 예약 검색, 생성, 상태 변경을 위한 Angular frontend
- domain, event, solver, notification, API, frontend로 나뉜 modular backend 구조

이 프로젝트에서는 파란 테이프 농담이 어느 순간 reliability strategy가 됩니다.

## 엔지니어링 기본값

- Kotlin-first, coroutine-first API
- Gradle multi-module build
- core library는 Java 21, 최신 실험/애플리케이션은 Java 25 중심
- 필요 모듈에 Spring Boot 3.x/4.x 호환성 고려
- JUnit 5, MockK, Testcontainers, Kover
- bluetape4k 모듈은 영어/한국어 README 동시 관리
- 작은 단위의 reviewable change와 명시적인 verification

## 어디서 시작할까

- 핵심 유틸리티와 Spring 인프라가 필요하면 [`bluetape4k-projects`](https://github.com/bluetape4k/bluetape4k-projects)를 보세요.
- Exposed를 쓴다면 [`bluetape4k-exposed`](https://github.com/bluetape4k/bluetape4k-exposed)와 [`exposed-workshop`](https://github.com/bluetape4k/exposed-workshop)을 함께 보는 것이 좋습니다.
- 실제 애플리케이션 사례가 필요하면 [`clinic-appointment`](https://github.com/bluetape4k/clinic-appointment)를 보세요.
- graph, image, text, AWS, audit, leader election이 필요하면 위의 해당 저장소에서 시작하면 됩니다.

---

Kotlin 백엔드 엔지니어를 위해 만들었습니다. 좋은 아키텍처는 파란 테이프도 문서화하고, 테스트하고, 꼭 필요한 곳에만 붙입니다.
