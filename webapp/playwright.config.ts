import { defineConfig, devices } from '@playwright/test'

// End-to-end smoke tests. By default, all external services (hydroviz data
// API, GeoServer, basemap tiles) are mocked per-test via page.route — see
// tests/e2e/helpers.ts — so the suite is deterministic and runs offline.
//
// Live mode runs the same tests against the real external services:
//   HYDROVIZ_E2E_LIVE=true npm run test:e2e
// To also target a deployed site instead of the local dev server (implies
// live mode):
//   HYDROVIZ_E2E_BASE_URL=https://example.com npm run test:e2e
const deployedBaseUrl = process.env.HYDROVIZ_E2E_BASE_URL
const liveMode = process.env.HYDROVIZ_E2E_LIVE === 'true' || !!deployedBaseUrl

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? [['list'], ['html']] : 'list',
  // The live data API can take a minute per report request, so live mode
  // needs far longer timeouts. In mock mode, Nuxt dev compiles routes on
  // demand, so first paint of a heavy report page (Plotly) can still exceed
  // the 5s expect default.
  timeout: liveMode ? 180_000 : 30_000,
  expect: { timeout: liveMode ? 90_000 : 15_000 },
  use: {
    baseURL: deployedBaseUrl || 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
  // When targeting a deployed site, don't start a local dev server.
  webServer: deployedBaseUrl
    ? undefined
    : {
        command: 'npm run dev',
        url: 'http://localhost:3000',
        reuseExistingServer: !process.env.CI,
        timeout: 120_000,
      },
})
