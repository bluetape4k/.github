# 순차 release line 정책

## 맥락

`bluetape4k-projects`는 `1.9.1` release train 이후 `1.9.2`와 `1.10.0`
milestone을 모두 열어 두었습니다. 오래된 PR이 `1.9.2`가 다음 patch line을
소유하는 동안 `develop`을 바로 `1.10.0`으로 옮기려 했습니다.

## 결정

기본값은 순차 release-line 작업으로 둡니다.

- `develop`은 현재 활성 release line에 둡니다.
- 활성 patch milestone을 다음 minor line으로 옮기기 전에 완료하거나 명시적으로
  연기합니다.
- `develop`이 다음 minor line으로 전진한 뒤 patch hotfix가 필요할 때만 마지막
  release tag에서 `release/X.Y.x` maintenance branch를 만듭니다.

## 결과

`bluetape4k-projects`는 먼저 `1.9.2` development line을 열었습니다.
`1.10.0` Ktor 모듈 family는 `1.9.2` patch line을 처리하거나 명시적으로
연기한 뒤의 다음 minor lane으로 남았습니다.

## 검증

milestone 순서와 `develop` version을 live GitHub 상태와 대조했습니다.
