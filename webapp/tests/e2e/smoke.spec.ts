import { test, expect } from '@playwright/test'
import {
  liveMode,
  mockHydrovizApi,
  mockHydrovizApiFailure,
  mockMapServices,
} from './helpers'

// A small smoke suite covering the highest-value user flows. All external
// services are mocked (see helpers.ts), and the report fixtures return the
// same example data for every segment id — so these tests assert on page
// structure and visibility, never on specific data values.

test('home page renders both region maps', async ({ page }) => {
  const pageErrors: Error[] = []
  page.on('pageerror', error => pageErrors.push(error))
  await mockMapServices(page)

  await page.goto('/')

  await expect(
    page.getByRole('heading', { name: 'Hydrologic Outlooks' })
  ).toBeVisible()
  await expect(
    page.getByRole('heading', { name: 'Continental United States' })
  ).toBeVisible()
  await expect(
    page.getByRole('heading', { name: 'Alaska', exact: true })
  ).toBeVisible()

  expect(pageErrors).toEqual([])
})

test('CONUS report renders stats and charts', async ({ page }) => {
  await mockMapServices(page)
  await mockHydrovizApi(page)

  await page.goto('/conus/stream/32174')

  await expect(
    page.getByRole('heading', { name: /Statistics for/ })
  ).toBeVisible()
  // Loading state has resolved.
  await expect(page.locator('progress')).toHaveCount(0)
  await expect(page.locator('table').first()).toBeVisible()
  await expect(page.locator('.js-plotly-plot').first()).toBeVisible()
})

test('Alaska report renders stats and charts', async ({ page }) => {
  await mockMapServices(page)
  await mockHydrovizApi(page)

  await page.goto('/alaska/stream/81015240')

  await expect(
    page.getByRole('heading', { name: /Statistics for/ })
  ).toBeVisible()
  await expect(page.locator('progress')).toHaveCount(0)
  await expect(page.locator('table').first()).toBeVisible()
  await expect(page.locator('.js-plotly-plot').first()).toBeVisible()
})

test('data API failure shows the failure message', async ({ page }) => {
  await mockMapServices(page)
  await mockHydrovizApiFailure(page)

  await page.goto('/conus/stream/32174')

  await expect(
    page.getByText(/experiencing technical difficulties/)
  ).toBeVisible()
})

test('searching a gage id navigates to its report', async ({ page }) => {
  // In live mode the autocomplete queries real GeoServer, so search for a
  // real USGS gage (on segment 52448, a known gaged stream per AGENTS.md).
  // In mock mode the gage-id WFS query is served one fake CONUS result and
  // the other three autocomplete queries (HUCs, Alaska gages) fall through
  // to empty.
  const search = liveMode
    ? {
        query: '12161000',
        result: 'South Fork Stillaguamish River (USGS-12161000)',
        reportUrl: /\/conus\/stream\/52448/,
      }
    : {
        query: '01234567',
        result: 'Test Creek (01234567)',
        reportUrl: /\/conus\/stream\/32174/,
      }

  await mockMapServices(page, url => {
    if (url.includes('seg_h8_outlet_stats_simplified_v2')) {
      return {
        type: 'FeatureCollection',
        features: [
          {
            type: 'Feature',
            properties: {
              seg_id_nat: 32174,
              GNIS_NAME: 'Test Creek',
              GAGE_ID: '01234567',
            },
          },
        ],
      }
    }
  })
  await mockHydrovizApi(page)

  await page.goto('/')
  await page.locator('#search').pressSequentially(search.query)
  await page.getByText(search.result).click()

  await expect(page).toHaveURL(search.reportUrl)
  await expect(
    page.getByRole('heading', { name: /Statistics for/ })
  ).toBeVisible()
})

test('static content page loads via direct URL', async ({ page }) => {
  await page.goto('/data-and-methodology')

  await expect(
    page.getByRole('heading', { name: 'Data, Methodology & Bibliography' })
  ).toBeVisible()
})
