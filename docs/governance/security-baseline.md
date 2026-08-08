# bluetape4k 보안 기준선

## 목적

보안 거버넌스는 모든 pull request를 전체 보안 스캔으로 만들지 않으면서도
저장소 위험을 보이게 해야 합니다. 기준선은 항상 실행하는 검사와 예약 또는
릴리스에 민감한 검사를 분리합니다.

## 기준선

관리 대상 저장소는 다음 항목을 갖춰야 합니다.

- 저장소별 `SECURITY.md` 또는 `.github/SECURITY.md`의 조직 기본 정책을 통한
  보안 제보 경로
- Gradle과 GitHub Actions에 대한 Dependabot
- CI의 gitleaks 또는 이에 준하는 예약 워크플로를 통한 secret scanning
- 명시적으로 제외하지 않은 source-heavy 저장소의 CodeQL
- 필요한 경우 dependency submission을 통한 dependency graph 가시성

## 트리거 정책

| 검사 | 권장 트리거 |
|---|---|
| 변경 내용의 Gitleaks | Pull request CI |
| 전체 이력 secret scan | 예약된 보안 워크플로 또는 수동 실행 |
| CodeQL | 비용이 허용되면 pull request, 아니면 예약 실행 |
| Dependency submission | 기본 브랜치 CI와 Gradle metadata가 바뀐 PR |
| Dependabot security updates | 자동 PR 생성 후 의존성 위험 등급에 따른 검증 |

## 감사 명령

```bash
python3 scripts/security_baseline_audit.py
```

감사는 적용 범위만 보고합니다. 워크플로 정규화는 저장소 inventory와
workflow drift 작업에서 담당합니다. 그래야 취약한 추측 대신 안정적인 job
이름으로 필수 check를 추가할 수 있습니다.
