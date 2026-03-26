import Plotly from 'plotly.js/lib/core'
import scatter from 'plotly.js/lib/scatter'
import box from 'plotly.js/lib/box'
Plotly.register(scatter)
Plotly.register(box)

export default defineNuxtPlugin(nuxtApp => {
  return {
    provide: {
      Plotly,
    },
  }
})
