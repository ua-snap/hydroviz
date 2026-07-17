# Fix for Mysterious Apostrophes in Stream Names

## Issue
Stream names with apostrophes (like "L'Anguille River") were being mangled to display as "'''Anguille River'" due to shapefile DBF format issues with quote escaping.

## Solution Overview
This fix has two components:

### 1. Data Preprocessing Fix (Primary)
The `data/preprocess/shp/simplify_segments.ipynb` notebook now includes a `clean_stream_name()` function that:
- Strips leading/trailing quotes
- Replaces doubled apostrophes (`''`) with single apostrophes (`'`)
- Handles nested quotes and mixed quote types

**To apply this fix to the shapefile data:**
1. Run the `simplify_segments.ipynb` notebook to regenerate the shapefiles
2. Deploy the updated shapefiles to GeoServer:
   - `seg_h8_outlet_stats_simplified.shp` (Data API)
   - `seg_h8_outlet_stats_simplified_subset.shp` (webapp)

### 2. Webapp Fix (Backup/Defensive)
The webapp now includes a `cleanStreamName()` utility function in `webapp/utils/cleanStreamName.ts` that cleans names as they're displayed. This provides immediate relief and serves as a backup if the shapefile data isn't regenerated.

## Files Changed
- `webapp/utils/cleanStreamName.ts` - New utility function
- `webapp/utils/map.ts` - Apply cleaning to map tooltips
- `data/preprocess/shp/simplify_segments.ipynb` - Clean names before writing shapefile

## Testing
The cleaning function correctly handles:
- `'''Anguille River'` → `Anguille River`
- `''L''Anguille River''` → `L'Anguille River`
- `"'Test'"` → `Test`
- Regular names without quotes remain unchanged

## Deployment Notes
The webapp fix is deployed automatically and will immediately clean any mangled names in tooltips. For a complete fix, the shapefiles should be regenerated using the updated notebook and redeployed to GeoServer.
