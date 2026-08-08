# bluetape4k Central Portal Release Runbook

이 문서는 독립적인 `bluetape4k-*` 라이브러리 저장소에 적용하는 반복 가능한 릴리스 절차다. 2026-05-17 Central Portal 릴리스 배치를 반영하며, 대상은 다음과 같다: `projects 1.8.0`, `aws 0.1.0`, `text 0.1.0`, `graph 0.3.0`, `javers 0.1.0`, `exposed 1.8.0`, `leader 0.1.0`, `image 0.1.0`, `dependencies 1.0.0`.

## Release Flow Map

명령을 선택하기 전에 이 맵을 확인한다. 대부분의 릴리스 오류는 앞 단계의 게이트가 아직 해결되지 않았는데 뒤 단계를 실행하면서 발생한다.

| Phase | Branch state | Version state | Required evidence | Next action |
|---|---|---|---|---|
| Normal development | `develop` | 자체 `baseVersion`은 다음 릴리스 버전이고 `snapshotVersion=`은 비어 있으며, 내부 bluetape4k 참조는 일치하는 `-SNAPSHOT`을 사용 | CI/Nightly가 허용 가능하고 drift를 파악함 | 개발을 계속하거나 snapshot을 게시 |
| Snapshot validation | `develop` | 일반 개발과 동일하며 snapshot suffix는 workflow에서만 주입 | `publish-snapshot.yml`이 dependency order대로 성공 | 필요한 upstream snapshot을 입증한 뒤에만 release prep 시작 |
| Release prep | `develop`에서 만든 PR branch | 자체 `baseVersion`이 release tag와 같고 `snapshotVersion=`은 비어 있으며, 내부 bluetape4k 참조는 upstream의 HTTP 200 확인 후에만 release non-snapshot 버전 사용 | pre-release checklist PASS, release workflow dry-run 또는 diagnostic clean | release-prep PR 병합 |
| Tag and release | release-prep commit에 위치한 `develop` | tag가 `baseVersion`과 같고 체크인된 snapshot suffix가 없음 | GitHub release workflow 성공, Central Portal이 publication 수락 | Maven Central에서 HTTP 200이 될 때까지 polling |
| Post-release reopen | release 이후의 `develop` | 자체 `baseVersion`을 다음 릴리스로 올리고 `snapshotVersion=`은 유지하며, 필요한 경우 개발용 내부 참조를 일치하는 `-SNAPSHOT`으로 복원 | PR CI가 clean이고 snapshot train을 실행할 수 있음 | reopen PR 병합 후 snapshot 게시 |
| Final dependencies BOM | import한 BOM이 공개된 이후 | `bluetape4k-dependencies`가 release된 BOM만 import | import한 모든 BOM이 Maven Central에서 HTTP 200 반환 | 마지막에 `bluetape4k-dependencies` 릴리스 |

현재 phase가 필요한 evidence를 충족하지 못하면 중지한다. downstream 저장소를 더 오래된 upstream release로 변경해 보상하지 않는다.

## Release Policy

- 표준 버전 정책은 `docs/governance/version-and-release-train.md`의 `Version Management Policy`를 따른다.
- `gradle.properties`를 안정적으로 유지한다: `baseVersion=<next release version>` 및 `snapshotVersion=`.
- `publish-snapshot.yml`에서 `-PsnapshotVersion=-SNAPSHOT`을 전달해 snapshot을 게시한다.
- release는 `baseVersion`만 사용해 게시하며, `release.yml`은 `-SNAPSHOT`을 주입하지 않아야 한다.
- 개발 branch에서는 내부 `bluetape4k-*` dependency가 일치하는 upstream `-SNAPSHOT` 버전을 가리킨다. release-prep PR에서는 참조한 upstream release가 Maven Central에 표시된 뒤에만 suffix를 제거한다.
- tag push가 release trigger다. tag는 `X.Y.Z`와 일치해야 한다.
- `experimental`, `workshop`, examples, demos, benchmarks는 release artifact가 아니다.
- `bluetape4k-dependencies`는 import한 모든 BOM이 Maven Central에 표시된 뒤 마지막으로 릴리스한다.
- 같은 release train에 속한 저장소의 build-time Gradle catalog version으로 최종 `bluetape4k-dependencies` BOM version을 사용하지 않는다. 해당 저장소들이 이미 릴리스되어야 최종 BOM이 존재할 수 있으므로 순환이 생긴다.
- `bluetape4k-dependencies`는 distribution path가 다른 두 가지 대상으로 구분한다.
  - `bluetape4k-dependencies`는 최종 consumer BOM이며 `1.1.3`과 같은 semantic version을 사용한다.
  - `gradle/libs.versions.toml`은 `bluetape4k-*` 저장소 전체의 external library와 plugin version 정렬을 위한 내부 build/contributor catalog다. `bluetape4k-dependencies` 저장소를 release-train tag 또는 commit으로 checkout해 고정하며, 이를 Maven Central artifact로 게시하지 않는다.
