# Nightly 워크플로 거버넌스

이 문서는 Issue #2를 위해 bluetape4k 저장소의 Nightly 워크플로를 분류합니다.
목표 모델은 게이트가 있는 워크플로입니다.

- PR/CI: 변경 범위가 빠르게 피드백되는 경로
- Daily Nightly: 신호가 높고 비용이 제한된 smoke 검사
- Weekly Full Nightly: 통합, 컨테이너, 커버리지, 예제를 포함한 고비용 검사
- 수동 dispatch: 검증 대상을 고르는 `scope` 입력

## Scope 의미

고비용 저장소는 다음 입력을 제공합니다.

- `scope=smoke`: compile, detekt, 비컨테이너 또는 저비용 core test
- `scope=full`: smoke에 더해 고비용 컨테이너, 외부 runtime, example 또는
  광범위한 coverage job 전체

예약 실행은 다음을 사용합니다.

- `0 19 * * 1-6`: daily smoke, KST 화-일 04:00
- `0 19 * * 0`: weekly full, KST 월요일 04:00

## 저장소 분류

| 저장소 | 분류 | Daily smoke | Weekly full |
|---|---|---|---|
| `bluetape4k-aws` | daily/full 분리 | Build, detekt, Spring Boot 모듈 테스트 | LocalStack AWS SDK/Kotlin/Ktor와 example |
| `bluetape4k-experimental` | 의도적으로 단순 | 기존 build/test 경로 | 동일 경로, 공개하지 않는 실험 저장소 |
| `bluetape4k-exposed` | daily/full 분리 | H2/core/serialization/cache/저비용 모듈 | PostgreSQL, MySQL, Redis, ClickHouse, Trino, BigQuery, matrix example job |
| `bluetape4k-graph` | daily/full 분리 | Core, TinkerGraph, Spring starter | Neo4j, Memgraph, Apache AGE, FalkorDB, example |
| `bluetape4k-image` | daily/full 분리 | Scrimage/core image test | libvips API, Java 21 vips, Java 25 vips |
| `bluetape4k-javers` | daily/full 분리 | `javers-core` | Redis와 Kafka persistence |
| `bluetape4k-leader` | daily/full 분리 | Core, H2, Micrometer | Redis, PostgreSQL, MySQL, MongoDB, Hazelcast, ZooKeeper, example, Spring Boot, Ktor |
| `bluetape4k-projects` | 기존 기준 분리 | Build, detekt, core test, 대표 Testcontainers smoke group | Weekly full schedule와 저장소별 scope |
| `bluetape4k-text` | 경량 단순 | 기존 tokenizer/language/search test | 동일 경로, 컨테이너 고비용 job 없음 |
| `bluetape4k-workshop` | daily/full 분리 | Build만 실행 | 전체 example/Testcontainers 경로 |

## 중앙 dispatch

조직 `.github` 저장소는 선택적 Nightly 실행을 지원하는 저장소에 공통
`smoke` 또는 `full` scope 입력을 전달합니다. scope 입력이 없는 저장소는
의도적으로 단순하게 두고 추가 dispatch 입력을 보내지 않습니다. `bluetape4k-projects`
의 `testcontainers`, `graphdb`, `aws`처럼 저장소별 scope는 저장소의
workflow dispatch UI에서 계속 사용할 수 있습니다.

## 후속 기준

- 고비용 새 Nightly job은 매일 실행해야 할 운영상 이유를 문서화하지 않는 한
  `scope=full` 뒤에 둡니다.
- 저장소에 새 모듈을 추가하면 같은 PR 또는 즉시 이어지는 PR에서 저장소별
  Nightly 워크플로를 갱신해 새 모듈 테스트가 적절한 smoke/full 범위에서
  실행되도록 합니다.
- 저장소 Nightly 워크플로가 바뀌면 DoD 전에 해당 Nightly를 명시적으로
  dispatch하고 실행 URL/result를 기록합니다. 모듈 커버리지 또는
  Testcontainers가 바뀌면 변경이 smoke-only가 아닌 한 `scope=full`을
  사용합니다.
- 고비용 통합 테스트가 생긴 저장소에는 수동 `scope` 입력을 추가합니다.
- full 실행에서 커버리지 artifact를 유지합니다. 저장소가 품질 게이트에
  커버리지를 사용하지 않는 한 smoke 커버리지는 선택 사항입니다.
- `bluetape4k-projects`의 smoke runtime은 설계상 대표 컨테이너 검사를
  포함하므로 여러 예약 실행 후 다시 검토합니다.
