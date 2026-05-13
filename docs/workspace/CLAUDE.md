# CLAUDE.md — bluetape4k Workspace Root

이 디렉토리는 **bluetape4k GitHub org** 의 모든 레포지토리를 담는 로컬 workspace다.
각 하위 디렉토리가 독립 Git 레포지토리이며, 각각의 `CLAUDE.md` 에는 레포별 세부 사항이 있다.
이 파일의 규칙은 하위 레포 작업 시 모두 적용된다.

---

## 레포지토리 목록

### 라이브러리 (bluetape4k ecosystem)

| 디렉토리 | 설명 |
|---------|------|
| `bluetape4k-projects/` | **코어** — 공유 Kotlin/JVM 백엔드 라이브러리 컬렉션. `core`, `coroutines`, `data/*`, `infra/*`, `spring-boot3/4/`, `virtualthread/` 포함 |
| `bluetape4k-experimental/` | 실험적 모듈 — Kotlin 2.3 + Java 25 + Spring Boot 4. 미출판 |
| `bluetape4k-aws/` | AWS SDK v2 + AWS Kotlin SDK 래퍼. Coroutines/Spring Boot 4/Ktor 3 지원 |
| `bluetape4k-image/` | 이미지 처리 — scrimage(Java2D) + libvips(JNI/FFM Panama) 이중 백엔드 |
| `bluetape4k-javers/` | Javers 감사(audit)/diff — Redis·Kafka 백엔드 + Exposed 통합 |
| `bluetape4k-leader/` | 분산 리더 선출 — blocking/async/coroutine/virtual-thread API, Redis 백엔드 |
| `bluetape4k-text/` | 텍스트 처리 — 한국어·일본어 형태소, 다국어 감지, Aho-Corasick 검색 |
| `bluetape4k-graph/` | 그래프 — Neo4j·Memgraph·AGE·TinkerPop·FalkorDB 연동 |
| `bluetape4k-exposed/` | JetBrains Exposed ORM 래퍼 — bluetape4k 통합 확장 |
| `bluetape4k-dependencies/` | **BOM** — bluetape4k 전체 생태계 버전 집중 관리 |

### 워크샵 / 예제

| 디렉토리 | 설명 |
|---------|------|
| `bluetape4k-workshop/` | bluetape4k 라이브러리 활용 백엔드 예제 모음 |
| `exposed-workshop/` | JetBrains Exposed ORM 예제 |
| `exposed-r2dbc-workshop/` | Exposed R2DBC 예제 |
| `ocean-workshop/` | 해양·기상 데이터 시각화 — Kotlin + Spring Boot 4 + bluetape4k |
| `clinic-appointment/` | 클리닉 예약 앱 예제 |
| `timefold-workshop/` | Timefold Solver 워크샵 |
| `kotlin-dev-agent/` | Kotlin 개발 에이전트 실험 |

---

## 공통 기술 스택

- **언어**: Kotlin 2.3+ · **JVM**: Java 21 (코어) / Java 25 (experimental 등)
- **빌드**: Gradle 멀티모듈 — `settings.gradle.kts` 의 `includeModules()` 자동 등록
- **프레임워크**: Spring Boot 3.x (코어) / Spring Boot 4.x (experimental, aws, image 등)
- **비동기**: Kotlin Coroutines 우선
- **테스트**: JUnit 5 + MockK + bluetape4k-assertions; Testcontainers (singleton companion object 패턴)
- **컴파일러 플래그**: `-Xjsr305=strict -jvm-default=enable -Xinline-classes -Xcontext-parameters`

---

## Kotlin 편집 워크플로우 (MANDATORY)

클래스 수정 전: `ide_find_references` 또는 `get_impact_radius_tool` 로 영향 파일 확인.

`.kt` 파일 편집 후 **매번**:

1. `ide_diagnostics` — import 오류 + `@Deprecated` 경고 확인
2. import 오류 → `ide_optimize_imports` 로 수정
3. `@Deprecated` → `lsp_code_actions` 로 Quick Fix 적용 — 미해결 절대 방치 금지
4. 위 단계 통과 후에만 빌드/컴파일

