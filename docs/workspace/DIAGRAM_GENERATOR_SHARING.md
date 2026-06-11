# Diagram Generator Sharing Guide

이 문서는 `bluetape4k-*`, `bluetape-*` 저장소에서 반복 작성되는 README
다이어그램 생성 스크립트를 줄이기 위한 공유 패턴 안내다.

검색 키워드: `diagram generator`, `readme-diagrams`, `Graphviz evidence`,
`geometry-summary`, `Architects Daughter`, `Comic Mono`, `shortConnectors`,
`minConnectorStem`, `bluetape4k-diagram`.

## 문제

여러 저장소에서 거의 같은 일을 하는 generator가 반복 작성되고 있다.

- Graphviz `.dot`, `.plain`, `*-graphviz.svg`, `*-graphviz.png` 생성
- 최종 hand-authored SVG 생성
- README용 PNG 렌더링
- `Architects Daughter`, `Comic Mono` 폰트 바인딩
- README가 PNG만 embed하는지 확인
- `xmllint`, forbidden UI font scan, visual preview 수행
- geometry summary 출력

반복 작성하면 repo마다 gate가 달라지고, 같은 결함이 다시 나온다. 예:
card 간격이 좁아 connector stem과 arrowhead가 안 보이는 문제는
`shortConnectors` / `minConnectorStem` 같은 generator gate가 없으면 리뷰 후에야
발견된다.

## 현재 확인된 중복 위치

2026-06-11 기준 workspace에서 확인한 generator 예시:

| Repo | Script |
|---|---|
| `bluetape-go-workshop` | `scripts/generate-*-diagrams.sh` |
| `bluetape-rs-workshop` | `scripts/generate-foundation-diagrams.py` |
| `bluetape4k-leader` | `scripts/generate-example-readme-diagrams.mjs`, `scripts/generate-module-architecture-diagrams.mjs` |
| `bluetape4k-projects` | `scripts/generate-observability-example-diagrams.mjs`, `scripts/generate-reviewed-readme-diagrams.mjs` |
| `bluetape4k.github.io` | `scripts/generate-cache-series-diagrams.mjs` |

## 공유 방향

새 저장소에서 generator를 새로 만들기 전에 다음 순서로 처리한다.

1. 기존 repo의 `scripts/generate-*diagram*`를 먼저 찾는다.
2. `bluetape-go-workshop`의 workshop-style baseline을 우선 reference로 삼는다.
3. 새 generator가 꼭 필요하면 repo-local script는 얇은 wrapper로 두고, 공통
   규칙은 공유 template/reference에서 복사하지 말고 가져온다.
4. generator output에는 반드시 `geometry-summary.txt` 또는 동등한 summary를
   남긴다.
5. 같은 결함이 한 번이라도 리뷰에서 잡히면 visual checklist가 아니라
   generator failure gate로 승격한다.

## 최소 공통 Contract

새 README diagram generator는 다음을 모두 지원해야 한다.

- 입력 모델에서 `nodes`, `routes`, `segments`를 계산한다.
- Graphviz evidence를 생성한다:
  - `.dot`
  - `.plain`
  - `*-graphviz.svg`
  - `*-graphviz.png`
- 최종 README asset을 생성한다:
  - final `.svg`
  - final `.png`
- final SVG에는 font 역할이 분리되어야 한다:
  - title/card/actor/table prominent label: `Architects Daughter`
  - details/captions/member/route label: `Comic Mono`
- final SVG에는 `Inter`, `Arial`, `Helvetica` 같은 UI font stack이 없어야 한다.
- README는 `docs/images/readme-diagrams/*.png`만 embed해야 한다.
- `geometry-summary.txt`에는 최소 다음 필드가 있어야 한다:
  - `nodes`
  - `routes`
  - `segments`
  - `badEndpointAngle`
  - `badBends`
  - `interiorCrossings`
  - `marginImbalance`
  - `margins=L/R/T/B`
  - `titleGap`
  - `fontFallback`
- flow/card connector가 있는 경우 다음 필드도 기록하고 fail-fast해야 한다:
  - `shortConnectors`
  - `minConnectorStem`

## Recommended Script Shape

```text
scripts/generate-<subject>-diagrams.{py,mjs,sh}
  1. discover required tools
  2. discover and bind required font files
  3. build diagram model
  4. write Graphviz evidence
  5. write final SVG
  6. render final PNG
  7. validate final SVG font policy
  8. validate README embed policy
  9. print and persist geometry summary
  10. fail when repeated defect gates trip
```

## Generator Gates To Promote Immediately

Do not leave these as manual review-only checks:

- card text overflow
- missing required font or renderer fallback
- SVG using UI font stack
- README embedding SVG
- missing matching PNG for SVG
- missing Graphviz evidence for node-and-connector diagrams
- connector endpoint inside a card
- connector crossing non-endpoint card interior
- connector stem too short to be visible
- label overlapping route, arrowhead, or card text
- title/subtitle too close to body content
- large one-sided outer whitespace without documented reason

## Validation Commands

Run from the target repository:

```bash
python3 scripts/generate-<subject>-diagrams.py
find docs/images/readme-diagrams -name '*.svg' -print0 | xargs -0 -n1 xmllint --noout
find docs/images/readme-diagrams -name '*.svg' -exec sh -c 'test -f "${1%.svg}.png"' sh {} \;
rg 'docs/images/readme-diagrams/.*\.svg' README*.md examples/*/README*.md && exit 1 || true
rg 'Inter|Arial|Helvetica' docs/images/readme-diagrams/*.svg && exit 1 || true
git diff --check
```

## DoD Reporting

DoD 보고에는 다음을 반드시 넣는다.

| DoD | Evidence |
|---|---|
| Existing baseline inspected | referenced repo and PNG names |
| Generator reused or shared pattern followed | script path |
| Graphviz evidence exists | `.dot/.plain/*-graphviz.svg/*-graphviz.png` |
| Final assets exist | `.svg/.png` |
| README embeds PNG only | scan result |
| Fonts are bound and UI fonts absent | font discovery and scan result |
| Geometry summary persisted | `geometry-summary.txt` fields |
| Rendered PNG inspected | inspected PNG names |

