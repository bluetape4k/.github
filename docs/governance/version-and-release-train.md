# bluetape4k version 거버넌스와 release train

## 목적

이 문서는 2026년 5월 말 예정된 공식 release를 지원합니다. 공유 dependency
drift 검사, 조직 전체 Nightly dispatch, snapshot publish, release train
dispatch의 중앙 운영 표면을 정의합니다.

의존성 업데이트 소유권과 검증 단계는
`docs/governance/dependency-governance.md`에 정의합니다.

## Token 요구사항

저장소 간 workflow dispatch에는 조직 범위 token이 필요합니다. 중앙
`.github` 저장소는 repository 또는 organization secret으로
`ORG_WORKFLOW_TOKEN`을 정의해야 합니다.

권장 token 형태:

- GitHub App installation token 또는 fine-grained PAT
- train이 관리하는 모든 bluetape4k 저장소 접근
- 권한: Actions read/write, Contents read, Metadata read

중앙 workflow는 대상 저장소에 이미 존재하는 workflow만 dispatch합니다.
Publish credential, signing key, package permission은 각 대상 저장소에
남겨 둡니다.

## 중앙 workflow

| Workflow | 목적 | 기본 안전장치 |
|---|---|---|
| `Org Version Drift` | bluetape4k 저장소를 clone해 공유 version drift 보고서 생성 | 주간 보고, 선택적 fail-on-drift |
| `Org Nightly Dispatch` | 선택 저장소의 Nightly workflow 실행 | 수동 실행만 허용, 기본 `dryRun=true` |
| `Org Snapshot Dispatch` | train 순서로 snapshot publish workflow 실행 | 수동 실행, `dryRun=true`, 실제 dispatch에는 확인 문구 필요 |
| `Org Release Train` | train 순서로 release workflow 실행 | 수동 실행, `dryRun=true`, 실제 dispatch에는 확인 문구 필요 |

## Train 순서

Snapshot dispatch의 기본 순서는 다음과 같습니다.

1. `bluetape4k-projects`
2. `bluetape4k-exposed`
3. `bluetape4k-text`
4. `bluetape4k-graph`
5. `bluetape4k-javers`
6. `bluetape4k-aws`
7. `bluetape4k-leader`
8. `bluetape4k-image`
9. `bluetape4k-dependencies`

`bluetape4k-dependencies`는 생태계 BOM이므로 이를 조정하는 library를 모두
publish한 뒤 마지막에 publish합니다. Gradle build catalog는 최종 BOM이
아니며 Maven Central publication 대상도 아닙니다. train에서 외부 dependency
alias나 plugin version을 갱신해야 하면 `catalog/2026-05-23-00` 같은
불변 `bluetape4k-dependencies` git ref를 만듭니다.

Release dispatch도 같은 순서를 사용하고 `bluetape4k-dependencies`를 최종
BOM으로 둡니다. `bluetape4k-experimental`과 `bluetape4k-workshop`은 기본적으로
Nightly만 실행합니다.

## Version Management Policy

이 section은 `bluetape4k-*` workspace version 관리의 canonical 규칙입니다.
Release runbook과 checklist는 이 규칙의 실행 표면입니다.

### 저장소 artifact version

- Publish 대상 저장소는 `gradle.properties`에
  `baseVersion=<next release version>`, `snapshotVersion=`을 둡니다.
- Release가 끝나면 `develop`의 `baseVersion`을 다음 release version으로
  즉시 올립니다. 예를 들어 `0.2.1` 뒤에는 `baseVersion=0.2.2`입니다.
- Git에는 `snapshotVersion=`을 빈 값으로 남깁니다. 개발 상태 표시를 위해
  `gradle.properties`에 `-SNAPSHOT`을 기록하지 않습니다.
- Snapshot artifact는 `-PsnapshotVersion=-SNAPSHOT` workflow 또는 명령 입력으로만
  생성합니다.