---

## 핵심 설계 패턴 (CRITICAL)

### assert vs require — 예외 타입 절대 변경 금지

- `assertXxx()` → `AssertionError` — 내부 불변식. 신규 코드에서 사용 금지(`@Deprecated`)
- `requireXxx()` → `IllegalArgumentException` — 파라미터 검증. **항상 이것 사용**

```kotlin
fun add(keyword: String): Builder = apply {
    keyword.requireNotBlank("keyword")   // ✅ IllegalArgumentException
}
```

### Coroutines-First

- 모든 비동기 작업은 Kotlin Coroutines 사용
- 블로킹 API 호출 → `withContext(Dispatchers.IO)` 래핑
- `runBlocking` 은 프로덕션 코드에서 사용 금지 (`lazy` 초기화 예외)
- `CancellationException` 은 반드시 re-throw — `catch(Exception)` 앞에 항상 추가

```kotlin
// ❌ 잘못된 패턴
try { doSomething() }
catch (e: Exception) { log.warn(e) { "실패" } }

// ✅ 올바른 패턴
try { doSomething() }
catch (e: CancellationException) { throw e }
catch (e: Exception) { log.warn(e) { "실패" } }
```

- `runCatching {}` 블록 안에 suspend 호출이 있으면 수동 try-catch로 전환 (`runCatching`은 CancellationException을 삼킴)
- `withContext(NonCancellable)` 안에서도 예외없이 적용

### Virtual Threads — 동기화 금지

`@Synchronized` / `synchronized {}` 절대 사용 금지 → `reentrantLock()` 사용

### atomicfu

클래스 프로퍼티 레벨에서만 사용 — 메서드 로컬 변수에 사용 금지

### Null Safety

- `!!` 절대 사용 금지
- `?.`, `?:`, `requireNotNull()` 사용

### 불변성

- `val` 우선 사용
- 기존 객체 변경 금지 — 항상 새 인스턴스 반환
- options/state → `data class`
- 모든 `data class` 는 `java.io.Serializable` 을 구현하고 `serialVersionUID` 를 정의한다.

### 함수 인자 — 동종 타입 파라미터는 data class로 래핑

2개 이상의 동종 타입 파라미터(Int/Int, String/String 등)는 named data class로 묶는다.

```kotlin
// ❌ positional 혼동 위험
fun smartCrop(width: Int, height: Int): Image

// ✅ 컴파일 시점에 혼동 방지
data class AspectRatio(val width: Int, val height: Int)
fun smartCrop(ratio: AspectRatio): Image
```

- `XxxOptions`, `XxxArgs`, `XxxConfig` 등 의미 명확한 이름 사용
- 파라미터 추가 시 binary-compatible 확장 가능

### 에러 처리

- `runCatching {}` 로 throwable 경계 처리 — **suspend 호출이 없는 경우만**
- suspend 함수 안에서 `runCatching {}` 사용 금지 — `CancellationException` 을 삼킴 → 수동 try-catch 사용
- 에러 묵살(silent swallow) 금지 — 항상 명시적 처리

---

## 테스트 규칙

### 기본 도구

- **JUnit 5 + MockK + bluetape4k-assertions**
- 모든 테스트 베이스 클래스에 `@TestInstance(TestInstance.Lifecycle.PER_CLASS)` 적용
- suspend 테스트 → `runTest` 사용 (가상 시간 자동 진행)
- 테스트 이름은 backtick 으로 감싼 설명형 이름 사용

```kotlin
@Test
fun `should return null when leader not elected`() { ... }
```

- bluetape4k-assertions 비교 매처 사용 — `(x >= y).shouldBeTrue()` 금지

```kotlin
result.size shouldBeGreaterOrEqualTo 1   // ✅
(result.size >= 1).shouldBeTrue()        // ❌
```

### 예외 검증 패턴

`assertFailsWith<T> { }` 를 사용한다. `invoking { } shouldThrow` 나 JUnit5 `assertThrows` 사용 금지.

```kotlin
import io.bluetape4k.assertions.assertFailsWith  // 또는 io.bluetape4k.assertions.internal.assertFailsWith

assertFailsWith<IllegalArgumentException> {
    doSomethingThatThrows()
}
```

