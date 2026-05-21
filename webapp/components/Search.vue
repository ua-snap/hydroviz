<script setup lang="ts">
const { $autoComplete, $config, $_ } = useNuxtApp()
const inputValue = ref('')

onMounted(() => {
  let config = {
    selector: '#search',
    placeHolder: 'Search for a stream segment or HUC',
    data: {
      src: async (query: string) => {
        // Escape single quotes for safe use inside CQL string literals
        const safeQuery = query.replace(/'/g, "''")
        const segUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&propertyName=seg_id_nat,GNIS_NAME,GAUGE_ID&cql_filter=GNIS_NAME%20ILIKE%20%27%25${safeQuery}%25%27%20OR%20GAUGE_ID%20ILIKE%20%27%25${safeQuery}%25%27`
        const hucUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Ahuc8_conus_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&propertyName=huc8,name&cql_filter=name%20ILIKE%20%27%25${safeQuery}%25%27%20OR%20huc8%20LIKE%20%27%25${safeQuery}%25%27`

        let items: any[] = []

        try {
          const [segRes, hucRes] = await Promise.all([
            fetch(segUrl).then(res => res.json()),
            fetch(hucUrl).then(res => res.json()),
          ])

          if (segRes && Array.isArray(segRes.features)) {
            segRes.features.forEach((feature: any) => {
              let segIdNat = feature.properties.seg_id_nat
              let gaugeId = feature.properties.GAUGE_ID
              let name = feature.properties.GNIS_NAME
              if (gaugeId && gaugeId !== 'NA') {
                name += ` (ID: ${segIdNat}, ${gaugeId})`
              } else {
                name += ` (ID: ${segIdNat})`
              }
              items.push({
                name: name,
                id: segIdNat,
                category: 'stream segment',
              })
            })
          }

          if (hucRes && Array.isArray(hucRes.features)) {
            hucRes.features.forEach((feature: any) => {
              let hucId = feature.properties.huc8
              let name = `${feature.properties.name} (${hucId})`
              items.push({
                name: name,
                id: hucId,
                category: 'huc',
              })
            })
          }

          items = $_.sortBy(items, ['name'])

          return items
        } catch (error) {
          console.error('Error fetching autocomplete data', error)
          return []
        }
      },
      keys: ['name'],
    },
    resultItem: {
      element: (element: HTMLElement, match: any) => {
        let item = match.value
        element.innerHTML =
          item.name + '<span class="category">' + item.category + '</span>'
      },
    },
    threshold: 3,
    debounce: 200,
  }

  let searchAutoComplete = new $autoComplete(config)

  searchAutoComplete.input.addEventListener('selection', function (event) {
    let selection = event.detail.selection.value
    let id = selection.id
    let category = selection.category
    if (category === 'stream segment') {
      navigateTo(`/conus/${id}`)
    } else if (category === 'huc') {
      navigateTo(`/huc/${id}`)
    }
  })
})
</script>

<template>
  <section class="section">
    <div class="container">
      <div class="field">
        <label class="label" for="search"
          >Search by stream segment name or HUC-8 ID</label
        >
        <input id="search" v-model="inputValue" class="input" />
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
#search {
  border: 1px solid rgba(33, 33, 33, 0.2);
  border-radius: 4px;
  color: #747474;
  font-size: 1rem;
  height: 40px;
  outline: none;
  padding-left: 10px;
  width: 600px;
  background: none;
}

:deep(.autoComplete_wrapper ul) {
  z-index: 1000;
}

:deep(.autoComplete_wrapper > ul > li > .category) {
  text-transform: uppercase;
  display: inline-block;
  padding-left: 1ex;
  color: #888;
  font-size: 90%;
}
</style>
