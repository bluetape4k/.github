# bluetape4k-* 라이브러리 배포 전 사전 점검 체크리스트

배포 대상 레포지토리에서 순서대로 점검한다.
각 항목은 PASS / FAIL / N/A 로 표기하고, FAIL 은 해소 후 재점검.

이 체크리스트는 release-prep branch에서 사용한다. 일반 `develop`에서는 내부
`bluetape4k-*` 참조가 `-SNAPSHOT`인 것이 정상이고, release-prep에서만
upstream release가 Maven Central HTTP 200으로 확인된 뒤 suffix를 제거한다.

---

## 1. 의존성 버전 점검

Canonical policy:
`docs/governance/version-and-release-train.md`의
`Version Management Policy`를 기준으로 삼는다.

### 1-0. BOM / catalog 역할 분리

`bluetape4k-dependencies` repo는 사용자용 BOM과 내부 빌드 catalog의
source를 함께 가진다. 배포 방식은 분리한다.

- `bluetape4k-dependencies`: 최종 사용자용 Maven BOM. semantic version을
  사용한다. 예: `1.1.3`
- `bluetape4k-dependencies/gradle/libs.versions.toml`: bluetape4k repo
  빌드/기여자용 Gradle catalog source. `bluetape4k-*` repo들이 사용하는
  외부 라이브러리와 Gradle plugin 버전을 통일하기 위해 사용한다.
  Maven Central에 별도 catalog artifact로 publish하지 말고,
  `catalog/YYYY-MM-DD-NN` 같은 `bluetape4k-dependencies` git ref로 고정한다.

```bash
grep -E '^(baseVersion|snapshotVersion|bluetape4kDependenciesCatalogPath|bluetape4kDependenciesCatalogRef|bluetape4kDependenciesVersion)=' gradle.properties || true
rg -n 'bluetape4kDependenciesCatalog(Path|Ref)|BLUETAPE4K_DEPENDENCIES_CATALOG_(PATH|REF)|bluetape4kDependenciesVersion|bluetape4k-version-catalog|bluetape4k-dependencies' settings.gradle.kts build.gradle.kts gradle.properties gradle/libs.versions.toml
```

- [ ] `bluetape4k-*` 라이브러리 repo가 shared catalog를 import한다면
      `bluetape4k-dependencies/gradle/libs.versions.toml`을 checkout된 git ref
      경로에서 읽을 수 있는가? 일반 PR CI fallback은 허용하지만 release
      validation은 명시 path/env 또는 `bluetape4kDependenciesCatalogRef`를
      사용해야 한다.
- [ ] `bluetape4kDependenciesVersion`은 실제 BOM/platform import에만
      사용되고, Gradle catalog import에는 사용되지 않는가?
- [ ] release train catalog source ref(`catalog/YYYY-MM-DD-NN`)가 존재하고
      downstream CI/local build가 그 ref를 checkout하도록 되어 있는가?
- [ ] catalog source ref를 내부 `bluetape4k-*` 의존 release version source로
      사용하지 않는가? 내부 bluetape4k 참조는 개발 중에는 matching
      `-SNAPSHOT`을 사용하고, release prep에서만 배포 순서에 따라 신규
      배포된 release version으로 suffix를 제거한다.
- [ ] 같은 release train 안의 repo가 아직 배포되지 않은 최종
      `bluetape4k-dependencies` BOM 버전에 의존하지 않는가?

### 1-1. 내부 bluetape4k-* 의존성

```bash
rg -n 'bluetape4k(-[a-z]+)? = "|bluetape4k-.*-bom = "|io\.github\.bluetape4k' \
  gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts

rg -n 'exposed|bluetape4k-exposed|io\.github\.bluetape4k\.exposed|bluetape4k\.exposed' \
  settings.gradle.kts gradle/libs.versions.toml build.gradle.kts **/build.gradle.kts

# release prep에서 제거해야 할 내부 SNAPSHOT 참조 전수 확인
rg "SNAPSHOT" gradle/libs.versions.toml gradle.properties build.gradle.kts \
  --glob "!gradle.properties" | grep -v "snapshotVersion\|central-snapshot\|maven-snapshots\|# "
```

