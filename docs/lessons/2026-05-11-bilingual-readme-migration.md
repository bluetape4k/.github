# 이중 언어 README는 한 쌍으로 관리해야 한다

## 맥락

최근 문서 작업에서 bluetape4k example과 application README를 영어/한국어
쌍으로 전환했습니다.

## 결정 또는 발견

`README.md`와 `README.ko.md`를 하나의 문서 표면으로 취급합니다. 공개 동작,
설정 또는 사용법 변경으로 한 언어를 수정하면 같은 PR에서 다른 언어도
확인합니다.

## 결과

Workspace guidance는 bluetape4k 모듈 README 쌍과 제목 바로 아래의 언어
전환 링크를 요구합니다.

## 검증

- Workspace `AGENTS.md`에 paired README 규칙이 기록되어 있습니다.
- 최근 README migration PR이 영어/한국어 쌍 형태를 사용했습니다.

## 다음 지침

- 별도의 승인된 범위가 없다면 한국어만 또는 영어만 수정한 모듈 README를
  남기지 않습니다.
- 독자가 언어를 쉽게 전환할 수 있도록 `English | 한국어` 링크를 제목 아래에
  둡니다.
