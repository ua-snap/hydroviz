// Redirect S3 hashbang URLs to Nuxt URLs.
//
// S3 static website hosting can't serve our client-side routes directly, so
// bucket redirection rules rewrite unknown/error URLs to hashbang URLs (e.g.
// /conus/stream/5 -> /#!/conus/stream/5) that resolve to index.html (see
// README). This middleware routes them back to the intended page during the
// initial navigation. Adapted from:
// https://via.studio/journal/hosting-a-reactjs-app-with-routing-on-aws-s3
export default defineNuxtRouteMiddleware(to => {
  const path = (/^#!(\/.*)$/.exec(to.hash) || [])[1]
  if (path) {
    return navigateTo(path, { replace: true })
  }
})