- Public release artifact, PR, issue, changelog entry, release note, commit message는 한국어로 작성한다. code identifier, URL, exact error, machine-required token은 보존한다.

## BOM vs Catalog Roles

모든 release 결정에서 다음 역할을 분리한다.

`bluetape4k-dependencies`는 사용자용 Maven BOM이다. application 또는 workshop의 dependency 선언에서 platform으로 사용한다.

```kotlin
dependencies {
    implementation(platform("io.github.bluetape4k:bluetape4k-dependencies:1.1.3"))
    implementation("io.github.bluetape4k.leader:bluetape4k-leader-core")
}
```

BOM은 dependency resolution에 참여한다. 사용자가 BOM을 import하면 version을 생략한 `io.github.bluetape4k*` dependency가 BOM이 관리하는 version으로 resolve된다.

`bluetape4k-dependencies/gradle/libs.versions.toml`은 repository build용 Gradle authoring catalog다. contributor에게 `fory.kotlin`, Kotlin, Spring, Ktor, Exposed, Testcontainers, build plugin과 같은 중앙 관리 external library 및 plugin version을 제공한다. BOM에서 transitive하게 전달되지 않으며, 사용자가 BOM을 직접 사용할 때는 필요하지 않다.

`bluetape4k-*` 간 dependency의 release-version source로 catalog source ref를 사용하지 않는다. 내부 bluetape4k 참조는 dependency order에 따라 새로 게시된 upstream release version을 가리켜야 한다. 이것이 repository release 순서를 두는 이유다.

따라서 repository build는 release-train validation에서 checkout한 `bluetape4k-dependencies` repo의 catalog file을 읽어야 한다.

```properties
bluetape4kDependenciesCatalogPath=../bluetape4k-dependencies/gradle/libs.versions.toml
bluetape4kDependenciesCatalogRef=catalog/2026-05-23-00
```

그리고 해당 file에서 catalog를 import한다.

```kotlin
val bluetape4kDependenciesCatalogFile = file(
    providers.gradleProperty("bluetape4kDependenciesCatalogPath")
        .orElse(providers.environmentVariable("BLUETAPE4K_DEPENDENCIES_CATALOG_PATH"))
        .orElse("../bluetape4k-dependencies/gradle/libs.versions.toml")
        .get(),
)

dependencyResolutionManagement {
    versionCatalogs {
        create("bt4k") {
            from(files(bluetape4kDependenciesCatalogFile))
        }
    }
}
```

일반 개발과 PR CI에서는 `develop`의 repo-local `bluetape4k-dependencies` raw TOML로 fallback할 수 있다. 그러나 release validation에서는 명시적인 checkout path 또는 `bluetape4kDependenciesCatalogRef`를 전달해 train을 감사 가능한 source ref로 고정해야 한다.

이 property를 `bluetape4kDependenciesVersion`으로 이름 짓지 않는다. 이 이름은 repository가 `io.github.bluetape4k:bluetape4k-dependencies`를 platform으로 실제 import할 때 최종 사용자용 BOM에 예약되어 있다.

### Catalog Source Ref Format

내부 catalog source cut에는 날짜가 포함된 tag 또는 branch name을 사용한다.

```text
catalog/YYYY-MM-DD-NN
```

예:

- `catalog/2026-05-23-00`: release train의 첫 catalog source 버전.
- `catalog/2026-05-23-02`: train의 upstream repository 하나가 릴리스된 뒤, 이후 repository가 새 BOM을 필요로 해서 만든 두 번째 catalog source cut.

counter는 날짜별로 관리하며 `00`에서 시작한다. 새로운 immutable source ref를 게시할 때만 증가시킨다. release 작업이 이미 사용한 tag를 다시 쓰지 않는다.

예를 들어 `bluetape4k-dependencies`를 `catalog/2026-05-23-00`으로 tag하고, downstream release job에서 해당 tag를 checkout한 뒤 `bluetape4kDependenciesCatalogPath`가 그 checkout을 가리키도록 build를 검증한다. 이전 source cut에서 catalog shape가 입증된 뒤에만 새 catalog tag를 만든다.

### Release-Train Catalog Flow

여러 repository로 구성된 release train은 다음 순서로 진행한다.

