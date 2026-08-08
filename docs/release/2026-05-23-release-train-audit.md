# 2026-05-23 Release train 감사

## 범위

`bluetape4k-projects 1.9.1` 이후 release train을 publish하기 전의 release
candidate 감사입니다.

## 현재 게이트

아래 milestone과 version blocker를 해결하기 전에는 release artifact를
publish하지 않습니다.

## Milestone 게이트

대상 release version마다 release PR/tag를 준비하기 전에 일치하는 GitHub
milestone이 있어야 합니다. Milestone 검사는 version별로 수행하며 이전 patch,
backlog 또는 다음 minor milestone으로 준비 상태를 추정하지 않습니다.

각 대상 milestone에 다음을 기록합니다.

- milestone 존재 여부
- 해당 milestone에 할당된 open Issue
- 해당 milestone Issue를 닫는 open PR
- 각 open 항목을 이번 release에 포함하는지, 명시적으로 연기하는지 여부

## 저장소 상태

| 저장소 | 대상 | 현재 local `baseVersion` | GitHub milestone 상태 | 게이트 |
|---|---:|---:|---|---|
| `bluetape4k-projects` | `1.9.1` | `1.9.1` | 존재, open: #620 | downstream handoff 완료 전 보류 |
| `bluetape4k-aws` | `0.2.1` | `0.2.1` | 존재, open: 0 | `bluetape4k-exposed 1.9.1` 대기 후 exposed reference 갱신 |
| `bluetape4k-text` | `0.1.2` | `0.1.2` | 존재, open: 0 | 검증 준비 완료 |
| `bluetape4k-graph` | `0.4.1` | `0.4.1` | 존재, open: 0 | 검증 준비 완료; 최종 dependencies BOM import 제거 |
| `bluetape4k-javers` | `0.1.2` | `0.1.2` | 존재, open: 0 | 검증 준비 완료 |
| `bluetape4k-exposed` | `1.9.1` | `1.9.1` | 존재, open: 0 | 검증 준비 완료 |
| `bluetape4k-leader` | `0.2.1` | `0.2.1` | 존재, open: #270 | #270 PR 해결; test helper reference를 올리면 `bluetape4k-exposed 1.9.1` 대기 |
| `bluetape4k-image` | `0.1.2` | `0.1.2` | 존재, open: 0 | `bluetape4k-aws 0.2.1` 대기 후 aws reference 갱신 |
| `bluetape4k-dependencies` | `1.1.3` | `1.1.2` | 존재, open: 0 | 최종 BOM 단계까지 `1.1.2` 유지 후 `1.1.3`으로 갱신 |

## 대상 milestone의 open 항목

- `bluetape4k-projects 1.9.1`: #620 `chore: coordinate downstream BOM/catalog handoff after projects 1.9.1`
- `bluetape4k-leader 0.2.1`: #270 `feat: promote StringTruncateSupport to bluetape4k-support after v1 stabilizes`

## 대상이 아니므로 연기하거나 범위를 다시 정할 항목

- `bluetape4k-javers 0.2.0`: #3, #4, #5는 feature 작업이며 release 범위를
  바꾸지 않는 한 제안한 `0.1.2` patch release에 포함하지 않습니다.
- `bluetape4k-exposed backlog`: #24, #30, #31, #32는 CockroachDB feature
  작업이므로 범위를 다시 정하지 않는 한 `1.9.1` patch release에 포함하지
  않습니다.
- `bluetape4k-image Backlog`: #1, #2, #3, #4는 새 feature 작업이므로
  `0.1.2` patch release에 포함하지 않습니다.
- `bluetape4k-graph backlog`: #30은 Neptune research/epic 작업이므로
  `0.4.1` patch release에 포함하지 않습니다.

## 내부 reference 사전 점검

내부 `bluetape4k-*` reference는 release 순서를 따라야 합니다. 참조 저장소가
이번 train에 포함되면 upstream target version이 release되고 Maven Central에서
HTTP 200이 확인될 때까지 downstream은 기다립니다. 이전 공개 release로
대체하지 않습니다. 공유 catalog source ref는 외부 library/plugin version 정렬에만
사용합니다.

현재 Maven Central 검사:

| Reference | Version | HTTP | 비고 |
|---|---:|---:|---|
| `io.github.bluetape4k:bluetape4k-bom` | `1.9.1` | `200` | Downstream용 upstream 공개 완료 |
| `io.github.bluetape4k.exposed:bluetape4k-exposed-bom` | `1.9.0` | `200` | 기존 exposed release. 같은 train에서 `1.9.1`이 필요하면 해당 HTTP 200까지 대기 |
| `io.github.bluetape4k.aws:bluetape4k-aws-bom` | `0.2.0` | `200` | 기존 aws release. image가 새 train version을 쓰면 aws `0.2.1` HTTP 200까지 대기 |
| `io.github.bluetape4k:bluetape4k-dependencies` | `1.1.1` | `200` | 기존 최종 BOM. 이번 train을 단축하는 데 사용하지 않음 |

