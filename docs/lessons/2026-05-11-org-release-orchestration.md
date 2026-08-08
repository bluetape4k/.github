# 조직 release orchestration에는 dry-run 게이트가 필요하다

## 맥락

bluetape4k 조직은 2026년 5월 말 공식 release를 준비했습니다. version drift,
Full Nightly dispatch, snapshot publish, release dispatch에는 조직 수준 운영
표면이 필요했습니다.

## 결정

중앙 orchestration은 조직 `.github` 저장소에 두되 기본값으로 publish하지
않습니다. 저장소 간 snapshot/release workflow는 `dryRun=true`를 기본으로
하고 실제 publish dispatch에는 명시적인 확인 문구가 필요합니다.

## 결과

중앙 `.github` 저장소가 다음을 소유합니다.

- 공유 version drift 보고
- 조직 Nightly dispatch 계획
- snapshot dispatch 계획과 실행
- release train dispatch 계획과 실행

대상 저장소는 자체 publish credential, signing key, package permission,
release workflow 동작을 계속 책임집니다.

## 검증

dry-run dispatch에서 대상과 순서를 확인하고, 실제 publish 입력에는 확인
문구가 없으면 거부되는지 검증했습니다.
