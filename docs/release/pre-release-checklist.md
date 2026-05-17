# bluetape4k-* 라이브러리 배포 전 사전 점검 체크리스트

배포 대상 레포지토리에서 순서대로 점검한다.
각 항목은 PASS / FAIL / N/A 로 표기하고, FAIL 은 해소 후 재점검.

---

## 1. 의존성 버전 점검

### 1-1. 내부 bluetape4k-* 의존성

```bash
# SNAPSHOT 참조 전수 확인
rg "SNAPSHOT" gradle/libs.versions.toml gradle.properties build.gradle.kts \
  --glob "!gradle.properties" | grep -v "snapshotVersion\|central-snapshot\|maven-snapshots\|# "
```

- [ ] `gradle/libs.versions.toml` 의 모든 `bluetape4k-*` 버전이 릴리즈 버전인가?
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
grep "baseVersion\|snapshotVersion" gradle.properties
```

- [ ] `baseVersion=X.Y.Z` — 배포할 버전이 맞는가?
- [ ] `snapshotVersion=` — 릴리즈 기본값은 비어 있는가?
- [ ] SNAPSHOT 배포는 파일 수정이 아니라 `-PsnapshotVersion=-SNAPSHOT` 파라미터로 수행하는가?

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

```
기준 순서:
bluetape4k-projects
  → aws/text/graph/javers
  → exposed/leader/image
  → bluetape4k-dependencies
```

- [ ] 이 레포가 참조하는 하위 레포가 **먼저** 배포되었는가?
- [ ] 각 하위 레포의 배포 버전이 Maven Central에서 resolve 가능한가?
- [ ] `bluetape4k-dependencies` 배포 전, imported BOM 전체가 Maven Central HTTP 200 인가?

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
- [ ] BOM/NMCP 집계에서 `examples/`, `*-examples`, `*-demo`,
      `benchmark/`, `*-benchmark` 모듈 제외 확인
- [ ] 소스 레포 다음 버전(`X.(Y+1).0-SNAPSHOT`) bump PR 생성

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
grep "baseVersion\|snapshotVersion" gradle.properties

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
| Nightly 1~2회 실패 후 무시 | 플레이크 or 실제 회귀 | 3회 연속 SUCCESS 기준 적용 |
| 배포 후 Maven Central에서 못 찾음 | 전파 지연 (최대 30분) | 10분 후 재확인 |
| KDoc 번역 누락 | 에이전트가 파일 목록 없이 디렉토리 단위로 번역 | `rg -l "[가-힣]"` 스캔 후 목록 명시 |
| Central validation에서 dependency version 누락 | Spring dependency-management POM customization 비활성화 | published module에서 `generatedPomCustomization { setEnabled(false) }` 제거 |
| `examples@버전` 이 Central validation 대상에 들어감 | `:examples:*`만 제외하고 `:examples` parent project를 놓침 | `path == ":examples"` 와 `path.startsWith(":examples:")` 둘 다 제외 |
| BOM에 benchmark alias가 들어감 | examples만 제외하고 benchmark 필터 누락 | `benchmark/`, `*-benchmark`까지 제외하고 dependencies generator 재실행 |
| polling 중 `curl`/`sleep` 명령을 못 찾음 | zsh 루프 변수 `path`가 `PATH`를 덮어씀 | 변수명을 `artifact_path`로 사용 |
