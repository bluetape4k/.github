# bluetape4k 브랜치 보호 거버넌스

## 목적

관리 대상 저장소의 변경은 pull request를 통해 반영해야 합니다. 기본
브랜치나 릴리스 브랜치에 직접 push하면 릴리스 train 상태를 감사하기
어렵고 CI를 우회할 수 있습니다.

## 현재 기준선

GitHub 조직 수준 ruleset을 우선하지만, bluetape4k 조직은 GitHub Team으로
업그레이드하기 전까지 이를 사용할 수 없습니다. 그 전까지는 저장소 수준
ruleset을 기준선으로 적용합니다.

저장소 ruleset 이름은 `bluetape4k default branch guard`이며 다음 대상에
적용합니다.

- `~DEFAULT_BRANCH`
- `refs/heads/main`

규칙은 다음과 같습니다.

- 브랜치 삭제를 차단합니다.
- non-fast-forward 업데이트를 차단합니다.
- pull request를 통한 변경을 요구합니다.
- 아직 승인을 필수로 요구하지 않습니다.
- 아직 status-check 이름을 필수로 요구하지 않습니다.

저장소 inventory와 workflow drift 감사가 안정적인 job 이름을 제공한 뒤에
승인과 필수 status check를 추가합니다. 그 전에 check 이름을 고정하면
유효한 유지보수 PR을 깨뜨리는 취약한 규칙이 될 수 있습니다.

## 문서 전용 PR 정책

브랜치 보호가 status check를 명시적으로 요구하지 않는 한 문서 전용 PR은
고비용 CI를 기다리지 않습니다. 로컬 기준선은 다음과 같습니다.

- 변경한 문서 내용을 검토합니다.
- `git diff --check`를 실행합니다.
- 렌더링 문서, 생성 문서 또는 공개 웹사이트에 영향을 주는 경우에만
  저장소별 문서 빌드를 실행합니다.

GitHub `Automatic Dependency Submission` / `submit-gradle` check는 참고
신호로 유용하지만, 브랜치 보호에서 필수 check로 명시하지 않았다면 문서
전용 PR의 병합을 막지 않습니다.

## 운영 명령

감사:

```bash
python3 scripts/repo_ruleset_guard.py
```

기준선 적용 또는 갱신:

```bash
python3 scripts/repo_ruleset_guard.py --apply
```

## 범위

관리 범위는 주요 bluetape4k 라이브러리, `.github`, 그리고 선정된
워크숍/예제 저장소입니다. `ocean-workshop`과 `kotlin-dev-agent`는 계속
제외합니다.
