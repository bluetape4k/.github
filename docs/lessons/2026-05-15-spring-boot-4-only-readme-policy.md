# Spring Boot 4 전용 README 정책

## 맥락

조직 profile README가 여전히 bluetape4k를 Spring Boot 3/4 지원으로
설명했습니다. 현재 정책은 지원하는 Spring integration을 Spring Boot 4.x
전용으로 두는 것입니다.

## 결정 또는 발견

README의 지원 문구는 Spring Boot 4.x만 지원한다고 설명해야 합니다. Spring
Boot 3은 역사적 migration note, 비교표, 지원 제거 공지 또는 legacy helper
경고에는 남길 수 있지만 현재 지원 주장으로 사용하지 않습니다.

## 결과

- 조직 profile README 쌍에서 Spring Boot 3/4 호환성 문구를 제거했습니다.
- 오래된 `bluetape4k-workshop` README heading/설명에서 Boot 4 example을
  "Spring Boot 3"이라고 부르던 부분을 고쳤습니다.
- `bluetape4k-projects` OpenTelemetry README 쌍에서 오래된 WebFlux helper를
  현재 Boot 3 지원이 아니라 legacy/migration reference로 표현했습니다.

## 검증

현재 지원 문구와 legacy 문구를 README 쌍에서 대조했습니다.