- Release artifact는 `baseVersion`만 사용합니다. Release workflow는
  `snapshotVersion`이 비어 있지 않거나 `-SNAPSHOT`을 주입하면 실패해야 합니다.

| 상태 | `baseVersion` | `snapshotVersion` | 공개 artifact version |
|---|---|---|---|
| Release 후 일반 개발 | 다음 release version | 빈 값 | Git만으로는 없음 |
| Snapshot workflow | 다음 release version | `-SNAPSHOT` 주입 | `<baseVersion>-SNAPSHOT` |
| Release prep와 tag | release version | 빈 값 | `<baseVersion>` |
| Maintenance branch | 해당 line의 다음 patch | 빈 값 | workflow가 주입할 때만 `<baseVersion>` 또는 `<baseVersion>-SNAPSHOT` |

### 내부 bluetape4k reference

- 일반 개발 중 다른 `bluetape4k-*` artifact를 의존하면 일치하는 upstream
  `-SNAPSHOT` version을 사용합니다. 예를 들어 `bluetape4k-projects`가
  `1.9.2`를 개발 중이면 downstream이 `bluetape4k-bom = 1.9.2-SNAPSHOT`
  또는 같은 의미의 local key를 사용합니다.
- Release prep에서 내부 reference의 `-SNAPSHOT`을 제거하는 시점은 upstream
  release가 공개되고 Maven Central artifact가 HTTP 200을 반환한 뒤입니다.
- 목표 upstream release가 아직 보이지 않는다고 이전 공개 release로
  돌아가지 않습니다. upstream release를 기다리거나 develop branch에서
  일치하는 snapshot을 계속 사용합니다.
- `bluetape4k-dependencies`는 최종 consumer BOM입니다. import한 모든 BOM이
  공개된 뒤 release하며, 같은 train 안의 internal release version source로
  최종 dependencies BOM을 사용하지 않습니다.

| 단계 | 내부 reference 예 | 규칙 |
|---|---|---|
| 개발 | `bluetape4k = "1.9.2-SNAPSHOT"` | 일치하는 upstream snapshot line 소비 |
| Upstream 공개 전 release prep | `1.9.2-SNAPSHOT` 유지 | 중지; downstream을 아직 release하지 않음 |
| Upstream HTTP 200 후 release prep | `bluetape4k = "1.9.2"` | suffix 제거 후 Maven Central의 정확한 artifact 검증 |
| Release 후 reopen | `bluetape4k = "1.9.3-SNAPSHOT"` 또는 다음 upstream snapshot | 개발을 snapshot 소비로 복귀 |

### Gradle catalog와 consumer BOM

- `bluetape4k-dependencies/gradle/libs.versions.toml`은 외부 library와
  plugin 정렬을 위한 build/contributor catalog source입니다. 공통으로
  사용할 때 `catalog/YYYY-MM-DD-NN` git ref로 고정합니다.
- `io.github.bluetape4k:bluetape4k-dependencies`는 사용자용 consumer BOM이며
  `1.1.3` 같은 semantic version을 사용합니다.
- Build catalog source에는 `bluetape4kDependenciesCatalogPath` 또는
  `bluetape4kDependenciesCatalogRef`를 사용합니다. Consumer BOM을 platform으로
  import할 때만 `bluetape4kDependenciesVersion`을 사용합니다.

### Branch line

- `develop`은 활성 release line입니다. Patch release는 milestone이 닫히거나
  명시적으로 연기될 때까지 보통 `develop`에서 계속합니다.
- `develop`이 다음 minor line으로 전진한 뒤 이전 minor line에 hotfix가
  필요할 때만 `release/X.Y.x`를 만듭니다.
- Maintenance branch에는 bug, security, compatibility fix만 넣고 모든 수정은
  `develop`으로 forward-port합니다.

## Branch line 정책

`develop`에서 순차 개발을 기본으로 합니다. 활성 patch milestone이 다음
release를 소유하고 있으면 이를 완료하거나 명시적으로 연기하기 전에는
`develop`을 다음 minor version으로 옮기지 않습니다.