- [ ] 참조하는 내부 `bluetape4k-*` repo가 이번 release train 대상이면,
      개발 branch에서는 matching `-SNAPSHOT`을 참조하고 있는가?
- [ ] release prep branch에서는 그 upstream repo의 목표 버전이 배포되어
      Maven Central HTTP 200이 된 뒤에만 `-SNAPSHOT` suffix를 제거했는가?
- [ ] `javers-exposed` 같은 신규 bridge module이 추가되어 release order가
      바뀌지 않았는가? 특히 `bluetape4k-javers`가
      `bluetape4k-exposed`를 참조하면 `exposed` 목표 버전 배포 후에만
      `javers`를 준비/배포해야 한다.
- [ ] 참조하는 내부 `bluetape4k-*` repo가 이번 release train 대상이
      아니라면, `gradle/libs.versions.toml`의 버전이 Maven Central에 공개된
      가장 최신 upstream release version인가?
- [ ] `io.github.bluetape4k` 와 `io.github.bluetape4k.exposed` 등 **groupId가 다른 아티팩트**는 별도 version key를 사용하는가?
- [ ] 해당 버전이 **Maven Central에 실제로 존재**하는가?
  ```bash
  # 예시: exposed-jdbc-tests 1.8.0 존재 확인
  curl -o /dev/null -s -w "%{http_code}" \
    "https://repo1.maven.org/maven2/io/github/bluetape4k/exposed/exposed-jdbc-tests/1.8.0/exposed-jdbc-tests-1.8.0.pom"
  # 200 이어야 함
  ```

> ⚠️ **함정**: groupId가 다른 아티팩트는 릴리즈 사이클이 다르다.  
> `bluetape4k-exposed` (`io.github.bluetape4k.exposed`) 는 `bluetape4k-projects` (`io.github.bluetape4k`) 와 별도로 배포된다.  
> 버전 번호가 같더라도 각각 Maven Central에 독립적으로 존재해야 한다.

### 1-2. 외부 의존성

- [ ] 외부 라이브러리 SNAPSHOT 참조 없음 (`-SNAPSHOT`, `.BUILD-SNAPSHOT` 등)
- [ ] `exposed`, `spring-boot`, `kotlin`, `kotlinx-coroutines` 등 주요 의존성이 GA 버전인가?

---

## 2. 코드 품질

### 2-0a. 브랜치 라인 정책

- [ ] `develop`의 `baseVersion`이 현재 active release line과 일치하는가?
- [ ] 배포 직후 `develop`의 `baseVersion`은 다음 release version으로
      올라가 있고, `snapshotVersion=`은 비어 있는가?
- [ ] snapshot publish는 workflow에서 `-PsnapshotVersion=-SNAPSHOT`으로만
      주입하고, release publish는 `baseVersion`만 사용하는가?
- [ ] open patch milestone이 남아 있는데 `develop`을 다음 minor로 올리지
      않았는가? 단, patch milestone을 명시적으로 close/defer했다면 예외.
- [ ] `develop`이 이미 다음 minor로 진행된 뒤 이전 minor patch가 필요하면,
      마지막 release tag에서 `release/X.Y.x` maintenance branch를 만들고
      거기서 patch version을 올리는가?
- [ ] maintenance branch fix는 bug/security/compatibility fix로 제한하고,
      같은 fix를 `develop`으로 forward-port할 계획이 있는가?
- [ ] 다음 minor feature/API 작업을 maintenance branch로 backport하지 않는가?

### 2-0. 버전별 milestone

```bash
gh api "repos/bluetape4k/$(basename "$PWD")/milestones?state=open&per_page=100" \
  --jq '.[] | [.title,.open_issues,.closed_issues] | @tsv'
gh issue list --state open --milestone "<target-version>" --limit 100
gh pr list --state open --search "milestone:<target-version>"
```

- [ ] 배포 대상 버전과 정확히 같은 GitHub milestone이 존재하는가?
- [ ] 대상 milestone의 open issue가 0이거나, 이번 배포에 포함할 항목으로
      명시되어 있는가?
