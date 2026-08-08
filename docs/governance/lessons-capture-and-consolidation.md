# Lesson 수집과 통합

## 목적

Lesson은 bluetape4k 조직의 지속 가능한 운영 지식입니다. 무엇이 바뀌었는지,
무엇이 실패했는지, 어떤 증거로 해결했는지, 다음 작업이 무엇을 다르게 해야
하는지를 기록합니다.

Runtime note, 대화 요약, `.omx` 상태는 일시적입니다. 안정적이고 재사용할 수
있는 발견만 저장소 문서로 승격합니다.

## 저장소 계약

활성 bluetape4k 저장소는 추적되는 `docs/lessons/` 디렉터리를 유지해야
합니다. lesson을 관리하지 않는 저장소는 중앙 inventory에 이유를 적고
활성화될 때 다시 검토합니다.

각 저장소에는 다음이 있어야 합니다.

- 저장소별 lesson 규칙을 설명하는 `docs/lessons/README.md`
- 중요한 사건마다 하나의 lesson 파일. 이름은 `YYYY-MM-DD-{slug}.md`
- 거버넌스 결정을 설명하는 lesson에서 중앙 Issue 또는 PR로 연결하는 링크

## Workspace guidance 계약

Workspace 루트 guidance 파일은 일반 Git 저장소 밖에 있으므로 조직
`.github` 저장소가 `docs/workspace/` 아래의 canonical 사본을 소유합니다.

추적하는 workspace 파일은 다음과 같습니다.

- `AGENTS.md`
- `CLAUDE.md`
- `WIP.md`

`scripts/sync_workspace_docs.py --check`로 drift를 확인하고,
`scripts/sync_workspace_docs.py --sync`로 활성 workspace 루트 사본을
갱신합니다.

## Lesson 템플릿

재사용할 템플릿은 `docs/templates/lesson.md`를 사용합니다.

필수 섹션은 다음과 같습니다.

- Context
- Decision or Finding
- Outcome
- Verification
- Future Guidance

Lesson은 간결하게 유지합니다. 명령, PR 링크, Issue 링크 또는 workflow
실행 같은 증거는 저장하되 긴 로그를 붙여 넣지 않습니다.

## 일일 또는 세션 통합

중요한 작업이 끝나면 다음을 수행합니다.

1. 새 저장소별 lesson과 최근 PR을 확인합니다.
2. 중복 lesson을 합치거나 관련 항목을 서로 연결합니다.
3. 반복 가능한 규칙을 `AGENTS.md`, workflow 문서 또는 skill로 승격합니다.
4. 사건에 종속된 증거는 lesson 파일에 남깁니다.
5. lesson이 거버넌스 항목을 닫으면 중앙 Issue 댓글을 갱신합니다.

## 현재 inventory

| 저장소 | Lesson 상태 | 비고 |
|---|---|---|
| `bluetape4k-aws` | 활성 | Assertion migration lesson이 있고 README를 정규화함 |
| `bluetape4k-dependencies` | 준비됨 | 향후 release/BOM lesson을 위한 README가 있음 |
| `bluetape4k-experimental` | 준비됨 | 실험 runtime 발견 사항을 여기에 기록 |
| `bluetape4k-exposed` | 활성 | 문서 저장소 lesson이 있고 README를 정규화함 |
| `bluetape4k-graph` | 준비됨 | graph/runtime lesson용 README가 있음 |
| `bluetape4k-image` | 준비됨 | image processing과 native dependency lesson용 README가 있음 |
| `bluetape4k-javers` | 준비됨 | audit/diff 통합 lesson용 README가 있음 |
| `bluetape4k-leader` | 활성 | 풍부한 lesson 이력이 있고 README를 정규화함 |
| `bluetape4k-projects` | 활성 | virtual-thread lesson과 Kover aggregation 보강이 있음 |
| `bluetape4k-text` | 준비됨 | tokenizer/language detection lesson용 README가 있음 |
| `bluetape4k-workshop` | 활성 | Nightly dependency lesson을 보강함 |

## 승격 규칙

- 일회성 실패는 `docs/lessons/`에 남깁니다.
- 반복되는 실패는 checklist guidance가 됩니다.
- 구현 동작을 바꾸는 규칙은 저장소별 `AGENTS.md` 또는 좁은 범위의 skill에
  둡니다.
- 조직 전체 workflow 동작은 `.github/docs/governance/`에 둡니다.
