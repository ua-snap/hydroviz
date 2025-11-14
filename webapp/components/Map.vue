<script setup lang="ts">
const { $L } = useNuxtApp()
const lcInput = defineModel('lc', { default: 'dynamic' })
const modelInput = defineModel('model', { default: 'ACCESS1-0' })
const scenarioInput = defineModel('scenario', { default: 'rcp85' })

let segName = ref('')
let statsData = ref(null)
let selectedSeg = ref(null)
let zoomAddGeoJson = false
let moveAddGeoJson = false

const lcs: Record<string, string> = {
  dynamic: 'Dynamic',
  static: 'Static',
}

const models: Record<string, string> = {
  'ACCESS1-0': 'ACCESS1-0',
  'bcc-csm1-1': 'BCC-CSM1-1',
  'BNU-ESM': 'BNU-ESM',
  CCSM4: 'CCSM4',
  'GFDL-ESM2G': 'GFDL-ESM2G',
  'GFDL-ESM2M': 'GFDL-ESM2M',
  'IPSL-CM5A-LR': 'IPSL-CM5A-LR',
  'IPSL-CM5A-MR': 'IPSL-CM5A-MR',
  MIROC5: 'MIROC5',
  'MIROC-ESM': 'MIROC-ESM',
  'MIROC-ESM-CHEM': 'MIROC-ESM-CHEM',
  'MRI-CGCM3': 'MRI-CGCM3',
  'NorESM1-M': 'NorESM1-M',
}

const scenarios: Record<string, string> = {
  rcp26: 'RCP 2.6',
  rcp45: 'RCP 4.5',
  rcp60: 'RCP 6.0',
  rcp85: 'RCP 8.5',
}

const eras: Record<string, string> = {
  // '1976_2005': '1976-2005',
  '2016_2045': '2016-2045',
  '2046_2075': '2046-2075',
  '2071_2100': '2071-2100',
}

const statsUnits: Record<string, string> = {
  dh3: 'cfs',
  dh15: 'days/year',
  dl3: 'cfs',
  dl16: 'days/year',
  fh1: 'events/year',
  fl1: 'events/year',
  fl3: 'events/year',
  ma12: 'cfs',
  ma13: 'cfs',
  ma14: 'cfs',
  ma15: 'cfs',
  ma16: 'cfs',
  ma17: 'cfs',
  ma18: 'cfs',
  ma19: 'cfs',
  ma20: 'cfs',
  ma21: 'cfs',
  ma22: 'cfs',
  ma23: 'cfs',
  ra1: 'cfs/day',
  ra3: 'cfs/day',
  th1: 'day',
  tl1: 'day',
}

const stats = Object.keys(statsUnits)