- [ ] 대상 milestone의 issue를 close하는 open PR이 남아있지 않은가?
- [ ] backlog/다음 minor milestone의 feature issue가 이번 patch 배포에
      묵시적으로 섞이지 않았는가?

### 2-1. 오픈 이슈

```bash
# 버그 레이블 오픈 이슈 확인
gh issue list --state open --label "bug" --limit 20
```

- [ ] **bug** 레이블 오픈 이슈 = 0  
  (있으면: 수정 후 배포 vs 1.x.y+1으로 defer 결정)
- [ ] **blocker** / **critical** 레이블 오픈 이슈 = 0

### 2-2. 오픈 PR

```bash
gh pr list --state open
```

- [ ] 오픈 PR이 없거나, 배포와 무관한 PR만 남아있음
- [ ] 배포 관련 fix/chore PR은 머지 완료

### 2-3. KDoc / 문서

- [ ] 신규 또는 변경된 공개 API에 English KDoc 작성 완료
- [ ] `README.md` 및 로케일 README(`README.ko.md` 등) 업데이트 완료

---

## 3. CHANGELOG 점검

```bash
head -30 CHANGELOG.md
```

- [ ] `## [X.Y.Z] — Unreleased` → `## [X.Y.Z] — YYYY-MM-DD` 날짜 스탬프 완료
- [ ] `## [Unreleased]` 섹션이 비어있거나 다음 버전 항목으로 분리되어 있음
- [ ] 이번 배포에 포함된 주요 변경사항이 기록되어 있음 (Added / Changed / Fixed / Removed)

---

## 4. CI / 테스트

### 4-1. Nightly CI

```bash
gh run list --workflow="Nightly" --limit 5
```

- [ ] 최근 Nightly **3회 연속 SUCCESS**
- [ ] 마지막 Nightly가 **48시간 이내** 실행됨

### 4-2. develop 브랜치 상태

```bash
git log --oneline origin/develop..HEAD   # 로컬이 ahead면 push 필요
git status --porcelain                    # 미커밋 변경 없음
```

- [ ] `develop` 브랜치 = origin/develop (로컬 ahead/behind 0)
- [ ] 미커밋 변경 없음
- [ ] 워크트리 잔존 없음: `git worktree list`

---

## 5. 버전 파일 점검

```bash
grep -E "baseVersion|snapshotVersion|bluetape4kDependenciesCatalogPath|bluetape4kDependenciesCatalogRef|bluetape4kDependenciesVersion" gradle.properties || true
```

- [ ] `baseVersion=X.Y.Z` — 배포할 버전이 맞는가?
- [ ] `snapshotVersion=` — 릴리즈 기본값은 비어 있는가?
- [ ] SNAPSHOT 배포는 파일 수정이 아니라 `-PsnapshotVersion=-SNAPSHOT` 파라미터로 수행하는가?
- [ ] downstream `bluetape4k-*` repo의 shared catalog import는
      `bluetape4kDependenciesCatalogPath`, `BLUETAPE4K_DEPENDENCIES_CATALOG_PATH`,
      `bluetape4kDependenciesCatalogRef`, 또는
      `BLUETAPE4K_DEPENDENCIES_CATALOG_REF`로 관리되는가?

---

## 6. 배포 워크플로우 점검

```bash
# release.yml 트리거 조건 확인
grep -A5 "on:" .github/workflows/release.yml | head -15
```

- [ ] `release.yml` 이 존재하고 태그 패턴(`[0-9]+.[0-9]+.[0-9]+`)에 트리거됨
- [ ] `Publish Snapshot` 워크플로우와 `Publish Release` 워크플로우가 분리되어 있음
- [ ] NMCP / Maven Central Portal 자격증명 시크릿이 설정되어 있음 (이전 배포 성공 이력으로 확인)

---

## 7. 배포 의존 순서 확인

복수 레포지토리가 서로 의존할 경우 **의존성 그래프 순서**대로 배포해야 한다.
아래 순서는 기본값일 뿐이며, 매 release train마다 실제 build/settings/catalog
파일을 스캔해 다시 확정한다.

