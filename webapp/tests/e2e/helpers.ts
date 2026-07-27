import fs from 'node:fs'
import path from 'node:path'
import type { Page } from '@playwright/test'

// The dev server runs without HYDROVIZ_USE_STATIC_FIXTURES so that data API
// requests actually hit the network, where these helpers intercept them.
// Happy-path tests are fulfilled with the same fixture JSON the app bundles
// in assets/fixtures/; the failure test fulfills with a 500 instead. This
// keeps every test deterministic and offline while still exercising the real
// fetch/loading/error code paths in stores/streamSegment.ts.

const fixturePath = (name: string) =>
  path.join(process.cwd(), 'assets', 'fixtures', name)

const emptyFeatureCollection = JSON.stringify({
  type: 'FeatureCollection',
  features: [],
})

// 1x1 transparent PNG, served in place of map tiles.
const transparentPng = Buffer.from(
  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',
  'base64'
)

// Serve the bundled example fixture for hydroviz data API requests so report
// pages render deterministically. The fixture is the same for every segment
// id, so tests must assert on structure/visibility, not data values.
export const mockHydrovizApi = async (page: Page) => {
  await page.route('**/*_hydrology/hydroviz/**', route => {
    const fixture = route.request().url().includes('arctic_hydrology')
      ? 'alaska_output_example.json'
      : 'conus_output_example.json'
    route.fulfill({
      contentType: 'application/json',
      body: fs.readFileSync(fixturePath(fixture), 'utf-8'),
    })
  })
}

// Fail hydroviz data API requests so the store's apiFailed branch runs.
export const mockHydrovizApiFailure = async (page: Page) => {
  await page.route('**/*_hydrology/hydroviz/**', route => {
    route.fulfill({ status: 500, body: 'Internal Server Error' })
  })
}

// Answer GeoServer WFS queries with an empty FeatureCollection (or a
// test-supplied response) and all map tile requests with a transparent PNG,
// so Leaflet maps and search autocomplete settle without the network.
export const mockMapServices = async (
  page: Page,
  wfsResponder?: (url: string) => object | undefined
) => {
  await page.route('**/geoserver/**', route => {
    const url = route.request().url()
    if (url.includes('GetFeature')) {
      const custom = wfsResponder?.(url)
      return route.fulfill({
        contentType: 'application/json',
        body: custom ? JSON.stringify(custom) : emptyFeatureCollection,
      })
    }
    return route.fulfill({ contentType: 'image/png', body: transparentPng })
  })
  await page.route('**/basemap.nationalmap.gov/**', route =>
    route.fulfill({ contentType: 'image/png', body: transparentPng })
  )
}
