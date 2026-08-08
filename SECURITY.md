# 보안 정책

## 지원 범위

bluetape4k 조직이 관리하는 공개 `bluetape4k` 라이브러리와 관리 대상
워크숍/예제 저장소의 보안 제보를 접수합니다.

`ocean-workshop`과 `kotlin-dev-agent`는 현재 거버넌스 범위에 포함하지
않습니다.

## 취약점 제보

가능한 경우 GitHub Security Advisories를 통해 의심되는 취약점을 비공개로
제보합니다. 저장소에서 비공개 취약점 제보를 제공하지 않으면 저장소
소유자에게 직접 연락합니다.

수정 또는 완화 조치를 적용할 수 있을 때까지 악용 가능한 세부 내용을 공개
Issue에 게시하지 마세요.

## 기본 기대사항

관리 대상 저장소는 다음 항목을 유지해야 합니다.

- CI 또는 예약된 보안 워크플로에서 secret scanning을 수행합니다.
- CodeQL을 사용하거나 코드 스캔 제외 사유를 명시합니다.
- Dependabot, dependency graph 또는 Gradle dependency submission으로 의존성
  가시성을 확보합니다.
- 중앙 버전 drift 보고서와 Nightly 워크플로 정책으로 릴리스에 영향을 주는
  의존성 업데이트를 검증합니다.

중앙 `.github` 저장소는 이 기대사항을 점검하는 감사 스크립트와 거버넌스
문서를 관리합니다.