```
기준 순서:
bluetape4k-projects
  → exposed/text/graph/javers
  → aws/leader
  → image
  → bluetape4k-dependencies
```

- [ ] 이 레포가 참조하는 하위 레포가 **먼저** 배포되었는가?
- [ ] 각 하위 레포의 배포 버전이 Maven Central에서 resolve 가능한가?
- [ ] `bluetape4k-dependencies` 배포 전, imported BOM 전체가 Maven Central HTTP 200 인가?
- [ ] release train 중간에 downstream build alias 또는 upstream BOM 버전이
      필요하면 `bluetape4k-dependencies`의 새 `catalog/YYYY-MM-DD-NN` ref를
      만들고 downstream repo CI/local build가 그 ref를 checkout하도록
      갱신했는가?
- [ ] 최종 `bluetape4k-dependencies` BOM은 모든 하위 repo 배포 이후에만
      publish하는가?

> ⚠️ **함정**: 버전 번호가 우연히 같아도 groupId가 다르면 별도로 배포해야 한다.

---

## 8. 배포 후 점검 (post-release)

배포 완료 후 즉시 확인:

```bash
# GitHub Release 생성 확인
gh release view X.Y.Z

# Maven Central 등재 확인 (전파에 수 분~수십 분 소요)
curl -s "https://repo1.maven.org/maven2/io/github/bluetape4k/<artifact>/X.Y.Z/<artifact>-X.Y.Z.pom" \
  -o /dev/null -w "%{http_code}"
```

- [ ] GitHub Release 태그 `X.Y.Z` 생성됨
- [ ] Maven Central에서 주요 아티팩트 HTTP 200 확인
- [ ] 릴리즈 노트 한영 이중 작성 완료
- [ ] `bluetape4k-dependencies` 버전 카탈로그 업데이트 PR 생성
- [ ] workshop/application repo는 `bluetape4k-dependencies`만 버전 source로
      사용하고, `io.github.bluetape4k*` artifact는 versionless로 선언됨
- [ ] BOM/NMCP 집계에서 `examples/`, `*-examples`, `*-demo`,
      `benchmark/`, `*-benchmark` 모듈 제외 확인
- [ ] `bluetape4k.github.io` 공개 문서 최신화 PR 생성 및 머지
- [ ] 소스 레포 post-release reopen PR 생성:
      `baseVersion`은 다음 release version으로 올리고, `snapshotVersion=`은
      비워 둔다.
- [ ] post-release reopen PR에서 개발 중 필요한 내부 `bluetape4k-*` 참조는
      matching upstream `-SNAPSHOT`으로 되돌렸다.

### 8-1. Central Portal 전파 확인

GitHub Actions `release.yml` 성공은 Central Portal 접수 완료를 뜻한다.
소비자 resolve 가능 여부는 Maven Central 공개 repo의 HTTP 200으로 따로 확인한다.

```bash
for i in $(seq 1 30); do
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://repo.maven.apache.org/maven2/<group-path>/<artifact>/<version>/<artifact>-<version>.pom")
  echo "$code <artifact>"
  [ "$code" = "200" ] && break
  sleep 20
done
```

주의: zsh에서 루프 변수명을 `path`로 쓰지 말 것. `PATH`를 덮어써서
`curl`, `sleep` 같은 명령을 찾지 못할 수 있다.

### 8-2. 공개 사이트 문서 최신화

최종 BOM과 `bluetape4k-dependencies`가 Maven Central에서 HTTP 200을 반환하면
`bluetape4k.github.io` 문서를 같은 배포 작업 안에서 갱신한다.

- [ ] quick start 예제의 `bluetape4k-dependencies` / `bluetape4k-bom`
      버전이 최신인가?
- [ ] Version Governance 표의 repository-specific BOM 버전이 최신인가?
- [ ] Repository 목록의 latest release 문구가 최신인가?
- [ ] English/Korean 문서를 함께 갱신했는가?
- [ ] `npm run build` 성공
- [ ] `Deploy Website` GitHub Actions 성공
- [ ] 라이브 페이지에서 최신 버전 확인:
  `https://bluetape4k.github.io/ecosystem/version-governance/`