| 패턴 | 사용 여부 |
|------|----------|
| `assertFailsWith<T> { }` | ✅ 표준 |
| `coInvoking { suspendCall } shouldThrow T::class` | ✅ suspend 전용 |
| `invoking { } shouldThrow T::class` | ❌ 금지 |
| `org.junit.jupiter.api.assertThrows<T> { }` | ❌ 금지 |
| `kotlin.test.assertFailsWith` | ❌ 금지 |

### 신규 모듈 필수 테스트 리소스

모든 신규 모듈은 `src/test/resources/` 에 다음 두 파일 필수 포함:

**junit-platform.properties:**
```properties
junit.jupiter.extensions.autodetection.enabled=true
junit.jupiter.testinstance.lifecycle.default=per_class

junit.jupiter.execution.parallel.enabled=false
junit.jupiter.execution.parallel.mode.default=same_thread
junit.jupiter.execution.parallel.mode.classes.default=concurrent
```

**logback-test.xml:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <appender name="Console" class="ch.qos.logback.core.ConsoleAppender">
        <immediateFlush>true</immediateFlush>
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} %highlight(%-5level) [%blue(%24.24t)] %yellow(%logger{36}):%line: %msg%n%throwable</pattern>
            <charset>UTF-8</charset>
        </encoder>
    </appender>
    <logger name="io.bluetape4k.<module>" level="DEBUG"/>
    <root level="INFO">
        <appender-ref ref="Console"/>
    </root>
</configuration>
```

### `internal` 클래스·함수 테스트

Kotlin `internal` 심볼 테스트는 동일 패키지 경로에 배치 필수:

- 소스: `src/main/kotlin/io/bluetape4k/redis/lettuce/filter/Murmur3.kt`
- 테스트: `src/test/kotlin/io/bluetape4k/redis/lettuce/filter/Murmur3Test.kt`

### Testcontainers 패턴

`GenericContainer` 직접 사용 금지. `@Testcontainers` 어노테이션 불필요.
`bluetape4k-testcontainers` 의 `XxxServer.Launcher.xxx` singleton 패턴 사용:

```kotlin
abstract class AbstractRedisTest {
    companion object : KLogging() {
        val redis = RedisServer.Launcher.redis
        val redisUrl: String get() = redis.url
    }
}
```

---

## KDoc 요구사항

모든 public 클래스, interface, object, extension function 에 KDoc 필수:

- 한 줄 요약
- `## 동작/계약` 섹션 (계약, 엣지 케이스)
- ` ```kotlin ` 사용 예제 블록

---

## README 규칙

### 이중언어 필수

모든 모듈 README: `README.md` (영어) + `README.ko.md` (한국어) 동시 유지.

### 언어 전환 링크 (모든 README 필수)

각 README 제목 바로 아래 두 번째 줄에 언어 전환 링크 추가:

**README.md:**
```markdown
# bluetape4k-<module>

[한국어](./README.ko.md) | English
```

**README.ko.md:**
```markdown
# bluetape4k-<module>

