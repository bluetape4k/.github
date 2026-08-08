# Catalog와 BOM version을 분리한다

## 맥락

2026-05-23 release train에서 cycle과 불필요한 artifact가 드러났습니다.
Downstream `bluetape4k-*` 저장소는 최종 `bluetape4k-dependencies` BOM이
존재하기 전에 공유 Gradle catalog가 필요했습니다. 이 catalog는 사용자용
dependency 계약이 아니라 내부 build input이므로 Maven Central에 별도
artifact로 publish할 필요가 없습니다.

## 결정

배포 경로를 분리합니다.

- `bluetape4k-dependencies`는 최종 consumer BOM에 semantic version을 사용합니다.
- `bluetape4k-dependencies/gradle/libs.versions.toml`은 내부
  build/contributor catalog source이며 `catalog/2026-05-23-00` 같은 git ref로
  고정합니다.
- Downstream library 저장소는 `bluetape4kDependenciesCatalogPath` 또는
  `BLUETAPE4K_DEPENDENCIES_CATALOG_PATH`로 checkout한 catalog 파일을 읽습니다.

## 결과

Release runbook과 pre-release checklist에 분리 규칙을 기록했습니다.
`bluetape4k-dependencies` build는 BOM만 publish하고 내부 catalog 소비는
checkout한 `bluetape4k-dependencies` ref에서 수행합니다.

## 검증

`projects`, `aws`, `text`, `graph`, `javers`, `exposed`, `leader`, `image`의
설정이 로컬 `bluetape4k-dependencies/gradle/libs.versions.toml` 경로에서
공유 catalog를 읽는지 확인했습니다.

## 다음 규칙

Gradle catalog import에 `bluetape4kDependenciesVersion`을 사용하지 않습니다.
실제 `io.github.bluetape4k:bluetape4k-dependencies` platform import에만
사용합니다. 별도의 사용자 목적이 없는 한 내부 build catalog를 Maven
Central artifact로 publish하지 않습니다.
