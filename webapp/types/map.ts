/**
 * Represents the discrete navigation phases of the map.
 *
 * Each phase pins the map to a fixed zoom level (or, for Phase 2, fitBounds to
 * the selected HUC) and owns a specific set of visible layers. Each phase
 * function in Map.vue is the single source of truth for that phase's layers and
 * zoom — there is no zoom-driven conditional layer management.
 *
 * The URL is the source of truth for which phase is active. Forward navigation
 * (clicking the perimeter to enter Phase 1, clicking a HUC to enter Phase 2)
 * pushes a new browser history entry; panning within a phase replaces the
 * current entry in-place with the new center. A watcher re-applies the matching
 * phase whenever the URL changes, so Back/Forward and fresh loads all flow
 * through one path. The saved lat/lng makes the experience a smooth "zooming in
 * and out, from broad spatial extent to an individual stream segment".
 *
 * Zoom levels differ by region (CONUS vs Alaska); the per-phase values
 * (defaultViewZoom, hucSelectZoom, segmentSelectZoom) are defined in Map.vue.
 * The phase model itself is the same across regions:
 *
 * Overview (0)
 *   Zoomed out to defaultViewZoom.
 *   Layers: HUC-8 choropleth (hucWmsLayer) + a transparent perimeter overlay
 *   that captures clicks and advances the map to Phase 1, centered on the click.
 *
 * WmsHuc (1)
 *   Zoomed in to hucSelectZoom.
 *   Layers: HUC-8 choropleth (hucWmsLayer) + invisible simplifiedHucsLayer
 *   (GeoJSON hover/click targets) + faint segWmsLayer stream overlay. The user
 *   can mouse over watersheds to see names and click one to advance to Phase 2.
 *
 * HucSelected (2)
 *   The map fitBounds' to the selected HUC-8, capped at segmentSelectZoom.
 *   Layers: detailed HUC-8 boundary (GeoJSON) + individual stream segments
 *   fetched by viewport bounds; all overview/WMS layers are hidden. The selected
 *   HUC id is encoded in the URL so Back restores this view exactly. Clicking a
 *   segment navigates away to the segment detail page (outside the phase model).
 */
export enum MapPhase {
  Overview = 0,
  WmsHuc = 1,
  HucSelected = 2,
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
