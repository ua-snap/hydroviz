import Plotly from 'plotly.js/lib/core'

import scatter from 'plotly.js/lib/scatter'
import box from 'plotly.js/lib/box'
import scatterpolar from 'plotly.js/lib/scatterpolar'

Plotly.register(scatter)
Plotly.register(box)
Plotly.register(scatterpolar)

export default defineNuxtPlugin(nuxtApp => {
  return {
    provide: {
      Plotly,
    },
  }
})
