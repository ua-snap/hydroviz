<script setup lang="ts">
const { $autoComplete, $config, $_ } = useNuxtApp()
const inputValue = ref('')

onMounted(() => {
  let autoCompleteConfig = {
    selector: '#search',
    placeHolder: 'Search for a HUC-8 watershed or USGS gage ID',
    data: {
      src: async (query: string) => {
        // Strip "USGS-" prefix if present (case-insensitive) to allow users
        // to paste gage IDs with the prefix
        const cleanedQuery = query.replace(/^USGS-/i, '')
        // Escape single quotes for safe use inside CQL string literals
        const safeQuery = cleanedQuery.replace(/'/g, "''")
        const hucUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Ahuc8_conus_stats_simplified&outputFormat=application%2Fjson&srsName=EPSG:4326&propertyName=huc8,name&cql_filter=name%20ILIKE%20%27%25${safeQuery}%25%27%20OR%20huc8%20LIKE%20%27%25${safeQuery}%25%27`
        const alaskaHucUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aarctic_rivers_watersheds_stats_simplified_v2&outputFormat=application%2Fjson&srsName=EPSG:4326&propertyName=ID_2,Name&cql_filter=Name%20ILIKE%20%27%25${safeQuery}%25%27%20OR%20ID_2%20LIKE%20%27%25${safeQuery}%25%27`
        // Ungaged CONUS segments have a GAGE_ID of 'NA' rather than an
        // empty string, so exclude those from gage ID matches.
        const gageUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg_h8_outlet_stats_simplified_v2&outputFormat=application%2Fjson&srsName=EPSG:4326&propertyName=seg_id_nat,GNIS_NAME,GAGE_ID&cql_filter=GAGE_ID%20ILIKE%20%27%25${safeQuery}%25%27%20AND%20GAGE_ID%20%3C%3E%20%27NA%27`
        const alaskaGageUrl = `${$config.public.geoserverUrl}/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aarctic_rivers_segments_joined_3338_simplified_v2&outputFormat=application%2Fjson&srsName=EPSG:4326&propertyName=COMID,Name,Gage_ID&cql_filter=Gage_ID%20ILIKE%20%27%25${safeQuery}%25%27`

        let items: any[] = []

        try {
          const [hucRes, alaskaHucRes, gageRes, alaskaGageRes] =
            await Promise.all([
              fetch(hucUrl).then(res => res.json()),
              fetch(alaskaHucUrl).then(res => res.json()),
              fetch(gageUrl).then(res => res.json()),
              fetch(alaskaGageUrl).then(res => res.json()),
            ])

          // 'category' is a stable key the selection handler routes on;
          // 'label' is the display text shown in the dropdown.
          if (hucRes && Array.isArray(hucRes.features)) {
            hucRes.features.forEach((feature: any) => {
              let hucId = feature.properties.huc8
              let name = `${feature.properties.name} (${hucId})`
              items.push({
                name: name,
                id: hucId,
                category: 'huc',
                label: 'huc',
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
                label: 'huc',
                region: 'alaska',
              })
            })
          }

          if (gageRes && Array.isArray(gageRes.features)) {
            gageRes.features.forEach((feature: any) => {
              let segId = feature.properties.seg_id_nat
              let gageId = feature.properties.GAGE_ID
              let streamName = feature.properties.GNIS_NAME
              let name = streamName ? `${streamName} (${gageId})` : gageId
              items.push({
                name: name,
                id: segId,
                category: 'gage',
                label: 'gage ID',
                region: 'conus',
              })
            })
          }

          if (alaskaGageRes && Array.isArray(alaskaGageRes.features)) {
            alaskaGageRes.features.forEach((feature: any) => {
              let segId = feature.properties.COMID
              let gageId = feature.properties.Gage_ID
              let streamName = feature.properties.Name
              let name = streamName ? `${streamName} (${gageId})` : gageId
              items.push({
                name: name,
                id: segId,
                category: 'gage',
                label: 'gage ID',
                region: 'alaska',
              })
            })
          }

          items = $_.sortBy(items, ['category', 'name'])

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
          item.name + '<span class="category">' + item.label + '</span>'
      },
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
      category: selection.category,
    })

    if (selection.category === 'gage') {
      const routePrefix =
        selection.region === 'alaska' ? '/alaska/stream' : '/conus/stream'
      navigateTo(routePrefix + '/' + id)
    } else if (selection.region === 'conus') {
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
  <!-- The root div gives the runtime-created .autoComplete_wrapper a scoped
       ancestor so the :deep() dropdown styles below can match. -->
  <div>
    <label class="label is-sr-only" for="search"
      >Search by HUC-8 ID or USGS gage ID</label
    >
    <input id="search" v-model="inputValue" class="input" />
  </div>
</template>

<style lang="scss" scoped>
#search {
  width: 35rem;
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
