# gpt-5.6 지침 단순화 교훈

## 맥락

workspace `AGENTS.md`에는 언어 정책, 검색 도구, module 등록, Kover,
Testcontainers, merge 승인 규칙이 여러 절에서 반복되어 있었다. 이전 모델의
누락을 막기 위해 추가한 설명이 최신 모델에서는 탐색 비용과 충돌 가능성을
높였다.

## 결정

- 안전과 외부 부작용 경계는 명시적으로 유지한다.
- 언어 정책은 audience 표를 단일 기준으로 삼는다.
- module 등록, coverage, heavyweight test, merge gate는 각각 한 곳에서만
  정의한다.
- 도구는 목적과 fallback만 규정하고 명령 목록은 제거한다.
- 일반적인 작은 diff, targeted test, 표준 도구 선택은 모델에 맡긴다.

## 결과와 검증

`docs/workspace/AGENTS.md`를 643줄에서 545줄로 줄였다. 임시 workspace에
canonical 문서를 동기화한 뒤 `sync_workspace_docs.py --check`와
`git diff --check`를 통과했다.

## 다음 작업 원칙

새 지침을 추가하기 전에 기존 canonical owner가 있는지 확인한다. 반복되는
실패가 machine check나 단일 규칙으로 막히면 여러 절에 설명을 복제하지
않는다.
