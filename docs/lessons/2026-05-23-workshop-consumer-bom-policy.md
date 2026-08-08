# Workshop consumer BOM 정책

## 맥락

2026년 5월 release-upgrade 작업에서 workshop과 application 저장소가
`bluetape4k-dependencies`를 import하면서 개별 bluetape4k artifact도 pin하면
drift가 발생할 수 있음을 확인했습니다.

## 결정

Workspace 거버넌스는 workshop, example, application 저장소를 consumer로
취급합니다. 이 저장소는 `bluetape4k-dependencies`를 유일한 bluetape4k
version source로 유지하고 version 없이 `io.github.bluetape4k*` artifact를
선언해야 합니다.

## 결과

정책을 dependency governance, release-train governance, release checklist에
추가해 향후 release-upgrade PR이 같은 규칙을 확인하도록 했습니다.

## 검증

문서 전용 변경이며 `git diff --check`를 통과했습니다.

## 다음 지침

consumer 저장소를 업그레이드할 때 직접 bluetape4k version reference를
grep하고 BOM version 하나만 남아 있는지 확인합니다.
