# Workspace guidance PR triage

## 맥락

로컬 `.github` worktree에는 2026-05-18 audit snapshot을 담은 오래된 WIP
브랜치와 이후의 미커밋 workspace guidance 변경이 함께 있었습니다.

## 결정 또는 발견

release train이 생태계 상태를 크게 바꾼 뒤에는 오래된 `WIP.md` snapshot을
병합하지 않습니다. 현재 `main`에서 새 PR을 만들어 지속적인 workspace
guidance 변경만 옮기고 오래된 WIP PR은 닫습니다.

## 결과

workspace guidance sync를 이전 WIP snapshot에서 분리해 canonical
`docs/workspace/AGENTS.md`와 `docs/workspace/CLAUDE.md`를 오래된 queue 상태
없이 검토할 수 있게 했습니다.

## 검증

- 열린 WIP PR을 `origin/main`과 비교했습니다.
- 추적되지 않은 `.omc/state/last-tool-error.json`이 저장소 내용이 아니라
  로컬 도구 오류 cache임을 확인했습니다.

## 다음 지침

WIP snapshot과 지속적인 guidance 변경을 하나의 PR에 섞지 않습니다.