1. 각 candidate repository의 마지막 tag부터 `origin/develop`까지를 audit한다. 열려 있는 bug/blocker issue, open PR, milestone state, tag 이후 변경이 다음 patch release에 포함되는지를 확인한다.
2. downstream repository에 새 shared external library 또는 plugin version이 필요하면 먼저 build catalog source ref를 만든다. 예를 들어 `fory-kotlin:0.17.0`과 같은 external version을 포함해 `bluetape4k-dependencies`를 `catalog/2026-05-23-00`으로 tag한다.
3. downstream release job 또는 local build가 checkout한 `bluetape4k-dependencies` ref의 `gradle/libs.versions.toml`을 `bluetape4kDependenciesCatalogPath`로 읽도록 변경한 뒤, 어떤 downstream release tag도 push하기 전에 아래 snapshot validation gate를 실행한다.
4. train 중 catalog content가 바뀌면 새 `catalog/YYYY-MM-DD-NN` ref를 만들고 downstream job을 해당 ref로 변경한다.
5. dependency order대로 repository를 릴리스한다. 같은 train의 앞 repository에서 만든 BOM이 뒤 repository에 필요하면 먼저 앞 repository를 게시하고, Maven Central에 BOM이 표시될 때까지 기다린 다음 뒤 repository의 local internal bluetape4k version reference를 올린다. catalog source ref를 internal bluetape4k release-version source로 사용하지 않는다.
6. import한 모든 BOM이 Maven Central에 표시된 뒤 최종 `bluetape4k-dependencies` BOM을 릴리스한다. 이 release는 user-facing BOM을 게시하며 internal build catalog는 게시하지 않는다.
7. 최종 `bluetape4k-dependencies` BOM과 versionless `io.github.bluetape4k*` dependency를 사용해 user-facing downstream build를 검증한다.

이 흐름은 다음과 같은 일반적인 순환을 방지한다.

```text
repo A needs final dependencies BOM
final dependencies BOM needs repo A release
```

catalog는 external dependency version을 중앙화하고 downstream build migration을 이끌 수 있지만 repository release order를 대체할 수 없다. `bluetape4k-*` 간 dependency에서는 참조하는 upstream release version을 새로 게시된 release version으로 설정하고 public하게 resolve할 수 있어야 한다. 최종 BOM이 train을 닫는다.

## Repository Order

편의가 아닌 dependency order를 사용한다.

1. `bluetape4k-projects`
2. 해당하는 경우 `projects`에만 의존하는 repository: `bluetape4k-exposed`, `bluetape4k-text`, `bluetape4k-graph`, `bluetape4k-javers`
3. release된 `exposed` 또는 다른 bluetape4k repo에 의존하는 repository: `bluetape4k-aws`, `bluetape4k-leader`
4. release된 `aws`에 의존하는 repository: `bluetape4k-image`
5. `bluetape4k-dependencies`

이 목록을 shortcut으로 사용하지 않는다. 모든 release train마다 현재 `settings.gradle.kts`, `gradle/libs.versions.toml`, 모든 `build.gradle.kts`에서 repository dependency graph를 다시 계산한 뒤 순서를 승인한다. `bluetape4k-javers`가 `javers-exposed` module 또는 `io.github.bluetape4k.exposed` reference를 추가하면 `javers`를 대상 `bluetape4k-exposed` release 뒤로 이동하고, 해당 exposed version이 Maven Central HTTP 200을 반환할 때까지 기다린다.

2026-05-17 batch에서는 `bluetape4k-projects 1.8.0`이 이미 release되어 다시 게시하지 않았다. `bluetape4k-image`는 `bluetape4k-aws 0.1.0`이 Maven Central에 표시될 때까지 기다렸다. `bluetape4k-dependencies 1.0.0`은 import한 모든 BOM이 Maven Central에서 HTTP 200을 반환할 때까지 기다렸다.

## Internal Reference Preflight

위 순서로 각 repository를 준비하기 전에 해당 repository가 참조하는 모든 `io.github.bluetape4k*` version을 점검한다. `develop`에서는 내부 reference가 일반적으로 일치하는 upstream `-SNAPSHOT` line을 가리킨다. release-prep branch에서는 이미 release되었고 Maven Central에서 HTTP 200을 반환한 upstream repository에 대해서만 `-SNAPSHOT`을 제거한다.

참조한 upstream repository가 같은 release train에 속하면 해당 upstream target version이 release되고 public하게 resolve될 때까지 기다린 뒤 downstream repository를 준비하거나 release한다. 현재 이용 가능한 최신 version이라는 이유만으로 이전 public release로 fallback하지 않는다. upstream release를 아직 이용할 수 없으면 downstream development branch는 일치하는 upstream `-SNAPSHOT` reference를 유지한다.

