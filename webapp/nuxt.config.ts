export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  css: ['assets/styles/main.scss'],
  pages: true,
  modules: ['@pinia/nuxt'],
  runtimeConfig: {
    public: {
      snapApiUrl: process.env.SNAP_API_URL || 'https://earthmaps.io',
      geoserverUrl:
        process.env.GEOSERVER_URL || 'https://gs.earthmaps.io/geoserver',
      staticFixtures: process.env.HYDROVIZ_USE_STATIC_FIXTURE || false,
    },
  },
})
