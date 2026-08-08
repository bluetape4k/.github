# 2026-05-17 Central Portal release batch

## 맥락

Workspace는 Central Portal을 통해 bluetape4k library set을 Maven Central에
배포했습니다. `bluetape4k-projects 1.8.0`은 이미 배포된 상태였으므로 이번
batch는 나머지 publish 대상 저장소를 처리하고
`bluetape4k-dependencies 1.0.0`으로 마무리했습니다.

배포한 artifact:

- `bluetape4k-aws 0.1.0`
- `bluetape4k-text 0.1.0`
- `bluetape4k-graph 0.3.0`
- `bluetape4k-javers 0.1.0`
- `bluetape4k-exposed 1.8.0`
- `bluetape4k-leader 0.1.0`
- `bluetape4k-image 0.1.0`
- `bluetape4k-dependencies 1.0.0`

## 결정

- `gradle.properties`는 `baseVersion=<release>`, `snapshotVersion=`으로
  release 상태를 유지합니다. Snapshot publish는 파일을 편집하지 않고
  `-PsnapshotVersion=-SNAPSHOT`을 전달합니다.
- `bluetape4k-bom`, `bluetape4k-exposed-bom`처럼 저장소별 BOM version key를
  사용하고 모호한 공통 key `bluetape4k`는 피합니다.
- `experimental`, `workshop`, example, demo, benchmark는 release artifact에서
  일관되게 제외합니다.
- 모든 imported BOM이 Maven Central에서 HTTP 200으로 보인 뒤에만
  `bluetape4k-dependencies`를 마지막으로 publish합니다.
- Release-prep PR은 rebase merge를 사용하고 release workflow는 tag push로
  실행합니다.

## 발견한 문제

### 생성 POM의 dependency version 누락

`aws`, `exposed`, `leader`, `image`는 publish module에 Spring
dependency-management POM customization이 필요했습니다.
`generatedPomCustomization { setEnabled(false) }`로 비활성화하면 생성된
Maven POM의 dependency version이 비어 Central validation이 거부할 수
있습니다.

### SNAPSHOT dependency drift

`graph`가 여전히 `bluetape4k` SNAPSHOT version을 참조했습니다. Tag 전에
catalog와 생성 POM에서 `SNAPSHOT`을 검사해야 합니다.

### Release metadata에 포함된 비 library 모듈

Example, demo, benchmark는 다음에서 일관되게 제외해야 합니다.

- BOM constraint
- NMCP aggregation
- publication/signing 설정
- 생성되는 `bluetape4k-dependencies` catalog와 constraint

Aggregation만 필터링하면 모듈에 `maven-publish`가 남습니다. 중첩 example은
`:examples`와 `:examples:*`를 모두 만들 수 있으므로 두 형태를 제외해야
합니다.

### Central Portal 수락과 Maven Central 공개의 차이

GitHub Actions 성공은 Central Portal이 publish를 수락했다는 뜻입니다.
공개 consumer가 사용할 수 있는지는 `repo.maven.apache.org`에 별도로 HTTP
200을 요청해야 합니다. 일부 artifact는 전파에 몇 분이 걸렸습니다.

### Shell 변수 함정

zsh에서 `path`는 `PATH`와 연결됩니다. `for path in ...`로 polling loop를
작성하면 loop 내부의 `curl`과 `sleep`이 깨집니다. `artifact_path`를
사용합니다.

## 결과

대상 release workflow가 모두 성공했고 대표 Maven Central POM URL이 HTTP
200을 반환했습니다. 후속 PR에서 publish 저장소 전반의 BOM/NMCP filter와
`bluetape4k-dependencies` generation을 표준화했습니다.

## 검증 증거

- `leader 0.1.0`: release workflow 성공; `bluetape4k-leader-bom`과
  `bluetape4k-leader-core` POM이 HTTP 200.
- `image 0.1.0`: release workflow 성공; `bluetape4k-image-bom`과
  `bluetape4k-images` POM이 HTTP 200.
- `dependencies 1.0.0`: release workflow 성공;
  `bluetape4k-dependencies`와 `bluetape4k-version-catalog` POM이 HTTP 200.
- `dependencies` 전 imported BOM preflight에서 `projects`, `aws`, `image`,
  `text`, `graph`, `leader`, `exposed`, `javers`가 HTTP 200.

## 다음 실행

1. `.github/docs/release/pre-release-checklist.md`부터 시작합니다.
2. `.github/docs/release/central-portal-release-runbook.md`를 그대로 따릅니다.
3. Tag push 전에 생성 POM 검사를 실행합니다.
4. Central validation이 실패하면 PR에서 고치고 `develop`에 병합한 뒤
   `--force-with-lease`로 실패 version을 다시 tag합니다.
5. 모든 imported BOM이 Maven Central에 공개되기 전에는
   `bluetape4k-dependencies`를 release하지 않습니다.
