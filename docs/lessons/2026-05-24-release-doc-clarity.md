# Release 문서의 명확성

## 맥락

2026년 5월 release train에서 release 준비, snapshot publish, release 후
reopen, 내부 bluetape4k version reference를 혼동해 여러 후속 편집이
필요했습니다.

## 결정

`Version Management Policy`를 canonical policy로 유지하고 release runbook은
필수 증거가 있는 실행 단계로 설명합니다. Checklist는 모든 SNAPSHOT
reference를 동일하게 잘못된 것으로 보지 말고 적용되는 branch phase를
명시해야 합니다.

## 결과

Release runbook은 flow map으로 시작하고 governance policy는
version/reference state table을 포함합니다. Pre-release checklist는 개발
snapshot reference와 release-prep non-snapshot reference를 구분합니다.

## 검증

- `git diff --check`

## 다음 guard

문서에서 version을 바꿀 때 현재 phase, artifact visibility, upstream HTTP 200
증거를 함께 기록합니다.