참조한 upstream repository가 release train에 속하지 않으면 최신 public upstream release version을 사용하고 Maven Central에서 확인한다.

이 검사는 `bluetape4kDependenciesCatalogPath`와 별개다. shared catalog는 external library/plugin version 정렬에 사용하고, 내부 bluetape4k release version은 repository release order를 따른다.

일반적인 점검 명령:

```bash
rg -n 'bluetape4k(-[a-z]+)? = "|bluetape4k-.*-bom = "|io\.github\.bluetape4k' \
  gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts

rg -n 'exposed|bluetape4k-exposed|io\.github\.bluetape4k\.exposed|bluetape4k\.exposed' \
  settings.gradle.kts gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts

curl -s -o /dev/null -w "%{http_code}" \
  "https://repo.maven.apache.org/maven2/io/github/bluetape4k/bluetape4k-bom/<version>/bluetape4k-bom-<version>.pom"

curl -s -o /dev/null -w "%{http_code}" \
  "https://repo.maven.apache.org/maven2/io/github/bluetape4k/aws/bluetape4k-aws-bom/<version>/bluetape4k-aws-bom-<version>.pom"

curl -s -o /dev/null -w "%{http_code}" \
  "https://repo.maven.apache.org/maven2/io/github/bluetape4k/exposed/bluetape4k-exposed-bom/<version>/bluetape4k-exposed-bom-<version>.pom"
```

기대 결과:

- `bluetape4k-projects` target version이 release되어 표시된 뒤에야 exposed/text/graph/javers, aws, leader 또는 image가 reference에서 `-SNAPSHOT`을 제거한다.
- aws가 exposed module을 참조하고 exposed가 train에 속하면 먼저 exposed target version을 release하고 확인한 뒤 aws의 exposed reference를 올린다.
- 예를 들어 javers가 exposed module을 참조하는 향후 `javers-exposed` module을 추가하면 먼저 exposed target version을 release하고 확인한 뒤 javers의 exposed reference를 올린다.
- image가 aws를 참조하고 aws가 train에 속하면 먼저 aws target version을 release하고 확인한 뒤 image의 aws reference를 올린다.
- leader 또는 다른 repo가 exposed artifact를 참조하고 exposed가 train에 속하면 먼저 exposed target version을 release하고 확인한다.
- `bluetape4k-dependencies`는 library release order의 shortcut으로 사용하지 않는다. import한 모든 BOM이 표시된 뒤 마지막에 release한다.

## Preflight

tagging 전에 각 repository에서 실행한다.

```bash
git switch develop
git pull --ff-only
git status --short --branch
grep -E '^(baseVersion|snapshotVersion)=' gradle.properties
grep -E '^bluetape4kDependenciesCatalogPath=' gradle.properties || true
rg 'SNAPSHOT' gradle/libs.versions.toml gradle.properties build.gradle.kts \
  --glob '!gradle.properties' \
  | grep -v 'snapshotVersion\|central-snapshot\|maven-snapshots\|# ' || true
gh pr list --state open
gh api "repos/bluetape4k/$(basename "$PWD")/milestones?state=open&per_page=100" \
  --jq '.[] | [.title,.open_issues,.closed_issues] | @tsv'
gh issue list --state open --milestone "<target-version>" --limit 100
rg -n 'bluetape4k(-[a-z]+)? = "|bluetape4k-.*-bom = "|io\.github\.bluetape4k' \
  gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts
```

기대 결과:

- working tree가 clean이다.
- local `develop`이 `origin/develop`과 같다.
- `baseVersion`이 게시할 tag와 같다.
- `snapshotVersion=`이 비어 있다.
- GitHub에 target version과 제목이 정확히 일치하는 milestone이 있다.
- target milestone의 모든 open issue는 release 전에 해결했거나 해당 milestone 밖으로 명시적으로 연기했다.
- 대상이 아닌 open milestone/backlog issue도 검토해 feature 작업이 patch release에 조용히 포함되지 않도록 했다.
- local repository build가 참조하는 모든 `bluetape4k-*` version이 의도한 upstream target release이고 Maven Central에서 HTTP 200을 반환한다. upstream target이 아직 publish되지 않았다면 이전 release를 사용하지 말고 중지해 기다린다.
- shared build catalog를 import하는 repository라면 Maven-published catalog artifact가 아니라 `bluetape4kDependenciesCatalogPath` 또는 `BLUETAPE4K_DEPENDENCIES_CATALOG_PATH`를 통해 `bluetape4k-dependencies/gradle/libs.versions.toml`을 읽는다.
- 아직 release되지 않은 `*-SNAPSHOT` bluetape4k dependency reference가 없다.
- release를 막는 PR이 병합되어 있다.