한국어 | [English](./README.md)
```

### README 구조 표준

1. **Architecture** — 개념 개요 + Mermaid UML 다이어그램 (classDiagram / sequenceDiagram / flowchart)
2. **Core Features** — 주요 기능 목록
3. **Usage Examples** — 사용 코드 예시
4. **Configuration Options** — 설정 옵션
5. **Dependency** — 의존성 추가 방법

- Mermaid UML 다이어그램 필수 — 없으면 독자가 코드 읽기 전에 이해 불가
- Vega-Lite 사용 금지 → `xychart-beta horizontal` (Mermaid) 사용
- 루트 README 수정 시 `README.md` + `README.ko.md` 모두 업데이트

---

## 빌드·커버리지 규칙

### 커버리지: Kover 전용

- Jacoco 사용 금지. 모든 레포 표준 커버리지 도구는 **Kover**
- 목표: 프로덕션 코드 80% 이상 (Spring Boot 통합 테스트가 nightly에서만 돌면 60%)

### kover sourceSet 제외

`benchmark`, `generated` 등 비프로덕션 sourceSet은 명시적 제외 필수:

```kotlin
kover {
    currentProject {
        sources {
            excludedSourceSets.add("benchmark")
        }
    }
}
```

### 포맷터: ktlint 금지

IntelliJ IDEA 포맷 + `.editorconfig` 사용. ktlint 자동 포맷 hook 적용 금지.

### CI 동기화

`ci.yml` 변경 시 `nightly-tests.yml` 도 동기화 필수.

---

## Spring Boot AutoConfig 규칙

### `@ConditionalOnClass` — compileOnly 클래스 name= 가드

`compileOnly` 의존성 클래스가 `@Bean` 반환 타입에 쓰이면 `name=` 배열에 해당 FQCN 추가 필수:

```kotlin
// ✅ compileOnly 반환 타입도 name= 가드
@ConditionalOnClass(name = [
    "io.micrometer.core.instrument.MeterRegistry",
    "com.example.MicrometerRecorder",
])
class FooAutoConfiguration {
    @Bean
    fun recorder(registry: MeterRegistry): MicrometerRecorder = ...
}
```

### AutoConfigure 순서 보장 — 별도 클래스 분리 필수

`@AutoConfigureOrder` / `@AutoConfigureAfter` 는 `AutoConfiguration.imports` 에 직접 등록된 클래스에만 적용된다. `@Import`로 불러온 클래스에는 무효.

1. 순서가 필요한 Configuration은 별도 파일/클래스로 분리
2. `@AutoConfiguration(after = [MainConfig::class])` 명시
3. `AutoConfiguration.imports` 에 두 클래스 모두 등록
4. `@ConditionalOnMissingBean(<type>::class)` 로 fallback 조건 명시

### INHERIT sentinel — 어노테이션 + Properties 전역 설정

어노테이션 default를 실제 값 대신 INHERIT sentinel로 지정하여 "미지정"과 "명시 설정"을 구분:

```kotlin
enum class FailureMode { INHERIT, RETHROW, SKIP }

annotation class LeaderElection(
    val failureMode: FailureMode = FailureMode.INHERIT,
)

// Aspect에서 해석
val effective = if (ann.failureMode == INHERIT) props.failureMode else ann.failureMode
```

### `@ConditionalOnProperty` — 모든 AutoConfig Phase에 중복 적용 필수

활성화 스위치(`@ConditionalOnProperty`)는 모든 AutoConfiguration phase 클래스에 중복 적용해야 한다. 진입점에만 달면 나머지 phase에서는 조건이 무시된다.

---

## Exposed 1.2.0 규칙

### 연산자 import — top-level 함수 사용

`SqlExpressionBuilder` 멤버 import 사용 금지 (DeprecationLevel.ERROR):

```kotlin
// ❌ 컴파일 오류
import org.jetbrains.exposed.v1.core.SqlExpressionBuilder.eq

// ✅ top-level import
import org.jetbrains.exposed.v1.core.eq
import org.jetbrains.exposed.v1.core.and
import org.jetbrains.exposed.v1.core.less
import org.jetbrains.exposed.v1.core.greaterEq
import org.jetbrains.exposed.v1.jdbc.exists  // Table.exists()
```

### 람다 implicit receiver 섀도잉 주의

`update { }` / `insert { }` / `deleteWhere { }` 람다 안에서 클래스 프로퍼티와 동일 이름의 컬럼이 충돌할 수 있음. 로컬 변수로 미리 추출하여 사용.

---

## 코드 변경 후 체크리스트

- [ ] `ide_diagnostics` — 오류 0, 미해결 `@Deprecated` 없음
- [ ] 변경된 모듈 컴파일 + 테스트 실행
- [ ] 변경된 모듈의 `README.md` + `README.ko.md` 업데이트
- [ ] 신규·변경 공개 API 에 KDoc 추가/수정

---

## PR 생성 전 (MANDATORY)

- [ ] 모듈 테스트 통과 (통과 수 + 소요 시간 포함 보고)
- [ ] `oh-my-claudecode:code-reviewer` 실행 — HIGH/CRITICAL 해결 후 push
- [ ] PR 설명: 테스트 결과 + 수정 이유 + 검증 커맨드 포함
- [ ] `README.md` + `README.ko.md` 업데이트
- [ ] KDoc 추가/수정 완료
- [ ] worktree (`.worktrees/<branch>/`) 에서 작업했는지 확인

---

## Git 워크플로우

### 브랜치 전략

- **`develop`** — 기본 브랜치. 모든 PR 대상. 직접 push 금지.
- **`main`** — 릴리즈 전용. `develop` → `main` PR 로만 업데이트.
- **feature 브랜치** — `.worktrees/<branch>` 에서 작업.
- 로컬 worktree/branch 이름에 `codex/` prefix를 쓰지 않는다. `feat/`,
  `fix/`, `docs/`, `refactor/`, `test/`, `build/`, `chore/` 같은 일반 prefix를 쓴다.

### 작업 흐름 (MANDATORY)

```bash
# 1. worktree 생성 (항상 develop 기준)
git worktree add .worktrees/<branch> -b feat/<name>

