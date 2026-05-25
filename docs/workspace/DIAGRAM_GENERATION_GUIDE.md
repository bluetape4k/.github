# README Diagram Generation Guide

Date: 2026-05-25
Scope: bluetape4k workspace README diagrams and benchmark chart imagery

This is the canonical organization-wide generation guide for README visual
assets across the bluetape4k workspace. Keep generation rules here instead of
scattering them through PR notes, lessons, website pages, or per-repo scripts.

## Skill Usage And Sync

- Use `$bluetape4k-diagram` for any bluetape4k README diagram work, including
  architecture, sequence, class/UML, ERD, flow, topology, Mermaid/ASCII
  conversion, and benchmark chart imagery.
- When this guide changes, update the `bluetape4k-diagram` skill in the same
  change for both Codex and Claude:
  - `~/.codex/skills/bluetape4k-diagram/SKILL.md`
  - `~/.claude/skills/bluetape4k-diagram/SKILL.md`
  - managed chezmoi sources under `private_dot_codex/private_skills/` and
    `private_dot_claude/private_skills/`
- When `$bluetape4k-diagram` changes for workspace-wide behavior, update this
  `.github/docs/workspace/DIAGRAM_GENERATION_GUIDE.md` guide as the canonical
  source.

## Goal

Replace Mermaid and ASCII diagrams in README files with deterministic,
professional pastel infographic assets. README files embed PNGs for stable
GitHub rendering, while matching SVG sources stay in the repository for review,
reuse, and regeneration.

Generated diagrams must not look like recolored Mermaid output. Diagram type
must drive the layout, geometry, labels, and connector semantics.

## Review Escalation Rule

- Treat repeated human review findings as mandatory rules, not suggestions.
- If the same defect category is pointed out more than once in a diagram batch
  or project, promote it immediately into generator validation, batch checklist,
  and skill/reference guidance.
- Do not keep relying on manual visual review for repeated defects. Add
  deterministic checks where practical, for example Graphviz route evidence,
  connector-interior intersection checks, text overflow checks, inheritance
  endpoint checks, and README image-link checks.
- Future batches must apply escalated rules before preview. A batch is not ready
  for review while a known repeated defect class is unchecked.

## Output Contract

- Generate both `.svg` and `.png` for every README diagram.
- Embed only `.png` in README files.
- Keep the matching `.svg` next to the PNG.
- Store README diagram assets under `docs/images/readme-diagrams/` unless a
  repo-local rule requires root README assets under `docs/assets/`.
- Store benchmark chart assets under `docs/images/readme-charts/`.
- Use English text inside all generated images, including images embedded in
  localized README files.
- Do not generate localized diagram variants by default. Share the same
  English-label PNG/SVG assets across localized README files.
- Use content-driven SVG dimensions. Do not force every diagram into one fixed
  aspect ratio.
- Treat current source code as the authority for class/API diagrams. Recovered
  Mermaid history is a source, not proof.

## Workflow

1. Confirm diagram type and README placement.
2. Gather source truth from the latest checked-out source code, README text,
   existing diagram assets, and qmd-retrieved lessons or specs when relevant.
3. Before drawing, read the concrete source files that own the displayed
   classes, tables, repositories, controllers, configuration, or workflows. Do
   not infer relationships from file names, stale Mermaid, prior generated
   images, or memory.
4. For exposed-workshop, broad rewrites, or 4-5 item review batches, load the
   `bluetape4k-diagram` reference
   `references/exposed-workshop-batch-review-lessons.md` before drawing.
5. Convert Mermaid/ASCII into a visual model, not into a recolored Mermaid
   render.
6. Create or update SVG source.
7. Render a matching PNG.
8. Update README files to embed PNG only.
9. Re-check source drift against the latest source before previewing or asking
   for review.
10. Validate links, SVG parsing, PNG rendering, source drift, and visual sanity.

## Source Priority

1. Current source code and public APIs.
2. Current README text and examples.
3. Existing SVG/PNG assets when they are visually sound and concept-equivalent.
4. Recovered Mermaid or ASCII history from git.

If a recovered diagram mentions removed, renamed, deprecated, or internal-only
APIs, rebuild the model from current source or drop the stale element.

