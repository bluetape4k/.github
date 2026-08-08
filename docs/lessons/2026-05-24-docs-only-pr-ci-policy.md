# 문서 전용 PR의 CI 정책

## 맥락

변경 내용이 Markdown 경로 수정뿐인데도 작은 문서 정리 PR이 repository build와
dependency submission check를 기다리고 있었습니다. 신뢰도를 높이지 못하면서
release train 비용만 늘었습니다.

## 결정

문서 전용 PR은 로컬 문서 게이트로 처리합니다.

- 일반 Markdown, lesson, spec, plan, governance 문서는 내용 검토와
  `git diff --check`면 충분합니다.
- 렌더링 문서, 생성 문서 또는 공개 웹사이트에 영향을 줄 때만 문서 빌드를
  실행합니다.
- GitHub `Automatic Dependency Submission`을 branch protection이 필수로
  지정하지 않는 한 고비용 CI를 기다리지 않습니다.

## 결과

Workspace guidance와 branch-protection governance에 이 정책을 기록해 불필요한
CI 대기 없이 향후 정리 PR을 병합할 수 있게 했습니다.

## 검증

문서 전용 PR에서 내용 검토, `git diff --check`, 영향이 있는 경우의 문서
build만 실행하는 경로를 확인했습니다.
