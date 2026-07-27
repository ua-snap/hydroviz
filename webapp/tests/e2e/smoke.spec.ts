import { test, expect } from '@playwright/test'
import {
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
  await mockMapServices(page, url => {
    // The gage-id WFS query gets one fake CONUS result; the other three
    // autocomplete queries (HUCs, Alaska gages) fall through to empty.
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
  await page.locator('#search').pressSequentially('01234567')
  await page.getByText('Test Creek (01234567)').click()

  await expect(page).toHaveURL(/\/conus\/stream\/32174/)
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