## BOM And Publication Guards

repository BOM을 게시하기 전에 build의 모든 release metadata path에서 non-library module이 제외되는지 확인한다.

BOM constraint, NMCP aggregation, publication/signing setup, generated ecosystem BOM entry에서 다음을 제외한다.

- `examples/`
- `*-examples`
- `*-demo`
- `benchmark/`
- `*-benchmark`

알려진 함정:

- 중첩 Gradle include는 `:examples`와 `:examples:*`를 모두 만든다. 둘 다 filter한다.
- NMCP aggregation만 filter하는 것으로는 충분하지 않다. non-library module에 `maven-publish`가 남아 있으면 Gradle이 publication을 생성할 수 있고 Central validation이 이를 볼 수 있다.
- release artifact에 대한 Spring dependency-management POM customization을 끄지 않는다. `generatedPomCustomization { setEnabled(false) }`는 dependency version metadata가 빠진 POM을 만들어 Central validation을 실패시킬 수 있다.
- `bluetape4k-dependencies` generated section은 `scripts/sync-managed-catalog.py`로 다시 생성한다. generated managed-module block을 수동 편집하지 않는다.

검증 명령:

```bash
# repo-specific publication name examples:
./gradlew clean generatePomFileForBluetapeAwsPublication --no-daemon --no-configuration-cache --no-build-cache
./gradlew clean generatePomFileForBluetapeExposedPublication --no-daemon --no-configuration-cache --no-build-cache
./gradlew clean generatePomFileForBluetapeGraphPublication --no-daemon --no-configuration-cache --no-build-cache
./gradlew clean generatePomFileForBluetapeImagePublication --no-daemon --no-configuration-cache --no-build-cache
./gradlew clean generatePomFileForBluetapeLeaderPublication --no-daemon --no-configuration-cache --no-build-cache

# generated POM scan should print nothing
rg -n 'SNAPSHOT|examples|demo|benchmark' build/publications
```

`bluetape4k-dependencies`의 경우:

```bash
python3 -m unittest tests/test_sync_managed_catalog.py
scripts/sync-managed-catalog.py --write --check --summary
./gradlew generatePomFileForBluetapeDependenciesPublication \
  --no-daemon --no-configuration-cache --no-build-cache
rg -n 'SNAPSHOT|examples|demo|benchmark' \
  build/publications/BluetapeDependencies/pom-default.xml \
  gradle/libs.versions.toml build.gradle.kts
```

## Snapshot Validation Gate

train에서 shared catalog alias, upstream BOM coordinate 또는 centrally governed dependency version을 변경하는 경우, 실제 release publish 또는 release tag push 전에 이 gate를 실행한다.

Snapshot validation은 catalog mechanics와 downstream compatibility를 입증한다. 아직 release되지 않은 upstream `bluetape4k-*` version에 downstream release가 의존하도록 허용하는 것은 아니다. Release candidate에서 내부 `bluetape4k-*` dependency version은 catalog source ref가 아니라 repository release order가 계속 관리한다.

1. `bluetape4k-dependencies`에서 shared catalog 변경을 commit하고 train을 위한 immutable source ref를 만든다.

   ```bash
   git tag catalog/YYYY-MM-DD-NN
   ```

2. 각 downstream repository에서 해당 ref로 `bluetape4k-dependencies`를 checkout하고, checkout한 TOML을 Gradle이 가리키게 한다.

   ```bash
   export BLUETAPE4K_DEPENDENCIES_CATALOG_PATH="$WORKSPACE/bluetape4k-dependencies/gradle/libs.versions.toml"
   ```

   GitHub Actions에서는 `ref: catalog/YYYY-MM-DD-NN`으로 `bluetape4k-dependencies`를 두 번째 checkout하고 같은 environment variable을 설정하거나 `-Pbluetape4kDependenciesCatalogPath=...`를 전달한다.