# 2. worktree 에서 작업
cd .worktrees/<branch>
# ... 코드 변경, 커밋 ...

# 3. PR 생성 → develop 으로
git push origin feat/<name>
gh pr create --base develop

# 4. 머지 후 정리
git worktree remove .worktrees/<branch>
git branch -d feat/<name>
```

### 릴리즈 흐름

```bash
# develop → main PR (릴리즈 시에만)
gh pr create --base main --head develop --title "release: vX.Y.Z"
```

- **Commits**: English + prefix (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `perf:`)
- **PR**: One issue = one PR, squash-merge
- **Branch protection**: `develop`, `main` 모두 PR 필수 (모든 레포 적용됨)

---

## Workspace Scripts (`bin/`)

Cross-repo 작업 스크립트. `bin/` 을 PATH 에 추가하거나 `./bin/<script>` 로 실행.

| 스크립트 | 설명 |
|---------|------|
| `all-status` | 전체 레포 git status 요약 (`repo-status` 기반) |
| `all-pull` | 전체 레포 `git pull --rebase` (upstream 없는 레포 자동 스킵) |
| `all-clean-branches` | 전체 레포 gone 브랜치 + worktree 정리 (`clean-branches` 기반) |
| `all-ci-status` | 라이브러리 레포 최신 CI 결과 요약 (`gh` CLI 필요) |

Per-repo 공통 스크립트 (`repo-status`, `repo-diff`, `repo-test-summary`, `clean-branches`, `worktree-new`, `worktree-list`, `ci-status`) 는 `~/.local/bin/` 에 있으며 PATH 에서 직접 사용.

---

## 스킬 라우팅

설치된 bluetape4k skill을 프로젝트 source of truth로 사용한다. 세부
체크리스트를 이 문서에 복제하지 말고, 구현 전에 관련 skill과 references를
로드한다.

| 스킬 | 용도 |
|------|------|
| `bluetape4k-workflow` | bluetape4k 작업의 first-stop router. Full Design, Fast Track, Bug Fix, Code Review, Maintenance를 분류하고 최소 안전 lane과 검증 수준을 선택한다. |
| `bluetape4k-design` | 신규 모듈, 신규 서비스/서브시스템, broad API 설계, 대규모 리팩터링, 신규 dependency, multi-layer 변경. spec/plan/advisor-review/DoD와 new-module checks를 소유한다. |
| `bluetape4k-patterns` | bluetape4k Kotlin 구현·리뷰. 현재 references는 testing, Spring Boot auto-config, new-module setup, final checklist/IDE diagnostics를 다룬다. |
| domain skills | 필요 시 `ecc-kotlin-patterns`, `ecc-kotlin-exposed`, `ecc-springboot-kotlin`, `ecc-kotlin-testing`, `kotlin-coroutines-skill`, `kotlin-spring`, `kotlin-expert`를 함께 로드한다. |

workflow 또는 skill-maintenance 요청에서는 durable guidance를 바꾸기 전에
관련 repo-local `docs/lessons/*.md`를 읽는다.
