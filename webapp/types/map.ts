/**
 * Represents the discrete navigation phases of the map.
 *
 * Each phase corresponds to a zoom range and a specific set of visible layers.
 * Advancing to a higher phase pushes a new browser history entry; moving within
 * or descending a phase replaces the current entry in-place.  We keep track
 * of the lat/lng so the user's experience is a smooth "zooming in and out, from
 * broad spatial extent to an individual stream segment".
 *
 * Zoom thresholds differ by region (CONUS vs Alaska) but the phase model is the same:
 *
 * Overview (0)
 *   CONUS zoom < 6 / Alaska zoom < 2
 *   Layers: basemap only. A transparent perimeter overlay captures clicks and
 *   zooms the map to Phase 1 when the user clicks inside the region boundary.
 *
 * WmsHuc (1)
 *   CONUS zoom 6–7 / Alaska zoom 2–3
 *   Layers: HUC-8 choropleth (WMS) + invisible GeoJSON HUC overlay for hover/click.
 *   The user can mouse over watersheds to see names and click one to advance to Phase 2.
 *
 * HucSelected (2)
 *   Same zoom range as WmsHuc, but the map has fitBounds'd to a single HUC-8.
 *   Layers: detailed HUC-8 boundary (GeoJSON) + segment WMS overlay.
 *   The selected HUC id is encoded in the URL so Back restores this view exactly.
 *
 * Segments (3)
 *   CONUS zoom ≥ 8 / Alaska zoom ≥ 4
 *   Layers: individual stream segment GeoJSON fetched by viewport bounds.
 *   Clicking a segment navigates to the segment detail page.
 */
export enum MapPhase {
  Overview = 0,
  WmsHuc = 1,
  HucSelected = 2,
  Segments = 3,
}

export const ALL_MAP_PARAMS = [
  'cp',
  'chuc',
  'clat',
  'clng',
  'ap',
  'ahuc',
  'alat',
  'alng',
] as const
