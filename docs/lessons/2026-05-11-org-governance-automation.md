# 조직 거버넌스 자동화에서 얻은 교훈

## 맥락

bluetape4k 조직은 의존성 업데이트, 브랜치 보호, 보안 기준선 가시성,
저장소 inventory drift를 위한 거버넌스 자동화를 추가했습니다.

## 교훈

- Dependabot은 업데이트 PR을 생성해야 하지만 모든 PR을 사람에게 기본
  할당해서는 안 됩니다. Dependabot 활성화 직후 조직 전체에서 알림이
  폭증합니다.
- 저장소 간 일관성을 Dependabot만으로 위임할 수 없습니다. Dependabot은
  저장소 단위로 동작하므로 `.github`가 중앙 version drift와 governance
  drift 감사를 제공해야 합니다.
- 호환성 라인 alias는 자동 semver-major 업데이트에서 보호해야 합니다.
  `kafka3`/`kafka4`, `jackson2`/`jackson3`, `spring-boot3`/`spring-boot4`는
  지원 platform line을 나타내지만 Dependabot은 Maven coordinate나 plugin ID만
  보고 이전 major를 새 major로 바꿀 수 있습니다.
- 숫자 suffix만 유일한 신호는 아닙니다. suffix가 없는 alias도 이전
  compatibility line을 나타낼 수 있습니다. `ignite`는 Apache Ignite 2.x,
  `ignite3`는 3.x를 뜻하며 `spring-kafka`는 3.x, `spring-kafka4`는 4.x를
  뜻합니다. 중앙 drift 검사는 alias 이름 비교가 아니라 예상 major를
  검증해야 합니다.
- 모든 의존성 업데이트에 Full Nightly가 필요한 것은 아닙니다. 변경의
  runtime 영향과 통합 비용에 따라 검증 단계를 선택합니다.

## 결과

중앙 `.github` 저장소에 version drift, Nightly dispatch, security baseline,
repository inventory 감사를 두고 각 repository workflow에는 실제 검증을
남겼습니다.

## 검증

정책 문서, inventory, workflow 설정을 대조하고 관리 대상 repository의
drift audit을 실행했습니다.