Maintenance branch는 필요할 때만 사용합니다.

- `develop`이 다음 minor로 전진한 뒤 patch hotfix가 필요하면 마지막 `X.Y.Z`
  tag에서 `release/X.Y.x`를 만듭니다.
- 예를 들어 `1.9.2` tag에서 `baseVersion=1.9.3`으로 시작합니다.
- maintenance branch에는 bug, security, 저위험 compatibility fix만 적용합니다.
- `1.9.3` 같은 patch tag는 maintenance branch에서 만듭니다.
- 모든 maintenance 수정은 cherry-pick 또는 merge로 `develop`에 forward-port합니다.
- 다음 minor feature/API 작업을 maintenance branch로 backport하지 않습니다.

이 정책은 일반 작업을 단순하게 유지하면서 다음 minor 개발 중 이전 minor line을
수정할 수 있게 합니다. 저장소 version line 변경은
`Version Management Policy > Repository Artifact Version`의 적용을 받습니다.

## Release 전제조건

`Org Release Train`을 `dryRun=false`로 실행하기 전에 다음을 모두 확인합니다.

- 공유 version drift에 계획하지 않은 drift가 없습니다.
- 각 대상 저장소에 요청 version과 일치하는 release tag가 있습니다.
- `snapshotVersion=`이 비어 있고 release workflow가 `baseVersion`만 사용합니다.
- release-prep branch의 내부 `bluetape4k-*` reference는 공개된 upstream
  version만 사용하며, 각 artifact가 Maven Central에서 보입니다.
- 저장소별 release workflow가 dry-run 또는 diagnostic mode에서 통과했습니다.
- 같은 dependency 상태의 snapshot train이 성공했습니다.
- 대상 저장소의 GitHub Packages publish와 signing secret이 유효합니다.

## Snapshot 전제조건

`Org Snapshot Dispatch`를 `dryRun=false`로 실행하기 전에 다음을 확인합니다.

- 대상 저장소가 의도한 `develop` 상태입니다.
- `gradle.properties`의 `snapshotVersion=`은 비어 있고 workflow가
  `-PsnapshotVersion=-SNAPSHOT`을 주입합니다.
- 개발 branch의 내부 reference는 upstream `-SNAPSHOT`과 일치합니다.
- Snapshot artifact 증거는 Central snapshot repository의
  `maven-metadata.xml`을 사용합니다. release Maven Central POM URL은 사용하지
  않습니다.
- Version drift를 정렬했거나 이유를 문서화했습니다.
- 공유 Gradle catalog를 import하는 저장소는 checkout한
  `bluetape4k-dependencies/gradle/libs.versions.toml`을
  `bluetape4kDependenciesCatalogPath` 또는
  `BLUETAPE4K_DEPENDENCIES_CATALOG_PATH`로 읽거나, 고정한
  `bluetape4kDependenciesCatalogRef` / `BLUETAPE4K_DEPENDENCIES_CATALOG_REF`로
  raw TOML을 가져옵니다.
- Nightly 실패를 이해했거나 의도적으로 waive했습니다.
- 호출자가 confirmation input에 `deploy snapshots`를 입력했습니다.

## Drift 정책

조직이 관리하는 version group은 `scripts/version_drift_report.py`로 추적합니다.

- bluetape4k artifact와 `bluetape4k-dependencies` BOM
- 날짜가 포함된 `catalog/YYYY-MM-DD-NN` ref로 고정할 수 있는 Gradle catalog
- Kotlin, Spring Boot, Testcontainers, Jackson 2/3, Exposed, Lettuce/Redisson,
  AWS Kotlin SDK/Smithy Kotlin, Kover, Apache Fory

보고서는 `bluetape4k-*` library 저장소의 공유 alias도 자동으로 찾습니다. 두
개 이상의 library가 같은 alias를 서로 다른 값으로 선언하면 drift를 표시하고,
존재할 경우 `bluetape4k-projects` 값을 기본 기준선으로 표시합니다.