---

## 빠른 점검 스크립트

```bash
#!/usr/bin/env bash
# 배포 전 빠른 상태 확인 (pass/fail 판정은 수동)

echo "=== 1. SNAPSHOT 의존성 ==="
rg "SNAPSHOT" gradle/libs.versions.toml 2>/dev/null | grep -v "snapshotVersion\|central-snapshot\|maven-snapshots\|# "

echo "=== 2. 오픈 버그 이슈 ==="
gh issue list --state open --label "bug" --limit 10 2>/dev/null

echo "=== 3. 오픈 PR ==="
gh pr list --state open 2>/dev/null

echo "=== 4. CHANGELOG 상태 ==="
head -15 CHANGELOG.md

echo "=== 5. Nightly CI (최근 3회) ==="
gh run list --workflow="Nightly" --limit 3 2>/dev/null

echo "=== 6. gradle.properties ==="
grep -E "baseVersion|snapshotVersion|bluetape4kDependenciesCatalogPath|bluetape4kDependenciesCatalogRef|bluetape4kDependenciesVersion" gradle.properties || true

echo "=== 6b. BOM/catalog role split ==="
rg -n "bluetape4kDependenciesCatalog(Path|Ref)|BLUETAPE4K_DEPENDENCIES_CATALOG_(PATH|REF)|bluetape4kDependenciesVersion|bluetape4k-version-catalog|bluetape4k-dependencies" \
  settings.gradle.kts build.gradle.kts gradle.properties gradle/libs.versions.toml 2>/dev/null || true

echo "=== 7. release metadata exclusions ==="
rg -n "SNAPSHOT|examples|demo|benchmark" build/publications gradle/libs.versions.toml build.gradle.kts 2>/dev/null || true

echo "=== 8. develop 상태 ==="
git log --oneline origin/develop..HEAD
git status --porcelain
git worktree list
```

---

## 공통 함정 모음

| 증상 | 원인 | 해결 |
|------|------|------|
| `./gradlew build` 성공인데 배포 후 resolve 실패 | SNAPSHOT 의존성이 Maven Central에 없음 | 의존 레포 먼저 배포 |
| groupId 달라도 버전 같으면 괜찮다고 가정 | 릴리즈 사이클이 별도임 | Maven Central HTTP 200 직접 확인 |
| `release.yml` 트리거 안 됨 | `snapshotVersion` 비우지 않음 or tag 형식 불일치 | `baseVersion` = tag, `snapshotVersion=` 확인 |
| 배포 후 개발 시작 시 어떤 버전으로 열지 헷갈림 | own artifact version과 dependency reference version을 섞음 | own `baseVersion`은 다음 release, `snapshotVersion=`은 empty, 내부 refs는 matching `-SNAPSHOT` |
| Nightly 1~2회 실패 후 무시 | 플레이크 or 실제 회귀 | 3회 연속 SUCCESS 기준 적용 |
| 배포 후 Maven Central에서 못 찾음 | 전파 지연 (최대 30분) | 10분 후 재확인 |
| KDoc 번역 누락 | 에이전트가 파일 목록 없이 디렉토리 단위로 번역 | `rg -l "[가-힣]"` 스캔 후 목록 명시 |
| Central validation에서 dependency version 누락 | Spring dependency-management POM customization 비활성화 | published module에서 `generatedPomCustomization { setEnabled(false) }` 제거 |
| `examples@버전` 이 Central validation 대상에 들어감 | `:examples:*`만 제외하고 `:examples` parent project를 놓침 | `path == ":examples"` 와 `path.startsWith(":examples:")` 둘 다 제외 |
| BOM에 benchmark alias가 들어감 | examples만 제외하고 benchmark 필터 누락 | `benchmark/`, `*-benchmark`까지 제외하고 dependencies generator 재실행 |
| polling 중 `curl`/`sleep` 명령을 못 찾음 | zsh 루프 변수 `path`가 `PATH`를 덮어씀 | 변수명을 `artifact_path`로 사용 |