3. `mavenLocal()` 없이 각 영향 repository가 checkout한 catalog를 resolve하는지 확인한다.

   ```bash
   ./gradlew help --refresh-dependencies \
     --no-daemon --no-configuration-cache --no-build-cache
   ```

   repository 간 smoke check는 다음과 같이 실행한다.

   ```bash
   for repo in \
     bluetape4k-projects bluetape4k-aws bluetape4k-text bluetape4k-graph \
     bluetape4k-javers bluetape4k-exposed bluetape4k-leader bluetape4k-image
   do
     export BLUETAPE4K_DEPENDENCIES_CATALOG_PATH="$PWD/bluetape4k-dependencies/gradle/libs.versions.toml"
     (cd "$repo" && ./gradlew help --refresh-dependencies \
       --no-daemon --no-configuration-cache --no-build-cache)
   done
   ```

4. release content가 변경된 repository에는 target compile/test를 실행한다. `help`는 settings/catalog resolution만 입증하며 runtime 또는 API compatibility는 입증하지 않는다.

   downstream test result를 release evidence로 채택하기 전에 resolve된 모든 내부 upstream coordinate가 public release인지 확인한다.

   ```bash
   curl -s -o /dev/null -w "%{http_code}" \
     "https://repo.maven.apache.org/maven2/io/github/bluetape4k/bluetape4k-bom/<version>/bluetape4k-bom-<version>.pom"
   ```

downstream repository가 아직 게시되지 않은 upstream release 또는 기록되지 않은 catalog source 변경을 요구하는 동안에는 release tag를 push하거나 release artifact를 게시하지 않는다.

## Post-release Snapshot Publish Train

release와 post-release reopen PR에서 `baseVersion`을 다음 release line으로 올린 뒤 이 train을 실행한다. 이 gate는 development line의 validation이다. 내부 `bluetape4k-*` reference는 일치하는 `-SNAPSHOT` version을 사용해야 하고, 체크인된 `snapshotVersion`은 비어 있어야 한다.

dependency order를 사용하고 첫 실패에서 중지한다.

1. `bluetape4k-projects`
2. `bluetape4k-exposed`, `bluetape4k-text`, `bluetape4k-graph`, `bluetape4k-javers`
3. `bluetape4k-aws`, `bluetape4k-leader`
4. `bluetape4k-image`
5. `bluetape4k-dependencies`

각 repository에서:

```bash
git switch develop
git pull --ff-only
grep -E '^(baseVersion|snapshotVersion)=' gradle.properties
rg -n 'bluetape4k(-[a-z]+)? = "|bluetape4k-.*-bom = "|io\.github\.bluetape4k' \
  gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts
gh workflow run publish-snapshot.yml --ref develop
gh run list --workflow publish-snapshot.yml --branch develop --limit 1
```

`publish-snapshot.yml`이 모든 repository에서 같은 input을 받는다고 가정하지 않는다. repository에 `diagnoseSigning` input이 없으면 `--field diagnoseSigning=false` 없이 dispatch한다.

각 publish가 성공한 뒤에는 release Maven Central POM URL이 아니라 snapshot repository에서 snapshot metadata를 확인한다.

```bash
curl -fsSL \
  "https://central.sonatype.com/repository/maven-snapshots/<group-path>/<artifact>/<version>-SNAPSHOT/maven-metadata.xml" \
  | rg '<lastUpdated>|<timestamp>|<buildNumber>'
```

`bluetape4k-dependencies`의 경우 catalog가 `-SNAPSHOT` BOM을 import하는 동안 CI와 local verification에서 snapshot metadata check를 사용한다.

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
scripts/verify-managed-artifacts.py --summary --allow-snapshots
```

release-prep branch는 strict release verification으로 다시 전환해야 한다. 참조한 모든 upstream release가 Maven Central에 public하게 표시된 뒤에만 내부 `-SNAPSHOT` reference를 제거한다.

## Release PR

preflight에서 변경이 필요하면 먼저 PR을 만든다. 일반적인 release-prep 변경은 다음과 같다.

- version catalog reference는 `-SNAPSHOT`이 아닌 release version을 사용한다. 참조한 upstream release가 Maven Central에 표시된 뒤에만 수행한다.
- `baseVersion`은 push할 tag와 이미 같아야 한다. post-release reopen PR이라면 대신 `baseVersion`을 다음 release version으로 올리고 `snapshotVersion=`은 비워 둔다.
- BOM artifact/version key가 일치한다. 예를 들면 `bluetape4k-bom`과 `bluetape4k-exposed-bom`이다.
- non-library module filter가 있다.
- `CHANGELOG.md`에 tag용 release section이 있다.
- release별 결정을 간결한 lesson에 기록한다. repository별 동작은 repo-local `docs/lessons/YYYY-MM-DD-*.md`를 사용하고, organization-wide release process 동작은 `.github/docs/lessons/YYYY-MM-DD-*.md`를 사용한다.

release-prep PR은 기본적으로 rebase merge를 사용한다.

```bash
git switch -c chore/release-prep-X.Y.Z
git add <files>
git commit -m $'<intent line>\n\n<body>\n\nConstraint: ...\nConfidence: high\nScope-risk: narrow\nDirective: ...\nTested: ...\nNot-tested: ...'
git push -u origin chore/release-prep-X.Y.Z
gh pr create --base develop --head chore/release-prep-X.Y.Z --assignee debop
gh pr view <PR> --json mergeStateStatus,statusCheckRollup
gh pr merge <PR> --rebase --delete-branch
git switch develop
git pull --ff-only
```

## Tag And Release

```bash
git tag -a X.Y.Z -m "Release X.Y.Z"
git push origin X.Y.Z
sleep 5
gh run list --workflow release.yml --limit 3 \
  --json databaseId,status,conclusion,headBranch,headSha,createdAt,event
