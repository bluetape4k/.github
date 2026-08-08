# Website release 문서 갱신

## 맥락

2026-05-23 release train에서 `bluetape4k-dependencies`와 library BOM version을
갱신한 뒤, 공개 setup 예제와 version governance 페이지가 Maven Central과
일치하도록 `bluetape4k.github.io`를 별도로 갱신해야 했습니다.

## 결정 또는 발견

최종 BOM이 Maven Central에 보이면 Central Portal release runbook에 website
문서 갱신을 필수 단계로 포함해야 합니다. 공개 website에 현재 coordinate가
표시되기 전에는 release가 운영상 완료된 것이 아닙니다.

## 결과

공유 release runbook에 갱신할 website 페이지, 로컬 website build 검사,
GitHub Pages/live-page 증거를 기록했습니다. Pre-release checklist도 이를
release 후 점검 항목으로 취급합니다.

2026-05-23 release train에서 `bluetape4k.github.io` PR #11은
`bluetape4k-dependencies 1.1.3`이 Maven Central에서 HTTP 200을 반환한 뒤
공개 coordinate를 갱신했습니다. GitHub Pages deployment run `26337058162`가
성공했고 live version governance 페이지에 다음 version이 표시되었습니다.

- `bluetape4k-dependencies` `1.1.3`
- `bluetape4k-bom` `1.9.1`
- `bluetape4k-exposed-bom` `1.9.1`
- `bluetape4k-aws-bom` `0.2.1`
- `bluetape4k-graph-bom` `0.4.1`
- `bluetape4k-leader-bom` `0.2.1`
- `bluetape4k-image-bom` `0.1.2`
- `bluetape4k-javers-bom` `0.1.2`
- `bluetape4k-text-bom` `0.1.2`

## 검증

- `docs/release/central-portal-release-runbook.md` 갱신
- `docs/release/pre-release-checklist.md` 갱신
- 이 저장소에서 Markdown과 diff 검사 실행
- `bluetape4k.github.io`에서 `npm run build`와 `git diff --check` 실행
- Pages deployment 뒤 live `https://bluetape4k.github.io/ecosystem/version-governance/`
  페이지 확인

## 다음 지침

매 release train마다 `bluetape4k-dependencies`가 publish되고 imported BOM이
Maven Central에서 HTTP 200을 반환한 직후 `bluetape4k.github.io`를 갱신합니다.
완료를 보고하기 전에 `npm run build`, Pages deployment run, live version
governance 페이지를 확인합니다.
