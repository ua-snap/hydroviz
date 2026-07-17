# Hydroviz Webapp Agentic Coding Guide

Use this guide when generating or editing code for `webapp/` in the Hydroviz
repo. The goal is to produce code that looks native to this codebase rather
than introducing generic Nuxt/Vue patterns. This guide is modeled on the
[ARDAC Explorer agents.md](https://github.com/ua-snap/ardac/blob/main/explorer/agents.md);
where the two repos differ, this document wins.

## Core objective

Match the existing architecture first:

- Nuxt 4 static SPA (`ssr: false`), deployed to S3
- Composition API with `<script lang="ts" setup>`
- TypeScript
- Pinia store (`stores/streamSegment.ts`)
- Bulma + project SCSS
- Leaflet / Plotly / autocomplete.js exposed via client-only Nuxt plugins

Optimize for consistency with existing code over introducing new abstractions.

## Development environment setup

Always set up the environment the same way before running or verifying
anything. All commands run from the `webapp/` directory.

### 1. Node version

Use the Node version pinned for this project:

```bash
nvm use lts/jod
```

This matches `.nvmrc` (Node 22) and the `engines` field in `package.json`.
Do not develop or build against other Node versions.

### 2. Install dependencies

```bash
npm install
```

### 3. Choose a data source (environment variables)

Data-source behavior is controlled entirely by environment variables read in
`nuxt.config.ts` (`runtimeConfig.public`). Pick one mode before starting the
dev server:

**Static-only local development** (no API required; uses fixtures bundled in
`assets/fixtures/`):

```bash
export HYDROVIZ_USE_STATIC_FIXTURES=true
```

**Development against a backend API** (local or remote; defaults to
`https://earthmaps.io` if unset):

```bash
export SNAP_API_URL=https://earthmaps.io
```

`GEOSERVER_URL` may also be set to point at a non-default GeoServer
(defaults to `https://gs.earthmaps.io/geoserver`).

Do not hardcode API or GeoServer URLs in code — always read them from
`runtimeConfig.public` (`snapApiUrl`, `geoserverUrl`, `staticFixtures`).

### 4. Run the dev server

```bash
npm run dev
```

### 5. Preview a production (static) build

```bash
npm run generate
npx serve .output/public
```

### Deployment cautions

Deployment (S3 sync, S3 website configuration, CloudFront invalidation) is a
human-driven process documented in `README.md`. Do not run `aws` commands
unless explicitly asked. In particular, never run the `aws s3 website`
bucket-setup command against an existing bucket — it wipes out the S3 website
redirection rules that report permalinks depend on.

## Manual testing locations

When verifying changes to report pages, charts, maps, or stats tables, do not
pick arbitrary stream segment IDs — use the known-good locations below (from
[issue #220](https://github.com/ua-snap/hydroviz/issues/220)). They cover the
distinct report variants the app renders, so exercise every case relevant to
the change. URLs assume the dev server at `http://localhost:3000`.

**Baseline CONUS + Alaska pair for any report-page change** — always check
both domains, since components are paired (see the CONUS / Alaska split rule):

- Low-flow stream: `/conus/stream/32174` and `/alaska/stream/81015240`

**Special report variants:**

- HUC outflow segments: `/conus/stream/33364` and `/alaska/stream/81014439`
- Stream with a USGS gage (CONUS): `/conus/stream/52448`
- Alaska streams with gage links: `/alaska/stream/81000404`,
  `/alaska/stream/81001685`, `/alaska/stream/81002548`,
  `/alaska/stream/81003397`, `/alaska/stream/81005122`

**More CONUS options:** a larger curated set of test streams — organized by
ecoregion, with GNIS names, USGS gage IDs, and notes — lives in
[`data/tests/test_streams.json` on the `add_test_suite` branch](https://github.com/ua-snap/hydroviz/blob/add_test_suite/data/tests/test_streams.json).
Use it when a change needs coverage across varied geography or gage
configurations.

Guidelines:

- For changes touching gage-related UI, test at least one gaged and one
  ungaged segment.
- For changes touching flow visualizations or stats, include the low-flow
  segments — they surface edge cases (near-zero values, sparse data) that
  average streams do not.
- For map or segment-styling changes, include a HUC outflow segment, since
  outflow segments are colored/styled differently.

## Non-negotiable style rules

- Honor `.prettierrc` (no semicolons, single quotes, 2-space indent, ES5
  trailing commas, no parens on single-arg arrows).
- Use `<script lang="ts" setup>` in components. Do not use the Options API.

## Architectural rules

### 1) Respect the static-SPA routing model

This app deploys as a fully static SPA. Unknown URLs on S3 redirect to
hashbang URLs (`/#!/...`) which `middleware/hashbangRedirect.global.ts`
resolves client-side.

- Do not enable SSR or SSG payload hydration.
- When adding a top-level page, also add its route to the
  `nitro.prerender.routes` list in `nuxt.config.ts` so direct visits return
  200 from S3 instead of bouncing through the hashbang redirect.
- Rely on Nuxt file-based routing under `pages/`; report pages live at
  `pages/conus/stream/[segment].vue` and `pages/alaska/stream/[segment].vue`.

### 2) Keep pages thin; let the store do the work

Pages are light orchestration layers that compose components. Shared state,
remote fetching, and fixture handling belong in
`stores/streamSegment.ts` (`useStreamSegmentStore`), which follows the setup
pattern:

- `defineStore('name', () => { ... })`
- state in `ref(...)` / `shallowRef(...)` (use `shallowRef` for large data
  payloads)
- small async functions for fetch / transform operations
- honor `staticFixtures` mode: every remote fetch must have a fixture
  branch that imports from `assets/fixtures/` so the app works with
  `HYDROVIZ_USE_STATIC_FIXTURES=true`
- track `isLoading` / `apiSlow` / `apiFailed` state around fetches

Prefer extending this store over creating a new one with overlapping
responsibility.

### 3) Follow the CONUS / Alaska split

Where content differs between the two model domains, components are paired in
a subdirectory: `components/Report/{Conus,Alaska}.vue`,
`components/StatsTable/{Conus,Alaska}.vue`,
`components/Citations/{Conus,Alaska}.vue`. When adding domain-specific
behavior, follow this pattern; branch on the store's `segmentRegion` the way
existing code does. Do not fork shared components into near-duplicates when a
small conditional will do.

### 4) Use plugins to expose third-party libraries

Browser-heavy libraries (Leaflet, Plotly, autocomplete.js, lodash) are exposed
through Nuxt plugins in `plugins/` (client-only where needed) and consumed via
`useNuxtApp()`. Do not import these libraries directly in components or invent
a parallel wrapper pattern.

## File placement rules

- **Pages**: `pages/` (file-based routing)
- **Components**: `components/`, PascalCase; domain-paired components in a
  subdirectory (see above)
- **Charts**: `components/Viz/` — Plotly-based; reference existing chart
  components extensively to keep the same code style (trace construction,
  layout, labels, footer explainer text)
- **Shared state / fetching**: `stores/streamSegment.ts`
- **Stateless helpers**: `utils/` (`chart.ts`, `map.ts`, `general.ts`,
  `metas.ts`) — if logic needs reactive state or network calls, it belongs in
  the store instead
- **Types**: `types/` (`map.ts`, `modelsScenarios.ts`, `statsVars.ts`)
- **Route middleware**: `middleware/` (global middleware uses the
  `.global.ts` suffix)
- **Fixtures**: `assets/fixtures/`

## Component conventions

- `const props = defineProps<...>()`
- `const store = useStreamSegmentStore()`
- `computed(...)`, `watch(...)`, `onMounted(...)` / `onUnmounted(...)`
- `NuxtLink` for internal navigation
- Explicit `v-if` / `v-else` conditional rendering
- Prefer existing Bulma/project class patterns; avoid one-off classes or
  inline styles. Project SCSS lives in `assets/styles/`.
- Plain, semantic HTML; always include meaningful `alt` text on images unless
  purely decorative

## Naming rules

- Components: PascalCase
- Store: `useStreamSegmentStore` pattern (`useXStore`)
- Terminology: use "gage" (not "gauge") for USGS gage references
- Variables / functions: plain TS naming; clear nouns and verbs over clever
  names

## What not to do

- Do not switch to the Options API
- Do not enable SSR or add server-side code paths
- Do not add a new CSS framework or write one-off styling, use the framework (Bulma) everywhere possible
- Do not bypass `runtimeConfig` with hardcoded URLs or env reads in components
- Do not add remote fetches without a static-fixtures branch
- Do not move shared map/chart/data logic out of the store or `utils/` into
  individual components
- Do not run deployment or AWS commands unless explicitly asked

## Golden rule

When in doubt, copy an existing nearby pattern from this repo and make the
smallest possible change that fits naturally into the static-SPA model, the
single-store data flow, and the CONUS/Alaska component split.
