# Workspace 문서

이 디렉터리는 단일 저장소 checkout에 속하지 않는 bluetape4k workspace 루트
guidance 파일의 canonical source입니다.

추적하는 source 파일:

- `AGENTS.md` - Codex workspace 계약
- `CLAUDE.md` - Claude workspace 계약
- `WIP.md` - 생태계 수준 작업 queue snapshot

활성 runtime 사본은 workspace 루트에 있습니다.

- `../AGENTS.md`
- `../CLAUDE.md`
- `../WIP.md`

`scripts/sync_workspace_docs.py --check`로 drift를 확인하고 `.github`
저장소에서 `scripts/sync_workspace_docs.py --sync`를 실행해 canonical
디렉터리에서 workspace 루트 사본을 갱신합니다.

`WIP.md`는 자주 바뀝니다. 매번의 로컬 queue scratch가 아니라 의미 있는
snapshot만 commit합니다.
