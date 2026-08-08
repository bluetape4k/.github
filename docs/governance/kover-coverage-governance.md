# Kover 커버리지 거버넌스

## 목적

Kover는 bluetape4k 저장소의 표준 커버리지 도구입니다. 커버리지 보고서는
임계치를 실제로 강제하거나, 아직 report-only로 남겨 두는 이유를 명시할
때만 유효한 품질 신호가 됩니다.

## 임계치 등급

| 등급 | 목표 | 적용 대상 |
|---|---:|---|
| Core library | 라인 커버리지 80% | 대부분 단위 테스트로 검증할 수 있는 안정적인 공개 API |
| Integration-heavy library | 라인 커버리지 60-70% | 외부 서비스, 컨테이너, native runtime 또는 framework wiring 비중이 큰 모듈 |
| Report-only transition | 아직 실패 게이트 없음 | Kover 보고서는 있지만 검증된 기준선이 없는 저장소. 후속 임계치 계획을 포함해야 함 |
| Workshop/demo | production 게이트 없음 | 예제 저장소. 테스트는 compile/run해야 하지만 커버리지는 참고 정보임 |

## 저장소 inventory

| 저장소 | 현재 상태 | 정책 | CI/Nightly 신호 |
|---|---|---|---|
| `bluetape4k-aws` | Nightly에서 Kover XML 보고서 생성, verify bounds 없음 | AWS/LocalStack 통합 비용으로 report-only 전환. 먼저 기준선을 만들고 pure client 모듈은 70%, Spring/Ktor 통합 모듈은 더 낮은 문서화 임계치를 적용 | Nightly가 모듈별 커버리지 artifact 업로드 |
| `bluetape4k-experimental` | 안정적인 Kover 게이트 없음 | 공개하지 않는 Java 25/Spring Boot 4 실험 작업이라는 예외를 문서화. publish 전 게이트 추가 | CI/Nightly 테스트 신호만 사용 |
| `bluetape4k-exposed` | 모듈 제외가 있는 Kover 보고서, 넓은 verify bounds 없음 | 다중 데이터베이스 통합 범위로 report-only 전환. 넓은 게이트 전 core/cache/batch 기준선 측정 | CI/Nightly가 커버리지 artifact 업로드 |
| `bluetape4k-graph` | aggregate Kover 보고서, benchmark/examples 제외 | report-only 전환. graph-io/core와 pure wrapper부터 게이트를 적용하고 DB backend에는 낮은 통합 임계치 적용 | Nightly가 커버리지 artifact 업로드 |
| `bluetape4k-image` | aggregate Kover 보고서, native/libvips 변형도 보고 | report-only 전환. pure image 모듈부터 게이트를 적용하고 native 변형은 플랫폼별 예외 적용 | Nightly가 커버리지 artifact 업로드 |
| `bluetape4k-javers` | aggregate Kover 보고서, verify bounds 없음 | report-only 전환. 먼저 core를 게이트하고 Redis/Kafka persistence는 기준선 후 적용 | Nightly가 커버리지 artifact 업로드 |
| `bluetape4k-leader` | `leader-core`, `leader-micrometer`, `leader-zookeeper`는 80%, `leader-spring-boot`는 60% 강제 | 검증된 모듈은 강제하고 나머지 backend는 통합 비용 예외로 문서화 | Nightly가 강제 모듈에 `koverVerify` 실행 |
| `bluetape4k-projects` | 넓은 Kover 보고서 집계, 넓은 verify 강제 없음 | 대부분 모듈 report-only 전환. 실패 게이트 전환 전에 낮은 기준선 결과를 모듈별 후속 작업으로 분리 | Nightly가 Kover XML artifact 집계 |
| `bluetape4k-text` | Nightly에서 Kover 보고서 생성, `text-search` benchmark package 제외 | report-only 전환. 기준선 후 tokenizer/text-search 모듈은 80% 게이트 후보 | Nightly가 모듈별 커버리지 artifact 업로드 |
| `bluetape4k-workshop` | production Kover 게이트 없음 | workshop/demo 예외를 문서화. 커버리지는 참고 정보만 사용 | Nightly 테스트 신호만 사용 |

## 저장소별 정책 문서

위 목록의 각 저장소는 다음 내용을 담은
`docs/governance/kover-coverage-policy.md`를 소유해야 합니다.

- 현재 Kover 상태
- 강제 모듈과 임계치(있는 경우)
- 문서화한 예외
- 임계치 후속 계획
- CI/Nightly task 계약

## 승격 규칙

최근 측정 기준선과 현실적인 개선 경로가 없는 모듈에는 실패하는
`koverVerify` bounds를 추가하지 않습니다. bounds를 추가한 뒤에는 CI 또는
Nightly가 해당 `koverVerify` task를 실행해야 합니다.
