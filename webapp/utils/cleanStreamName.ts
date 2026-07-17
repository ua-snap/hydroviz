/**
 * Cleans stream names that may have been mangled by shapefile processing.
 * 
 * Issue: Shapefiles (DBF format) have problems with apostrophes and quotes.
 * Names like "L'Anguille River" can become "'''Anguille River'" or similar.
 * 
 * This function:
 * 1. Strips leading/trailing quotes (single and double)
 * 2. Replaces doubled single quotes ('') with single quotes (')
 * 3. Handles edge cases with mixed quotes
 * 
 * @param name - The potentially mangled stream name
 * @returns The cleaned stream name
 */
export function cleanStreamName(name: string | null | undefined): string {
  if (!name) {
    return ''
  }

  let cleaned = name.trim()

  // Strip leading and trailing quotes (both single and double)
  // Do this multiple times to handle nested quotes
  for (let i = 0; i < 3; i++) {
    const before = cleaned
    cleaned = cleaned.replace(/^["']+/, '').replace(/["']+$/, '')
    if (cleaned === before) break
  }

  // Replace doubled single quotes with single quotes
  // (CSV/DBF escaping pattern)
  cleaned = cleaned.replace(/''/g, "'")

  // Replace doubled double quotes with single double quotes
  cleaned = cleaned.replace(/""/g, '"')

  return cleaned
}
