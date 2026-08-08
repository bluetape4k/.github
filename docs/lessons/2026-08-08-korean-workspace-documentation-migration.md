# bluetape4k workspace 한국어 기술문서 migration

## 맥락

bluetape4k workspace의 독자용 기술문서와 사람이 작성한 공개 GitHub 기록을
한국어 기술문체로 정비한다. `clinic-appointment`의 완료된 migration을
reference로 사용한다.

## 범위와 예외

- 독자용 `docs/**/*.md`, `WIP.md`, release note, lesson, runbook, API 문서를
  한국어로 작성한다.
- 일반 library 저장소는 영어 `README.md`와 source-equivalent 한국어
  `README.ko.md`를 함께 유지한다. Workshop/example도 같은 bilingual 계약을
  따른다.
- 기존 코드, 명령, API/identifier, URL, 버전, Issue/PR 번호, commit SHA,
  라벨, milestone, exact error, 기계 판독 token은 보존한다.
- `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, prompt, workflow guidance 같은
  agent-facing 문서는 영어 계약을 유지한다.
- `docs/workspace/DIAGRAM_GENERATION_GUIDE.md`와 `docs/templates/lesson.md`처럼
  generator/agent가 직접 소비하는 운영 가이드와 template도 영어 계약을
  유지한다. 이 문서들은 독자용 기술 설명이 아니라 재현 가능한 운영 입력이다.
- `clinic-appointment`는 이미 완료했으므로 다시 변경하지 않는다.
- Dependabot 등 bot이 작성한 Issue/PR은 재작성하지 않는다.
- 기존 public commit SHA는 force rewrite하지 않는다. 이번 작업 이후 생성하는
  commit 메시지부터 한국어 Lore 형식을 사용한다.

## 처리 순서

1. 저장소별 문서 inventory와 독자/agent audience를 고정한다.
2. 독자용 문서를 격리 worktree에서 한국어화한다.
3. 문서 링크, 명령, 코드 block, 숫자, identifier를 원문과 대조한다.
4. 사람이 작성한 GitHub Issue/PR의 제목·본문을 한국어로 갱신한다.
5. 갱신 직후 `gh api`로 제목, 본문, author, 상태, assignee, label,
   milestone, PR head SHA를 live read-back한다. PR 본문은 마지막
   `## DoD Status`까지 정확히 확인한다.
6. `git diff --check`와 저장소별 문서 검증을 통과한 뒤 PR-ready 상태로
   남긴다. 병합은 별도 승인 게이트다.

## 현재 `.github` 배치

이번 배치에서 다음 중앙 governance, lesson, release audit, release runbook
문서를 한국어 기술문체로 정비했다.

- `SECURITY.md`
- `docs/governance/*.md` 중 기준선, dependency, Kover, Nightly, inventory,
  branch protection, lesson 계약 문서
- `docs/lessons/`의 governance/release lesson
- `docs/release/2026-05-23-release-train-audit.md`
- `docs/release/central-portal-release-runbook.md`
- `docs/workspace/README.md`

대형 `docs/workspace/WIP.md`는 원문 구조 보존 검증에서 축약 결함이 발견되어
원문 상태로 되돌렸으며, 후속 배치의 미완료 범위다. `DIAGRAM_GENERATION_GUIDE.md`
와 template는 agent/generator 계약 때문에 계속 영어로 유지한다. 이 문서는
migration 자체의 영속적인 범위와 read-back 계약을 기록하며, 완료되지 않은
저장소를 완료로 표시하지 않는다.

## 검증

- 대상 worktree: `.worktrees/docs-korean-writer-github`
- 변경 문서: 32개
- `git diff --check`: 통과
- agent-facing `AGENTS.md`, `CLAUDE.md`, `SKILL.md`는 변경하지 않음
- GitHub metadata는 문서 배치 검증 후 대상별 live read-back 수행

## 다음 지침

각 저장소의 문서 배치와 GitHub metadata batch는 별도의 PR로 유지한다.
한 저장소의 한국어화가 끝났다고 다른 저장소 또는 과거 commit 이력이
완료되었다고 추정하지 않는다. 공개 기록을 수정할 때는 항상 수정 직후
원격 API 응답을 보관하고, 본문이 비어 있거나 English-only로 남은 항목을
PR-ready로 보고하지 않는다.