For repository/module diagrams, inspect the current implementation files that
own each displayed relationship. For example, a repository box may depend on
several tables, DAO entities, transaction APIs, or mapper records; do not show
only the most obvious table unless the source proves that is the only
dependency.

## Asset Naming And Embeds

- Use lowercase kebab-case filenames that describe the subject and diagram type,
  for example `advanced-workflow-architecture.svg` and
  `tenant-isolation-sequence.png`.
- Treat SVG as the source of truth and PNG as the rendered README artifact.
- Keep each PNG beside its matching SVG.
- Embed diagrams with normal Markdown image syntax, for example
  `![Architecture](docs/images/readme-diagrams/advanced-workflow-architecture.png)`.
- Do not add separate localized images unless the diagram itself must show
  locale-specific domain terms. Prefer one shared English-label asset across all
  localized README files.

## Generation Tools

- Prefer existing repo-local diagram/chart generators when they exist.
- For hand-authored SVG, keep the SVG readable enough for review and
  regeneration.
- Graphviz layout and routing evidence is mandatory for README diagrams with
  nodes and connectors.
- Generate Graphviz `.dot`, `.plain`, and sketch `.svg` artifacts before drawing
  final hand-authored SVG routes.
- Parse or inspect Graphviz `.plain` edge paths and use them to choose ranks,
  ports, side entry/exit, and orthogonal lanes.
- Final generators must fail when a major architecture/UML/ERD/flow connector
  lacks a corresponding Graphviz edge route, unless the exception is documented
  in the generator.
- D2 may still be used as a secondary sketch helper, but it does not replace
  required Graphviz layout and routing evidence.
- Final SVG may deviate from Graphviz only to improve typography, UML/ERD
  semantics, or boundary attachment. Do not replace a short Graphviz
  side-to-side route with a long U-shaped detour or extra bends.
- Do not use Graphviz or D2 output as the final README asset. Keep the final SVG
  hand-authored so typography, shapes, routing, UML/ERD semantics, and review
  feedback remain intentional.
- Render PNG with the first available project-appropriate tool:
  `rsvg-convert`, `sharp`, `magick`, or Playwright screenshot. Use the repo's
  established tool if it has one.
- Do not use screenshots of Mermaid output as final artifacts.
- Validate generated dimensions and visual framing after rendering, not only
  SVG syntax.

## README Placement

- Place architecture/module diagrams near the top, usually after overview or key
  features and before detailed usage examples.
- Place class diagrams near API, repository, domain model, or type hierarchy
  sections.
- Place sequence diagrams near workflow, request lifecycle, transaction flow,
  cache pattern, or operation sections.
- Place ERDs near schema/domain-model sections, before query examples that rely
  on the relationships.
- Place benchmark charts next to the measured result table they summarize.
- Keep a final `Diagrams` section only for explicit diagram galleries or whole
  document summaries.

## Shared Visual Language

- Background: near-white canvas, white rounded outer frame, subtle blue-gray
  border.
- Palette: pastel blue, green, amber, pink, teal, lavender, and soft neutral
  gray. Avoid dark one-note palettes.
- Typography:
  - Use `Architects Daughter` for title, actor, class/table name, panel label,
    and prominent component text.
  - Use `Comic Mono` for details, captions, member lists, columns, constraints,
    and compact annotations.
- Keep all text inside containers. Shorten English labels before shrinking text.
- Title text must fit the canvas. Move parenthetical detail into the subtitle or
  omit it.
- Component text must be vertically centered inside cards.
- Relationship labels may use small white pill backgrounds to avoid line
  collisions.
- Use semantic stroke colors when connector families overlap or share a lane;
  keep the legend implicit through consistent use, not decorative color noise.
- Connector paths must have a visible stem. A marker-only arrowhead is failed
  rendering even when the SVG is syntactically valid.
- Do not use decorative orbs, bokeh, fake 3D, stock imagery, or gradient-only
  backgrounds.

## Architecture And Flow Diagrams

Use layered architecture as the default structure. Prefer compact grouped cards,
layer bands, or panel composition rather than generic Mermaid boxes.

- Default to layered architecture when the system can be explained by
  presentation/API, application/service, domain, infrastructure, data, and
  external-system layers.
