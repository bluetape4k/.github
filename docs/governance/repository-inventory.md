# bluetape4k 저장소 inventory

## 목적

`org-workflows.json`은 관리 대상 저장소의 중앙 machine-readable inventory입니다.
워크플로 dispatch를 구동하고 release, snapshot, Nightly, Dependabot, 보안,
커버리지 정책에 대한 기대사항을 기록합니다.

## 관리 플래그

`governance` 아래의 각 항목은 다음을 정의합니다.

- `default_ref`: 예상하는 통합 브랜치
- `dependabot`: `.github/dependabot.yml`이 필요한지 여부
- `security`: 보안 정책과 보안 워크플로 적용이 필요한지 여부
- `coverage`: `docs/governance/kover-coverage-policy.md`가 필요하면 `policy`,
  로컬 정책 문서 없이 커버리지만 추적하면 `report-only`, 그 외에는 `excluded`
- `release`, `snapshot`, `nightly`: 해당 저장소가 그 train에 참여하는지 여부

## 감사 명령

```bash
python3 scripts/workflow_drift_audit.py --workspace ..
```

예상되는 보안/워크플로 category가 완전히 정규화된 뒤 CI에서
`--fail-on-drift`를 사용합니다.

## 제외 대상

`ocean-workshop`과 `kotlin-dev-agent`는 이 inventory에서 의도적으로
제외합니다. 운영 소유권이 바뀔 때만 추가합니다.
