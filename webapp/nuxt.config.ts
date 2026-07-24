import { metas } from './utils/metas'

// Shown to browsers and users without JavaScript, in place of the app.
// Modeled on ARDAC Explorer (https://github.com/ua-snap/ardac).
const noscriptHtml = `
<style>
  section {
    width: 600px;
    margin: 50px auto;
    font-size: 110%;
    font-family: sans-serif;
    line-height: 1.3;
  }
  li {
    margin-bottom: 0.25rem;
  }
</style>
<section>
  <h1>${metas.title}</h1>

  <p>${metas.description}</p>
  <p>
    ⚠️ We&rsquo;re sorry, but this web tool requires JavaScript to be enabled to
    run. <strong>Please email us at uaf-snap-data-tools@alaska.edu</strong> if
    you would like assistance to access content on this site.
  </p>

  <h3>Content available on this site</h3>
  <ul>
    <li>
      Modeled streamflow projections for stream segments and HUC-8 watersheds
      across the continental United States, based on PRMS (the Precipitation
      Runoff Modeling System, USGS)
    </li>
    <li>
      Streamflow and water temperature projections for Alaska and parts of
      Western Canada, based on RASM (the Regional Arctic System Model)
    </li>
    <li>
      Peak flow, low flow, seasonal averages, and other key hydrologic
      statistics, including range and uncertainty across climate models,
      emissions scenarios, and eras
    </li>
    <li>
      Interactive maps for finding stream segments, with charts and tables
      summarizing projected change for each segment
    </li>
    <li>CSV downloads and API access for full site-specific datasets</li>
  </ul>
  <p>
    The site also includes a how-to guide, a discussion of models and
    uncertainty, and full descriptions of the available data.
  </p>
</section>
`

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  // This app deploys as a static SPA to S3, where unknown URLs are redirected
  // to hashbang URLs and resolved client-side (see README). SSR/SSG payload
  // hydration breaks that flow, so disable it — same approach as ARDAC
  // Explorer (https://github.com/ua-snap/ardac).
  ssr: false,
  nitro: {
    prerender: {
      // With ssr: false these are SPA shells, not rendered pages. Listing
      // them makes each URL exist as an S3 object so direct visits return
      // 200 instead of bouncing through the hashbang redirect.
      routes: [
        '/',
        '/about',
        '/how-to',
        '/models-uncertainty-trust',
        '/data-and-methodology',
      ],
    },
  },
  devtools: { enabled: true },
  css: ['assets/styles/main.scss'],
  pages: true,
  modules: ['@pinia/nuxt'],
  app: {
    head: {
      htmlAttrs: {
        lang: 'en',
      },
      title: metas.title,
      noscript: [
        {
          innerHTML: noscriptHtml,
        },
      ],
      meta: [
        { name: 'description', content: metas.description },
        { property: 'og:title', content: metas.title },
        { property: 'og:description', content: metas.description },
        { name: 'twitter:card', content: 'summary' },
      ],
      link: [
        {
          rel: 'icon',
          type: 'image/x-icon',
          href: '/favicon.ico',
          sizes: '64x64',
        },
        { rel: 'icon', type: 'image/svg+xml', href: '/icon.svg' },
        { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
      ],
      script: [
        {
          src: 'https://umami.snap.uaf.edu/script.js',
          'data-website-id': 'a5a8e5a7-d390-4919-9502-827c2e1f1ac2',
          // Only track visits on the production domain, not development.
          'data-domains': 'futurehydrology.org',
          'data-do-not-track': 'true',
          async: 'true',
          defer: 'true',
        },
      ],
    },
  },
  runtimeConfig: {
    public: {
      snapApiUrl: process.env.SNAP_API_URL || 'https://earthmaps.io',
      geoserverUrl:
        process.env.GEOSERVER_URL || 'https://gs.earthmaps.io/geoserver',
      staticFixtures:
        process.env.HYDROVIZ_USE_STATIC_FIXTURES == 'true' || false,
    },
  },
})