- Prefer 4-8 prominent groups for large diagrams.
- Size groups by item count. Do not stretch every section to equal height.
- Prefer chapter-12-style panel composition when comparing frameworks, adapters,
  runtimes, or example variants: large stack/runtime panels with internal
  component cards, local arrows inside panels, and a compact shared band below.
- For component architecture, keep cards close enough to read the flow but leave
  visible connector stems between card boundaries.
- Use semantic shapes for architecture nodes: databases as cylinders with enough
  cap/body height for labels, OpenAPI/external APIs as visually distinct
  endpoint/client cards or icon-badged components, and runtime/application pieces
  as normal components.
- Architecture diagrams must explain source-derived relationships, not merely
  list boxes in a table. Read controllers, repositories, configuration, tables,
  and runtime adapters before choosing nodes and arrows.
- Use filled triangular arrowheads by default:
  `markerWidth=9`, `markerHeight=9`, `refX=8`, `refY=4.5`, path
  `M1,1 L8,4.5 L1,8 Z`.
- Use right-angled orthogonal connector paths by default. Avoid arbitrary
  diagonal/cubic curves unless they clearly improve readability.
- Omit hub-to-group connector lines when they create a hairball. Grouping can
  carry structure when explicit lines reduce readability.
- Root README module structure may use a software stack layout: foundation,
  core libraries, integrations, applications/examples.

Prompt shape:

> Create a pastel technical infographic from this architecture diagram. Do not
> imitate Mermaid. Use readable layer bands, compact grouped cards, filled
> triangular arrowheads, right-angled orthogonal connectors, English labels,
> Architects Daughter for large labels, and Comic Mono for details.

## Component Placement

- Prefer balanced whitespace over rigid symmetry.
- Place related cards near their actual relationship cluster.
- Avoid huge empty quadrants and over-wide single-row pipelines.
- In dense diagrams, use local buses or shared lanes instead of drawing every
  dependency as a long center-crossing curve.
- Card connectors must span the visible gap between cards, not only the midpoint
  of the gap.
- Connector endpoints must sit on component boundaries. Lines must not start
  inside a card, table, class, cylinder, or panel unless the source element is
  intentionally a nested port.
- Orthogonal routes should use the nearest readable side-to-side path before
  introducing long detours. Prefer moving components over accepting a tangled
  route.
- If Graphviz produces a direct side-to-side or bottom-to-top route for the same
  relationship, treat longer manual detours as defects unless they avoid a real
  component crossing.
- Move components to avoid line overlap before adding complex routing. Layout is
  part of the diagram model, not a cosmetic afterthought.
- Do not delete source-meaningful connectors merely because the route is
  complex. First change placement, then use Graphviz-like orthogonal lanes, local
  buses, section lanes, and semantic stroke colors.
- Omit a connector only when it adds no source or semantic value because
  grouping, labels, or source naming already prove the relationship.
- When multiple semantic connector families share space, use distinct lanes and
  distinct stroke colors so the viewer can track each relationship.
- Typical color families: inheritance/generalization = dark gray, FK/table
  relations = teal, DTO/domain mapping = green, repository/use calls = blue,
  runtime/session = purple, external/database/client = orange, converter/mapper
  = pink.

## Class Diagrams

Render class diagrams as UML diagrams, not architecture diagrams.

- Use UML compartments: header, fields, operations/notes.
- Use small-radius rectangular boxes (`rx=4`) for class/interface/object boxes.
- Generalization and realization arrows point from child/implementation to
  parent/interface with a hollow triangle at the parent endpoint.
- Generalization and realization connector stems must meet the hollow triangle
  base at 90 degrees. If an SVG marker makes the line appear to enter the
  triangle at 0 degrees or attach to its side, draw the hollow triangle
  explicitly and route the stem to the base center.
- Dependency/use arrows point from the using type to the used type.
- Prefer vertical inheritance trees. Place unrelated collaborators at the sides.
- Place superclasses, interfaces, and abstract bases above concrete
  implementations. Do not place a superclass below its children.
- Do not show factory/metaclass helpers such as companion factory classes unless
  they materially clarify the diagram; omit them when they add clutter.
- Keep vertical spacing wide enough for inheritance stems, superclass members,
  and table columns to remain legible at README zoom.
- Use free placement and orthogonal lanes when it reduces edge overlap.
- Route shared relationships through local buses or section lanes.
- For long class/member names or many member rows, widen the box or limit
  displayed rows before allowing text to overflow its compartment.
