# 조직 README는 profile 저장소에 둔다

## 맥락

bluetape4k 조직 profile README를 특수 `.github` 저장소를 통해 만들었습니다.

## 결정 또는 발견

조직을 대상으로 하는 문서는 `.github/profile/README.md`에 두고 프로젝트별
문서는 각 대상 저장소에 둡니다.

## 결과

조직 profile은 모든 저장소 README를 복제하지 않고 bluetape4k library,
workshop, example 프로젝트를 소개할 수 있습니다.

## 검증

- `.github` 저장소가 조직 profile 표면을 소유합니다.
- 프로젝트 저장소는 자체 build, 모듈, 사용법 README를 유지합니다.

## 다음 지침

- 생태계 방향 설명은 조직 README에 둡니다.
- build, 모듈, 사용법 상세는 각 저장소 README에 둡니다.
