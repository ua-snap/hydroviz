import { defineConfig, devices } from '@playwright/test'

// End-to-end smoke tests. All external services (hydroviz data API,
// GeoServer, basemap tiles) are mocked per-test via page.route — see
// tests/e2e/helpers.ts — so the suite is deterministic and runs offline.
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? [['list'], ['html']] : 'list',
  // Nuxt dev compiles routes on demand, so first paint of a heavy report
  // page (Plotly) can exceed the 5s default.
  expect: { timeout: 15_000 },
  use: {
    baseURL: 'http://localhost:3000',
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
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
})
