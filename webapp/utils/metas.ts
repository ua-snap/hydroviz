// Canonical site title and description, shared by the social media preview
// tags and the noscript fallback content in nuxt.config.ts.
export const metas = {
  title: 'Hydrologic Outlooks',
  description:
    'Interactive maps, charts, and data downloads of modeled hydrologic projections — streamflow, peak and low flows, and water temperature — for streams and watersheds across the continental United States, Alaska, and Western Canada.',
  // TODO: once the production domain is finalized, add a social preview image
  // here as an absolute URL (social media scrapers cannot resolve relative
  // paths) and add og:image / twitter:image tags in nuxt.config.ts.
}
