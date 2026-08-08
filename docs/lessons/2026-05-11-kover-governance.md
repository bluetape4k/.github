# Kover 거버넌스는 게이트 전에 기준선이 필요하다

## 맥락

Issue #1에서 bluetape4k 저장소 전체의 Kover 커버리지를 검토했습니다. 대부분
저장소가 이미 Kover 보고서를 만들지만, 일부 모듈만 검증 임계치를 강제합니다.

## 결정 또는 발견

측정된 기준선 없이 광범위한 실패 커버리지 게이트를 활성화하지 않습니다.
저장소별 정책 문서로 모듈이 강제 대상인지, report-only인지, 의도적으로
제외되었는지를 기록합니다.

## 결과

조직 정책은 core library, 통합 중심 대상, report-only 전환, workshop/demo
예외를 분리합니다.

## 검증

- 중앙 inventory를 `docs/governance/kover-coverage-governance.md`에 만들었습니다.
- Issue 범위의 각 저장소에 저장소별 커버리지 정책을 추가했습니다.
- 기존 `leader` Kover bounds는 이제 Nightly에서 실행됩니다.