- Connector paths must terminate at class box boundaries and must not pass
  through class interiors.
- Verify every displayed class, field, method, and relationship against current
  source before rendering.

Prompt shape:

> Create a pastel UML class diagram. Use UML compartment rectangles. Put class
> and interface names in Architects Daughter and members in Comic Mono. Arrange
> inheritance vertically. Hollow triangle arrows point to the parent class or
> implemented interface.

## Sequence Diagrams

Keep lifelines, but make the visual readable as a sequence infographic.

- Use generous outer margins. Participant headers, first/last messages, and
  notes must not hug the frame.
- Keep internal vertical spacing compact. Labels should sit close to their
  arrows; avoid large gaps between a call arrow and its label.
- Participant header labels must be vertically centered with the same baseline
  logic as architecture cards.
- Lifelines are dashed vertical stems without arrowheads. Do not reuse a
  return-message arrow style for lifelines.
- Messages become numbered rounded horizontal interaction bands with short
  English intent text.
- Use pastel color by interaction kind: request, suspend/work, response.
- Keep dashed return paths sparse. Return messages are dashed arrows, not solid
  calls; show returns only when response behavior matters.
- Render `alt`, `else`, `opt`, and similar conditional branches explicitly,
  with readable branch labels and enough detail to understand each path.
- For `alt` branches, show the guard/condition, the distinct messages inside
  each branch, and branch-specific responses or errors.
- Self-calls must render as small loop arrows. A self-call must never collapse
  into a zero-length path where only the arrowhead remains.
- Do not impose a fixed height limit. Grow the canvas until the sequence and
  notes fit.
- Notes and summaries must not cover the sequence body.
- If a normalized non-English message becomes empty, use participating
  components as the fallback label, for example `S3Client to LocalStack`.

Prompt shape:

> Create a pastel sequence diagram infographic. Keep lifelines, group messages
> into numbered horizontal interaction bands, use generous outer margins,
> compact internal label-to-arrow spacing, and render self-calls as visible loop
> arrows.

## ERD Diagrams

Use table compartments similar to class diagrams.

- Render tables as compartments: table name, key columns, remaining columns,
  constraints/notes.
- Ignore Mermaid config/init blocks. They are renderer configuration, not
  database tables.
- If Mermaid ERDs list only relationships, derive table boxes from relationship
  endpoints.
- FK arrow direction:
  - child table -> parent table
  - bridge table -> each parent table
- FK relationships use filled arrowheads toward the parent table. They must
  remain visually distinct from UML generalization, which uses a hollow
  triangle.
- Show bridge tables as first-class tables for many-to-many relationships.
- Prefer free placement and orthogonal FK routing over uniform table grids.
- Route FK lines to table boundaries at readable angles and keep FK endpoints
  visually distinct from UML inheritance triangle endpoints in hybrid diagrams.
- Use named FK lanes for repeated parent references such as `tenantId`,
  `clinicId`, or `appointmentId`.
- Connector paths must terminate at table boundaries and must not pass through
  table compartments.
- In hybrid ERD/UML/domain diagrams, keep FK lines inside the table cluster and
  keep UML inheritance inside the class cluster. Do not draw table-to-entity
  mapping lines unless they add necessary meaning; table and entity names often
  make the mapping clear enough.

Prompt shape:

> Create a pastel ERD using table compartments. Use table names in Architects
> Daughter and columns/constraints in Comic Mono. Show primary keys, foreign
> keys, unique constraints, and cardinality labels. FK arrows point from child
> or bridge table to parent tables.

## ASCII Diagram Conversion

Treat ASCII diagrams as source material, not final README content.

- Convert architecture, flow, sequence, ERD, decision-tree, and topology ASCII
  blocks to SVG/PNG assets.
- Leave project directory trees as code blocks unless they are being used as a
  conceptual diagram.
- Reuse an existing concept-equivalent PNG/SVG pair before generating a new
  asset.
- When converting localized ASCII diagrams, normalize labels to concise English
  inside the image and keep surrounding README prose localized.
- Replace ASCII code fences with PNG image links near the same section.

## Benchmark Charts

Benchmark result visuals are charts, not diagrams.