```

실행을 모니터링한다.

```bash
gh run watch <RUN_ID> --interval 20 --exit-status
```

기대 job:

1. `Resolve release version`
2. `Publish RELEASE to Maven Central Portal`
3. `Create GitHub Release`

모든 job이 성공해야 한다.

## Central Portal And Maven Central Verification

workflow는 public Maven Central repository에 artifact가 표시되기 전에 성공할 수 있다. GitHub Actions 성공은 "Central Portal accepted"로, Maven Central HTTP 200은 "consumers can resolve it"으로 취급한다.

Maven Central을 polling한다.

```bash
for i in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://repo.maven.apache.org/maven2/<group-path>/<artifact>/<version>/<artifact>-<version>.pom")
  echo "$code <artifact>"
  [ "$code" = "200" ] && break
  sleep 20
done
```

`zsh`에서는 `path`를 loop variable로 사용하지 않는다. `path`가 `PATH`에 alias되어 shell 내부 명령을 망가뜨릴 수 있다. `artifact_path` 또는 다른 이름을 사용한다.

## Failed Release Recovery

tag push 후 Central validation이 실패하면:

1. 실패한 job log를 읽는다.
2. 일반 PR branch에서 repository를 수정한다.
3. PR CI가 clean해질 때까지 기다린다.
4. `develop`에 병합한다.
5. local `develop`을 fast-forward한다.
6. `--force-with-lease`를 사용해 실패한 tag를 수정된 commit으로 다시 쓴다.

```bash
git switch develop
git pull --ff-only
git fetch origin --tags --force
old_tag=$(git rev-parse refs/tags/X.Y.Z)
git tag -fa X.Y.Z -m "Release X.Y.Z"
git push --force-with-lease=refs/tags/X.Y.Z:$old_tag origin refs/tags/X.Y.Z
```

실패했거나 사용할 수 없는 release에 대해서만 tag를 다시 쓴다. 명시적인 release 결정 없이 이미 성공적으로 소비된 tag를 다시 쓰지 않는다.

## `bluetape4k-dependencies` Final Release

`bluetape4k-dependencies`를 tagging하기 전에 import한 모든 BOM이 Maven Central에 표시되는지 확인한다.

```bash
for artifact_path in \
  io/github/bluetape4k/bluetape4k-bom/1.8.0/bluetape4k-bom-1.8.0.pom \
  io/github/bluetape4k/aws/bluetape4k-aws-bom/0.1.0/bluetape4k-aws-bom-0.1.0.pom \
  io/github/bluetape4k/image/bluetape4k-image-bom/0.1.0/bluetape4k-image-bom-0.1.0.pom \
  io/github/bluetape4k/text/bluetape4k-text-bom/0.1.0/bluetape4k-text-bom-0.1.0.pom \
  io/github/bluetape4k/graph/bluetape4k-graph-bom/0.3.0/bluetape4k-graph-bom-0.3.0.pom \
  io/github/bluetape4k/leader/bluetape4k-leader-bom/0.1.0/bluetape4k-leader-bom-0.1.0.pom \
  io/github/bluetape4k/exposed/bluetape4k-exposed-bom/1.8.0/bluetape4k-exposed-bom-1.8.0.pom \
  io/github/bluetape4k/javers/bluetape4k-javers-bom/0.1.0/bluetape4k-javers-bom-0.1.0.pom
do
  curl -s -o /dev/null -w "%{http_code} $artifact_path\n" \
    "https://repo.maven.apache.org/maven2/$artifact_path"
