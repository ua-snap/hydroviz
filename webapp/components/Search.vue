<script setup lang="ts">
const { $autoComplete, $config, $_ } = useNuxtApp()
const inputValue = ref('')

onMounted(() => {
  let autoCompleteConfig = {
    selector: '#search',
    placeHolder: 'Search for a HUC-8 watershed',
    data: {
      src: async (query: string) => {
        // Escape single quotes for safe use inside CQL string literals
        const safeQuery = query.replace(/'/g, "''")
        const hucUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Ahuc8_conus_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&propertyName=huc8,name&cql_filter=name%20ILIKE%20%27%25${safeQuery}%25%27%20OR%20huc8%20LIKE%20%27%25${safeQuery}%25%27`
        const alaskaHucUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aarctic_rivers_watersheds_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&propertyName=ID_2,Name&cql_filter=Name%20ILIKE%20%27%25${safeQuery}%25%27%20OR%20ID_2%20LIKE%20%27%25${safeQuery}%25%27`

        let items: any[] = []

        try {
          const [hucRes, alaskaHucRes] = await Promise.all([
            fetch(hucUrl).then(res => res.json()),
            fetch(alaskaHucUrl).then(res => res.json()),
          ])

          if (hucRes && Array.isArray(hucRes.features)) {
            hucRes.features.forEach((feature: any) => {
              let hucId = feature.properties.huc8
              let name = `${feature.properties.name} (${hucId})`
              items.push({
                name: name,
                id: hucId,
                category: 'huc',
                region: 'conus',
              })
            })
          }

          if (alaskaHucRes && Array.isArray(alaskaHucRes.features)) {
            alaskaHucRes.features.forEach((feature: any) => {
              let hucId = feature.properties.ID_2
              let name = `${feature.properties.Name} (${hucId})`
              items.push({
                name: name,
                id: hucId,
                category: 'huc',
                region: 'alaska',
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
    threshold: 3,
    debounce: 200,
  }

  let searchAutoComplete = new $autoComplete(autoCompleteConfig)

  searchAutoComplete.input.addEventListener('selection', function (event: any) {
    let selection = event.detail.selection.value
    let id = selection.id

    window.trackUmamiEvent('search-selection', {
      id: id,
      name: selection.name,
      region: selection.region,
    })

    if (selection.region === 'conus') {
      navigateTo({
        path: '/',
        query: { cp: 2, chuc: id },
        hash: '#conus-map',
      })
    } else if (selection.region === 'alaska') {
      navigateTo({
        path: '/',
        query: { ap: 2, ahuc: id },
        hash: '#alaska-map',
      })
    }
  })
})
</script>

<template>
  <label class="label is-sr-only" for="search">Search by HUC-8 ID</label>
  <input id="search" v-model="inputValue" class="input" />
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
  max-width: 30rem;
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
