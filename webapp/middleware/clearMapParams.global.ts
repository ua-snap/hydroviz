import { ALL_MAP_PARAMS } from '~/types/map'

const REPORT_PATTERN = /^\/(conus|alaska)\/(stream|huc)\//

export default defineNuxtRouteMiddleware((to) => {
  if (!REPORT_PATTERN.test(to.path)) return

  const hasMapParam = ALL_MAP_PARAMS.some(p => p in to.query)
  if (!hasMapParam) return

  const query = { ...to.query }
  ALL_MAP_PARAMS.forEach(p => delete query[p])
  return navigateTo({ ...to, query }, { replace: true })
})
