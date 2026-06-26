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