- Use charts only for tables with explicit numeric measurements.
- Preserve measured Markdown tables as the source of truth.
- Choose chart shape from metric shape:
  - ranking/top-N throughput: horizontal bar chart
  - latency by operation: grouped horizontal bars
  - environment or payload-size comparison: grouped bars
  - time-series history: line chart
- Show unit and direction: `higher is better` for throughput, `lower is better`
  for latency.
- Use log scale when values differ by orders of magnitude, and label it.

## Validation Commands

Use repo-local scripts first. If none exist, use small targeted checks:

```bash
find docs/images/readme-diagrams -name '*.svg' -print0 | xargs -0 -n1 xmllint --noout
find docs/images/readme-diagrams -name '*.svg' -exec sh -c 'test -f "${1%.svg}.png"' sh {} \;
rg 'docs/images/readme-diagrams/.*\.svg' README*.md && exit 1 || true
git diff --check
```

## Approved Samples

| Kind | PNG | SVG |
|---|---|---|
| Architecture modules | [`projects-module-sample-5-contact-sheet.png`](./projects-module-sample-5-contact-sheet.png) | source assets live in target repos |
| Architecture roots | [`sample-5-contact-sheet.png`](./sample-5-contact-sheet.png) | source assets live in target repos |
| Class diagram | [`class-diagram-style-v3-sample.png`](./class-sequence-style/class-diagram-style-v3-sample.png) | [`class-diagram-style-v3-sample.svg`](./class-sequence-style/class-diagram-style-v3-sample.svg) |
| Sequence diagram | [`sequence-diagram-style-sample.png`](./class-sequence-style/sequence-diagram-style-sample.png) | [`sequence-diagram-style-sample.svg`](./class-sequence-style/sequence-diagram-style-sample.svg) |
| ERD | [`blog-schema-erd-style-sample.png`](./erd-style/blog-schema-erd-style-sample.png) | [`blog-schema-erd-style-sample.svg`](./erd-style/blog-schema-erd-style-sample.svg) |

## Validation Checklist

Before review or PR:

- README image links touched by the work resolve: `missing=0`.
- README files do not embed local `docs/images/readme-diagrams/*.svg` links.
- Every new SVG parses as XML.
- Every new SVG has a rendered PNG.
- Diagram-like ASCII fences are gone unless they are intentional project
  structure listings.
- Architecture diagrams have visible connector stems and no marker-only arrows.
- Architecture diagrams use filled triangular arrowheads and right-angled
  orthogonal connector paths unless an explicit exception improves readability.
- Architecture diagrams default to a layered architecture layout when the
  subject supports it.
- Architecture diagrams use semantic shapes for databases, external APIs, and
  runtime/application components; database labels do not collide with cylinder
  caps.
- Graphviz/D2 layout sketches were used for dense topology, inheritance, ERD, or
  repeated-routing diagrams, and the final SVG was still hand-authored.
- Source-meaningful connectors were not deleted only to reduce visual
  complexity; overlaps are handled by placement, routing, lanes, or semantic
  color separation.
- Sequence diagrams pass:
  - generous outer margin check
  - compact label-to-arrow spacing check
  - participant header baseline check
  - lifelines have no arrowheads
  - return messages use dashed arrows, not solid calls
  - zero-length self-call check
  - explicit `alt` / `else` / `opt` branch rendering when conditional behavior
    exists
- Class and ERD diagrams have no connector path through box/table interiors.
- Class and ERD text fits inside compartments; long member lists are widened,
  wrapped, or intentionally summarized.
- UML generalization/realization stems meet hollow triangle bases at 90 degrees,
  with superclass/interface targets above concrete children.
- Hybrid ERD/UML diagrams keep FK, inheritance, dependency, and DTO mapping
  lines visually distinct by endpoint shape, line style, lane, or color.
- Source drift checks pass for deprecated APIs, removed classes, stale field
  names, and relationship directions.
- For 4-5 item review batches, inspect each rendered PNG one by one before
  asking for review; do not rely only on contact sheets or SVG syntax.
- Visual sanity check passes at README scale and contact-sheet scale:
  - no clipped text
  - no overlapping labels
  - no huge blank regions
  - no dense edge hairballs
  - no notes covering sequence bodies
- `git diff --check` is clean.

Only claim completion after link validation, generated asset validation, and
visual validation all pass.