done
```

모든 줄이 `200`을 반환한 뒤에만 `bluetape4k-dependencies`를 tag한다.

최종 `bluetape4k-dependencies` release workflow는 `BluetapeDependencies` publication만 게시한다. 내부 Gradle catalog는 `bluetape4k-dependencies` git ref에서 소비하며 Maven Central publication이 아니다.

## Website Documentation Refresh

최종 release artifact가 Maven Central에 표시된 뒤, 같은 release train에서 `bluetape4k.github.io`를 갱신한다. website는 현재 dependency coordinate의 public entrypoint이므로 게시된 BOM보다 뒤처지면 안 된다.

release version이 변경되면 최소한 다음 page를 English와 Korean 모두 갱신한다.

- `src/content/docs/getting-started.mdx`
- `src/content/docs/ko/getting-started.mdx`
- `src/content/docs/ecosystem/version-governance.mdx`
- `src/content/docs/ko/ecosystem/version-governance.mdx`
- `src/content/docs/ecosystem/repositories.mdx`
- `src/content/docs/ko/ecosystem/repositories.mdx`

검증:

```bash
cd ../bluetape4k.github.io
npm run build
git diff --check
```

website PR을 병합한 뒤 GitHub Pages deployment와 live page를 확인한다.

```bash
gh run list --workflow="Deploy Website" --limit 3 \
  --json databaseId,status,conclusion,headBranch,headSha,createdAt
curl -fsSL https://bluetape4k.github.io/ecosystem/version-governance/ \
  | rg 'bluetape4k-dependencies|bluetape4k-bom|bluetape4k-.*-bom'
```

website PR, deploy run URL, live-page evidence를 release note 또는 release lesson에 기록한다.

## Post-release

```bash
gh release view X.Y.Z --json tagName,publishedAt,url
git status --short --branch
```

다음을 기록한다.

- release workflow 실행 ID
- GitHub Release URL
- 대표 artifact의 Maven Central HTTP 200 확인 근거
- repository가 `develop`에서 계속 진행하는 경우 post-release reopen PR: `baseVersion`을 다음 release로 올리고 `snapshotVersion=`은 비워 두며, development에서 snapshot을 소비해야 하는 내부 bluetape4k reference는 일치하는 `-SNAPSHOT`으로 되돌림
- downstream development에 새 snapshot이 필요한 경우 reopen PR 이후 snapshot workflow run ID
- dependency order snapshot train 확인 근거: downstream repo가 소비한 각 upstream BOM의 PR URL, publish run ID, snapshot `maven-metadata.xml` timestamp
- `bluetape4k.github.io` PR 및 GitHub Pages 배포 확인 근거
- 모든 Central validation 실패 및 복구 PR

## Common Failures

| Symptom | Cause | Fix |
|---|---|---|
| Central validation reports missing dependency versions | Spring dependency-management generated POM customization disabled | 게시된 module에서 `generatedPomCustomization { setEnabled(false) }`를 제거하고 POM을 다시 생성 |
| Central validation includes `examples@<version>` | `:examples` parent project was not excluded | `path == ":examples"`와 `path.startsWith(":examples:")`를 모두 filter |
| BOM includes benchmark aliases | generator or BOM constraints only excluded examples | `benchmark/`와 `*-benchmark`를 제외하고 `bluetape4k-dependencies`를 다시 생성 |
| Release workflow succeeds but Maven Central returns 404 | Central Portal accepted, public repository has not propagated | `repo.maven.apache.org`를 polling해 HTTP 200이 될 때까지 대기 |
| Tag push points to wrong commit after a failed release | fix PR merged after tag was created | `--force-with-lease=refs/tags/X.Y.Z:<old-tag>`로 retag |
| `zsh: command not found: curl` inside polling loop | loop variable named `path` overwrote zsh `PATH` | loop variable을 `artifact_path`로 변경 |
| `gh workflow run publish-snapshot.yml --field diagnoseSigning=false` returns HTTP 422 | repository workflow has no `diagnoseSigning` input | workflow input을 확인한 뒤 해당 field 없이 dispatch |
| Snapshot artifact verification returns 404 from `repo1.maven.org` or a timestamped POM URL | snapshots are stored under Central snapshot metadata, not release Maven Central POM paths | `https://central.sonatype.com/repository/maven-snapshots/.../maven-metadata.xml` 확인 |
| `bluetape4k-dependencies` CI rejects `-SNAPSHOT` managed artifacts after post-release reopen | release artifact verifier is running in strict release mode on a development snapshot line | develop/normal PR에는 `--allow-snapshots`를 사용하고 main-target release PR에는 strict mode 유지 |
| GitHub Release fallback notes | no `CHANGELOG.md` section for the tag | tag 전에 release section을 추가하거나 생성 후 release note를 편집 |