또한 호환성 라인 위반을 실패 처리합니다. `ignite`/`ignite3`,
`kafka3`/`kafka4`, `spring-kafka`/`spring-kafka4`, `jackson`/`jackson3`,
`spring-boot`/`spring-boot4`는 지원 major line을 인코딩합니다. coordinate가
resolve되더라도 `ignite`를 3.x로 바꾸거나 `spring-kafka4`를 3.x로 바꾸는 PR은
유효하지 않습니다.

허용한 drift는 release freeze 전에 release note 또는 연결된 Issue에 기록합니다.
Experimental과 Java 25 전용 모듈은 이유가 명확하면 예외가 될 수 있습니다.

Drift 보고 범위는 주요 bluetape4k library와 관리 대상 workshop/example
저장소입니다. `ocean-workshop`과 `kotlin-dev-agent`는 의도적으로 제외합니다.

관리 대상 workshop/example/application 저장소는
`bluetape4k-dependencies`를 유일한 bluetape4k version source로 소비해야
합니다. `gradle/libs.versions.toml`에 `io.github.bluetape4k*` artifact version을
개별 pin하지 않고 BOM을 통해 versionless alias로 resolve합니다.

`bluetape4k-*` library 저장소에서는 build catalog 소비와 BOM 소비를 분리합니다.

- Checkout한 `bluetape4k-dependencies/gradle/libs.versions.toml`에는
  `bluetape4kDependenciesCatalogPath` 또는 `BLUETAPE4K_DEPENDENCIES_CATALOG_PATH`,
  git ref에는 `bluetape4kDependenciesCatalogRef` 또는
  `BLUETAPE4K_DEPENDENCIES_CATALOG_REF`를 사용합니다.
- `io.github.bluetape4k:bluetape4k-dependencies` platform import에만
  `bluetape4kDependenciesVersion`을 사용합니다.
- 같은 repository가 release되기 전에는 존재할 수 없는 최종 BOM version을
  train의 저장소가 가리키지 않습니다.
- 개발 중에는 일치하는 upstream `-SNAPSHOT`을, release prep에서는 upstream이
  공개되고 Maven Central에서 검증된 뒤에만 suffix 없는 version을 사용합니다.

## Dependency update 검증

Dependabot은 update detector이자 PR generator입니다. 중앙 drift 보고서는
저장소 간 consistency gate입니다. 저장소 단위로 동작하는 Dependabot만으로
release 준비를 판단하지 않습니다.

| 변경 유형 | 필수 검증 |
|---|---|
| 한 저장소에 한정된 patch/minor library update | 저장소 CI, 통합 test/runtime adapter에서 쓰일 때만 targeted Nightly |
| Kotlin, Spring Boot, Gradle, Testcontainers, Jackson, Redis client, Exposed, AWS SDK, Apache Fory 같은 공유 기준선 | 저장소 CI와 영향 저장소 Nightly. 영향이 불명확하면 관리 대상 library Nightly 전체 |
| compatibility-line alias update | 인코딩된 major line 유지 확인. 다른 line으로 바꾸는 update는 거부하고 올바른 alias를 갱신 |
| `bluetape4k-dependencies` BOM update | version drift 보고서와 release/snapshot 대상 저장소 Nightly |
| major upgrade, compiler/plugin/runtime 변경 또는 release-freeze update | version drift 보고서, 영향 Nightly, release 전 수동 Weekly Full Nightly |
| 문서 또는 GitHub Actions만 변경 | workflow validation 또는 저장소 CI |

다른 저장소를 나중에 깨뜨릴 수 있는 dependency update는 CI만 확인하고
병합하지 않습니다. 영향 Nightly를 병합 전에 실행하거나 PR에 연기 사유를
기록합니다.

공유 runtime library alias를 `bluetape4k-projects`가 선언하면 조직 기본
기준선으로 취급합니다. Redis client, serialization library, persistence
adapter 등 공유 runtime 구성요소의 major update는 개별 저장소보다 먼저
`bluetape4k-projects`에서 시작합니다.
