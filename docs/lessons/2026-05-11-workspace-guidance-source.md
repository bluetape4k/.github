# Workspace guidance에는 canonical 저장소 source가 필요하다

## 맥락

bluetape4k workspace 루트에는 `AGENTS.md`, `CLAUDE.md`, `WIP.md` 같은
guidance가 있지만 workspace 루트 자체는 Git 저장소가 아닙니다.

## 결정 또는 발견

canonical 사본을 조직 `.github` 저장소에서 관리하고 필요할 때 workspace
루트로 동기화합니다.

## 결과

`.github` 저장소가 `docs/workspace/` 아래에 workspace guidance를 저장하고,
drift 확인과 동기화를 위해 `scripts/sync_workspace_docs.py`를 제공합니다.

## 검증

- `python3 -m py_compile scripts/sync_workspace_docs.py`
- `python3 scripts/sync_workspace_docs.py --check`

## 다음 지침

workspace 루트 사본을 직접 고치지 말고 canonical 문서를 먼저 수정한 뒤
동기화합니다. `AGENTS.md`와 `CLAUDE.md`는 agent-facing 언어 계약을 유지합니다.
