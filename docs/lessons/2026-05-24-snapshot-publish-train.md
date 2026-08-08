# Snapshot publish train

## 맥락

2026년 5월 release train 뒤 각 `bluetape4k-*` 저장소를
`snapshotVersion=`을 비운 다음 개발 line으로 reopen하고, 내부
`bluetape4k-*` reference를 일치하는 `-SNAPSHOT` version으로 되돌렸습니다.
그 다음 실제 `publish-snapshot.yml` 실행을 dependency 순서대로 검증해야
했습니다.

## 결정 또는 발견

Release 준비의 비공식 후속 작업이 아니라 dependency 순서를 따르는 독립적인
train으로 다룹니다. `projects`를 먼저 publish/검증하고 downstream 저장소를
처리한 뒤 `bluetape4k-dependencies`를 마지막에 publish합니다.

저장소마다 workflow 입력이 같다고 가정하지 않습니다. 일부
`publish-snapshot.yml`은 `diagnoseSigning`을 받지 않습니다.

Snapshot artifact의 사용 가능성은 Central snapshot `maven-metadata.xml`로
확인해야 합니다. `-SNAPSHOT` version에 release Maven Central POM URL을
사용하면 잘못된 증거가 됩니다.

## 결과

Release runbook에 dependency 순서, dispatch 명령, metadata 검증 URL 형태,
`bluetape4k-dependencies` snapshot verifier 명령을 포함한
`Post-release Snapshot Publish Train` section을 추가했습니다.

Pre-release checklist와 version governance policy도 snapshot metadata 증거와
저장소별 snapshot workflow 입력을 명시합니다.

## 검증

- `git diff --check`
- `rg -n '^#' docs/release docs/governance docs/lessons`로 Markdown heading
  inventory 검토

## 다음 지침

모든 release 뒤 다음 개발 line을 먼저 열고 snapshot publish train을 순서대로
실행합니다. Downstream consumer의 release 준비를 시작하기 전에 PR URL,
publish run ID, snapshot metadata timestamp를 기록합니다.