onMounted(() => {
  var map = $L.map('map').setView([37.8, -96], 4)
  var geoJsonlayer: any = null

  $L.tileLayer(
    'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    {
      maxZoom: 19,
      attribution: 'Map data © USGS',
    }
  ).addTo(map)

  var wmsLayer = $L.tileLayer
    .wms('https://gs.earthmaps.io/geoserver/wms', {
      transparent: true,
      format: 'image/png',
      layers: 'hydrology:seg',
      zIndex: 10,
    })
    .addTo(map)

  map.on('zoomend', function () {
    if (moveAddGeoJson) {
      return
    } else {
      zoomAddGeoJson = true
    }
    if (map.getZoom() > 8) {
      if (!geoJsonlayer) {
        var bounds = map.getBounds()
        var minLon = bounds.getWest()
        var maxLon = bounds.getEast()
        var minLat = bounds.getSouth()
        var maxLat = bounds.getNorth()
        addGeoJson(minLon, maxLon, maxLat, minLat)
      }
    } else {
      if (!map.hasLayer(wmsLayer)) {
        map.addLayer(wmsLayer)
      }
      if (geoJsonlayer && map.hasLayer(geoJsonlayer)) {
        map.removeLayer(geoJsonlayer)
        geoJsonlayer = null
      }
    }
  })

  map.on('moveend', function () {
    if (zoomAddGeoJson) {
      return
    } else {
      moveAddGeoJson = true
    }
    if (geoJsonlayer) {
      map.removeLayer(geoJsonlayer)
      geoJsonlayer = null
    }
    if (map.getZoom() > 8) {
      var bounds = map.getBounds()
      var minLon = bounds.getWest()
      var maxLon = bounds.getEast()
      var minLat = bounds.getSouth()
      var maxLat = bounds.getNorth()
      addGeoJson(minLon, maxLon, maxLat, minLat)
    } else {
      if (!map.hasLayer(wmsLayer)) {
        map.addLayer(wmsLayer)
      }
      if (geoJsonlayer && map.hasLayer(geoJsonlayer)) {
        map.removeLayer(geoJsonlayer)
        geoJsonlayer = null
      }
    }
  })

  const addGeoJson = async (
    minLon: number,
    maxLon: number,
    maxLat: number,
    minLat: number
  ) => {
    if (geoJsonlayer) return
    fetch(
      'https://gs.earthmaps.io/geoserver/hydrology/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=hydrology%3Aseg&outputFormat=application%2Fjson&srsName=EPSG:4326&cql_filter=INTERSECTS(the_geom,ENVELOPE(' +
        minLon +
        ',' +
        maxLon +
        ',' +
        maxLat +
        ',' +
        minLat +
        '))'
    )
      .then(response => response.json())
      .then(data => {
        geoJsonlayer = $L
          .geoJSON(data)
          .addTo(map)
          .on('click', function (e) {
            if (selectedSeg.value) {
              statsData.value = null
              selectedSeg.value.setStyle({
                color: 'rgb(51, 136, 255)',
              })
            }
            selectedSeg.value = e.sourceTarget
            segName.value = selectedSeg.value?.feature.properties.GNIS_NAME
            console.log(
              'geom_id: ' + selectedSeg.value?.feature.properties.seg_id_nat
            )
            let seg_id = selectedSeg.value?.feature.properties.seg_id_nat
            let url =
              'http://127.0.0.1:5000/conus_hydrology/' +
              seg_id
            selectedSeg.value?.setStyle({
              color: 'red',
            })
            const startTime = performance.now()
            fetch(url)
              .then(response => response.json())
              .then(data => {
                statsData.value = data[seg_id]['stats']
                const endTime = performance.now()
                console.log(
                  `Fetch took ${((endTime - startTime) / 1000).toFixed(1)} seconds`
                )
              })
          })
        zoomAddGeoJson = false
        moveAddGeoJson = false
        map.removeLayer(wmsLayer)
      })
  }

  map.on('zoomend', function () {
    console.log('Current Zoom: ' + map.getZoom())
  })
})
</script>

<template>
  <div>
    <div id="map" style="height: 500px"></div>
  </div>
  <div v-if="selectedSeg && !statsData" class="p-6">
    <progress class="progress" />
  </div>
  <div v-if="statsData">
    <h3
      class="title is-3 is-flex is-justify-content-center is-align-items-center mt-6 mb-5"
    >
      Statistics for {{ segName }}
    </h3>
    <div
      class="container is-flex is-justify-content-center is-align-items-center"
    >
      <div class="parameter">
        <div class="select mb-5 mr-3">
          <select id="scenario" v-model="lcInput">
            <option v-for="lc in Object.keys(lcs)" :value="lc">
              {{ lcs[lc] }}
            </option>
          </select>
        </div>
      </div>
      <div class="parameter">
        <div class="select mb-5 mr-3">
          <select id="scenario" v-model="modelInput">
            <option v-for="model in Object.keys(models)" :value="model">
              {{ models[model] }}
            </option>
          </select>
        </div>
      </div>
      <div class="parameter">
        <div class="select mb-5 mr-3">
          <select id="scenario" v-model="scenarioInput">
            <option
              v-for="scenario in Object.keys(scenarios)"
              :value="scenario"
            >
              {{ scenarios[scenario] }}
            </option>
          </select>
        </div>
      </div>
    </div>
    <div
      class="container is-flex is-justify-content-center is-align-items-center"
    >
      <table class="table mb-6">
        <thead>
          <tr>
            <th class="p-5">Statistic</th>
            <th class="p-5">1976-2005</th>
            <th v-for="era in Object.keys(eras)" class="p-5">
              {{ eras[era] }}
            </th>
          </tr>
        </thead>
        <tr v-for="stat in stats">
          <th class="p-5">{{ stat }}</th>
          <td class="p-5">
            {{
              Number(
                statsData[lcInput][modelInput]['historical']['1976_2005'][stat]
              ).toFixed(2)
            }}
            <span style="color: #888">{{ statsUnits[stat] }}</span>
          </td>
          <td v-for="era in Object.keys(eras)" class="p-5">
            {{
              Number(
                statsData[lcInput][modelInput][scenarioInput][era][stat]
              ).toFixed(2)
            }}
            <span style="color: #888">{{ statsUnits[stat] }}</span>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.parameter {
  display: inline-block;
  select {
    background-color: #ffffff;
  }
}
</style>
