# Nightly 거버넌스에는 저장소별 scope 계약이 필요하다

## 맥락

Issue #2에서 bluetape4k의 고비용 Nightly job을 daily smoke와 weekly full로
나눴습니다. 조직 `.github` 저장소는 여러 저장소에 Nightly workflow를
dispatch하지만, 실제 Gradle job과 coverage/runtime 비용은 각 대상 저장소가
소유합니다.

## 결정

조직 수준 공통 scope 계약은 `smoke`와 `full`로 유지합니다. 저장소는 자체
workflow 안에서만 특화 scope를 제공하고, `org-workflows.json`에서는 지원되는
공통 입력만 매핑합니다.

## 결과

- daily Nightly는 기본 smoke로 빠르게 실행할 수 있습니다.
- weekly full Nightly는 폭넓은 통합 신호를 유지합니다.
- 중앙 dispatcher는 지원하지 않는 workflow에 저장소 전용 scope를 보내지
  않습니다.
- 고비용 저장소는 분리 여부, 의도적인 단순화 여부, release dispatch 제외
  여부를 문서화합니다.

## 검증

문서와 workflow inventory를 대조하고, 변경한 workflow의 dispatch 입력을
저장소별로 확인했습니다.
