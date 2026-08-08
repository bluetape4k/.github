# Snapshot reference 정책

## 맥락

Release runbook에서 check-in된 개발 version과 workflow가 주입하는 snapshot
publish version을 구분해야 했습니다.

## 결정

모든 release 뒤 `baseVersion`을 다음 release version으로 올리고
`snapshotVersion=`은 비워 둡니다. Snapshot publish는
`-PsnapshotVersion=-SNAPSHOT`을 주입하고 release publish는 `baseVersion`만
사용합니다. 개발 중 내부 `bluetape4k-*` reference는 일치하는 `-SNAPSHOT`을
사용하고, release-prep branch에서는 upstream release가 Maven Central에
공개된 뒤에만 suffix를 제거합니다.

## 결과

중앙 governance 문서가 canonical `Version Management Policy`를 소유하고
release runbook과 pre-release checklist는 이를 참조합니다.

## 검증

- `git diff --check`
