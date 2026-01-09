import lodash from 'lodash'
const _ = lodash

export default defineNuxtPlugin(nuxtApp => {
  return {
    provide: {
      _,
    },
  }
})
