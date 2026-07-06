export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['assets/styles/main.scss'],
  pages: true,
  modules: ['@pinia/nuxt'],
  app: {
    head: {
      htmlAttrs: {
        lang: 'en',
      },
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
          // TODO: replace with the website ID from Umami once the production
          // site is registered there.
          'data-website-id': '00000000-0000-0000-0000-000000000000',
          // Only track visits on the production domain, not development.
          // TODO: replace with the finalized production domain.
          'data-domains': 'hydroviz.snap.uaf.edu',
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