현재 release worktree의 reference 상태:

| 저장소 | 확인한 내부 reference | 게이트 |
|---|---|---|
| `bluetape4k-aws` | `bluetape4k-bom 1.9.1`, `bluetape4k-exposed-bom 1.9.0` | WAIT: `aws-exposed`가 exposed를 사용하므로 exposed `1.9.1` release 후 aws 갱신 |
| `bluetape4k-text` | `bluetape4k-bom 1.9.1` | PASS |
| `bluetape4k-graph` | `bluetape4k-bom 1.9.1` | PASS; 최종 `bluetape4k-dependencies` BOM import 제거 |
| `bluetape4k-javers` | `bluetape4k-bom 1.9.1`, 현재 exposed build/catalog reference 없음 | PASS. 향후 `javers-exposed` 작업은 javers를 exposed 뒤로 이동 |
| `bluetape4k-exposed` | `bluetape4k-bom 1.9.1` | PASS |
| `bluetape4k-leader` | `bluetape4k-bom 1.9.1`, `bluetape4k-exposed 1.9.0` test helper | WAIT: exposed test helper를 train에 맞추면 대기, 아니면 #270 검증 진행 |
| `bluetape4k-image` | `bluetape4k-bom 1.9.1`, `bluetape4k-aws-bom 0.2.0` | WAIT: aws `0.2.1` release와 HTTP 200 확인 후 image 갱신 |

## 필수 순서

1. 각 대상 milestone의 release 범위 Issue를 해결합니다.
2. 없는 target milestone은 release-prep Issue를 열거나 이동하기 전에 만듭니다.
   이번 train에서는 완료했습니다.
3. Release PR 전에 각 저장소 `baseVersion`을 target version으로 올립니다.
   Library 저장소는 완료했고 `bluetape4k-dependencies 1.1.3`은 최종 BOM
   단계까지 연기합니다.
4. `bluetape4k-dependencies` catalog source ref는 외부 library/plugin 정렬에만
   사용하고 checkout한 `gradle/libs.versions.toml`로 소비합니다.
5. 내부 `bluetape4k-*` dependency에는 새로 공개된 upstream release version을
   명시하며 catalog source ref를 version source로 쓰지 않습니다.
6. 다음 dependency 순서로 library를 release합니다.
   `projects 1.9.1` -> `exposed 1.9.1`, `text 0.1.2`, `graph 0.4.1`,
   `javers 0.1.2` -> `aws 0.2.1`, `leader 0.2.1` -> `image 0.1.2` ->
   `dependencies 1.1.3`
7. 모든 imported BOM이 Maven Central에서 HTTP 200을 반환한 뒤
   `bluetape4k-dependencies 1.1.3`을 마지막으로 release합니다.

위 순서는 감사한 2026-05-23 worktree에만 유효합니다. 다음 train마다
dependency를 다시 검사합니다. 예정된 `javers-exposed` 작업이 시작되면
`bluetape4k-javers`가 `bluetape4k-exposed`에 의존하므로 exposed target release와
Maven Central HTTP 200까지 javers를 대기시켜야 합니다.

## 즉시 blocker

`bluetape4k-leader` Issue #270은 `0.2.1` release 전에 완료해야 합니다.
Local `leader-core` UTF-8 truncation helper를
`bluetape4k-projects 1.9.1`의 `io.bluetape4k.support.truncateUtf8`로 교체합니다.

## Catalog source 정정

내부 Gradle catalog를 Maven Central artifact로 publish하지 않습니다. 이는
`bluetape4k-*` 저장소의 build input이므로 release train은
`bluetape4k-dependencies/gradle/libs.versions.toml`을
`bluetape4k-dependencies` git ref로 고정하고 checkout한 파일 경로를 downstream
build에 전달합니다.

2026-05-23 검증:

- `bluetape4k-dependencies` NMCP zip generation은
  `io/github/bluetape4k/bluetape4k-dependencies/1.1.2/*`만 포함하고
  version-catalog publication은 생성하지 않습니다.
- `projects`, `aws`, `text`, `graph`, `javers`, `exposed`, `leader`, `image`가
  `-Pbluetape4kDependenciesCatalogPath=<dependencies-worktree>/gradle/libs.versions.toml`
  로 `./gradlew help`를 통과했습니다.
- Local downloaded TOML cache를 지운 뒤 `aws`, `text`, `leader`도 path override
  없이 `./gradlew help`를 통과했으며 Gradle이
  `bluetape4k-dependencies` git ref fallback에서 catalog를 resolve했습니다.
