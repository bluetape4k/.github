# bluetape4k 의존성 거버넌스

## 목적

의존성 업데이트는 세 계층으로 처리합니다.

- Dependabot은 저장소별 Gradle 및 GitHub Actions 업데이트를 감지하고
  검토 가능한 PR을 엽니다.
- 중앙 version drift 보고서는 관리 대상 저장소 사이의 공유 artifact가
  일관된지 확인합니다.
- 같은 version alias를 선언한 경우 `bluetape4k-projects`를 공유 runtime
  library의 기본 기준선으로 사용합니다.

이 분리는 의도적입니다. Dependabot은 저장소 단위로 동작하지만 release
준비 상태는 저장소 간 일관성에 달려 있습니다.

`scripts/version_drift_report.py`는 다음 범위를 검사합니다.

- 이미 release gate로 알려진 의존성을 묶은 선별 release train group
- `bluetape4k-*` library 저장소 전체에서 자동으로 찾은 공유 alias. 두 개
  이상의 library가 선언한 alias는 drift를 검사하고, 존재하면
  `bluetape4k-projects` 값을 기본 기준선으로 표시합니다.
- `ignite`/`ignite3`, `kafka3`/`kafka4`, `spring-kafka`/`spring-kafka4`,
  `jackson`/`jackson3`, `spring-boot`/`spring-boot4` 같은 호환성 라인 alias.
  Maven coordinate가 Dependabot 관점에서 업그레이드 가능해 보여도 alias는
  인코딩된 major line을 유지해야 합니다.

## 관리 대상 저장소

관리 범위는 주요 bluetape4k library와 다음 저장소를 포함합니다.

- `bluetape4k-workshop`
- `clinic-appointment`
- `exposed-workshop`
- `exposed-r2dbc-workshop`
- `timefold-workshop`

`ocean-workshop`과 `kotlin-dev-agent`는 의도적으로 제외합니다.

## Workshop 및 application consumer

Workshop, example, application 저장소는 bluetape4k release를 소비하며,
bluetape4k 생태계 버전을 독립적으로 소유하지 않습니다. 다음 저장소는
`gradle/libs.versions.toml`에서 `bluetape4k-dependencies`를 유일한
bluetape4k version source로 유지해야 합니다.

- `bluetape4k-workshop`
- `clinic-appointment`
- `exposed-workshop`
- `exposed-r2dbc-workshop`
- `timefold-workshop`

필수 catalog 형태는 다음과 같습니다.

- `bluetape4k-dependencies = "<version>"` version alias 하나를 정의합니다.
- `io.github.bluetape4k:bluetape4k-dependencies`용 library alias 하나를
  정의합니다.
- dependency management 또는 Gradle platform 설정으로 이 BOM을 import합니다.
- core, exposed, leader, assertions, test helper를 포함한
  `io.github.bluetape4k*` artifact는 version 없이 선언합니다.

`bluetape4k`, `bluetape4k-bom`, `bluetape4k-leader`,
`bluetape4k-assertions-version`, `version.ref = "bluetape4k"` 같은 consumer
측 alias를 bluetape4k artifact에 계속 사용하지 않습니다. 과거 accessor
이름을 호환성 때문에 유지해야 한다면 이름만 유지하고 현재 BOM 관리
artifact를 가리키며 version은 생략합니다.

이 저장소의 release-upgrade PR은 `bluetape4k-dependencies`가 유일한
bluetape4k version source인지 확인하고, 금지된 직접 version reference를
grep하며, 가능하면 변경한 example 또는 전체 저장소를 compile해야 합니다.

## Dependabot 기준선

관리 대상 저장소마다 `.github/dependabot.yml`에 다음을 정의합니다.

- root build용 `gradle` ecosystem
- workflow action용 `github-actions` ecosystem
- project repository의 `target-branch: develop`
- 중앙 `.github` 저장소의 `target-branch: main`
- 기본 assignee `debop`
- 적용되는 경우 Kotlin, Spring, Testcontainers, Jackson, Redis client, AWS,
  bluetape4k artifact의 그룹 업데이트

`dependabot`, `dependency update` 또는 철자가 틀린 custom 값처럼 placeholder
ecosystem을 사용한 설정은 유효한 Dependabot 설정이 아닙니다.

## 검증 단계

| 업데이트 유형 | 검증 |
|---|---|
| 저장소에 한정된 patch/minor dependency | 저장소 CI |
| 통합 테스트, 컨테이너, serialization, persistence 또는 runtime adapter에서 사용하는 dependency | 저장소 CI와 병합 전 해당 Nightly 또는 PR에 명시한 연기 근거 |
| Kotlin, Spring Boot, Gradle, Testcontainers, Jackson, Redis client, Exposed, AWS SDK, Apache Fory 같은 공유 기준선 dependency | 저장소 CI와 영향 저장소 Nightly. 영향 범위가 불명확하면 관리 대상 library Nightly 전체 실행 |
| `ignite`, `ignite3`, `kafka3`, `kafka4`, `spring-kafka`, `spring-kafka4` 같은 compatibility-line alias | platform-line 변경으로 취급. alias를 다른 major로 옮기는 PR은 거부하고 올바른 alias를 만들거나 갱신 |
| `bluetape4k-dependencies` BOM | version drift 보고서와 release/snapshot 대상 Nightly |
| major/runtime/compiler/plugin 업데이트 | version drift 보고서, 영향 Nightly, release 전 수동 Weekly Full Nightly |

이 목적은 며칠 뒤 다른 저장소에서 깨짐을 발견하는 일을 막는 것입니다.
고위험 업데이트를 저장소 CI만 확인하고 병합하지 않습니다.

## 현재 drift 메모

Testcontainers, Jackson, Redis client 기준선은 관리 대상 저장소 전체에서
맞춰야 합니다. Lettuce와 Redisson 같은 Redis client의 major 버전 도입은
`bluetape4k-projects`에서 먼저 시작하고, 해당 runtime adapter를 먼저 검증한
뒤 조직 전체에 맞춥니다.

호환성 라인 alias는 서로 바꿔 쓸 수 없습니다. `ignite`는 Apache Ignite
2.x이고 `ignite3`는 Apache Ignite 3.x입니다. `spring-kafka`는 3.x line이고
`spring-kafka4`는 4.x line입니다. Dependabot이 이전 alias를 새 major로
바꾸는 PR은 병합하지 않습니다.

Apache Fory는 serialization 중심 모듈과 example에 사용이 집중되어 현재
알려진 drift가 있습니다. 2026년 5월 release freeze 전까지 Fory를 정렬하거나,
각 예외가 의도적인 이유와 이를 덮은 Nightly 실행을 연결한 Issue를 남깁니다.
