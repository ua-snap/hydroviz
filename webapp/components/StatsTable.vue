<script setup lang="ts">
import { eraFullNamesHtml, scenarioFullNames } from '~/types/modelsScenarios'
import { computed } from 'vue'

import { streamflowStatistics } from '~/types/statsVars'
const { $_ } = useNuxtApp()
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { appContext, appEra } = storeToRefs(streamSegmentStore)
const props = defineProps(['streamStats', 'category', 'tableTitle'])

var statsInCategory = $_.filter(streamflowStatistics, {
  category: props.category,
})

const tableCaptionHtml = computed(() => {
  return props.tableTitle + ', ' + eraFullNamesHtml[appEra.value]
})
</script>

<template>
  <div v-if="streamStats" class="my-6">
    <table class="table" v-if="appContext == 'mid'">
      <caption class="mb-4" v-html="tableCaptionHtml"></caption>
      <thead>
        <tr>
          <th scope="col" width="10%">Statistic</th>
          <th scope="col" width="30%">Description</th>
          <th scope="col" width="20%">Units</th>
          <th scope="col" width="20%">
            Modeled Historical<br />(1976&ndash;2005)
          </th>
          <th scope="col" width="20%">
            Median, {{ scenarioFullNames['rcp60'] }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stat in statsInCategory" :key="stat.id">
          <th scope="row">
            <code>{{ stat.id }}</code>
          </th>
          <td v-html="stat.description"></td>
          <td v-html="stat.units_short"></td>
          <td>
            <StatValue
              :value="streamStats['historical']['1976-2005'][stat.id]"
            />
          </td>
          <td>
            <StatValue
              :value="streamStats['projected'][appEra]['rcp60'][stat.id].median"
              :past="streamStats['historical']['1976-2005'][stat.id]"
              :future="
                streamStats['projected'][appEra]['rcp60'][stat.id].median
              "
            />
          </td>
        </tr>
      </tbody>
    </table>
    <table class="table" v-if="appContext == 'extremes'">
      <caption class="mb-4" v-html="tableCaptionHtml"></caption>
      <thead>
        <tr>
          <th scope="col" width="10%">Statistic</th>
          <th scope="col" width="25%">Description</th>
          <th scope="col" width="10%">Units</th>
          <th scope="col" width="15%">
            Modeled Historical<br />(1976&ndash;2005)
          </th>
          <th scope="col">Median, {{ scenarioFullNames['rcp45'] }}</th>
          <th scope="col">Median, {{ scenarioFullNames['rcp85'] }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stat in statsInCategory" :key="stat.id">
          <th scope="row">
            <code>{{ stat.id }}</code>
          </th>
          <td v-html="stat.description"></td>
          <td v-html="stat.units_short"></td>
          <td>
            <StatValue
              :value="streamStats['historical']['1976-2005'][stat.id]"
            />
          </td>
          <td>
            <StatValue
              :value="streamStats['projected'][appEra]['rcp45'][stat.id].min"
              :past="streamStats['historical']['1976-2005'][stat.id]"
            />
          </td>
          <td>
            <StatValue
              :value="streamStats['projected'][appEra]['rcp85'][stat.id].max"
              :past="streamStats['historical']['1976-2005'][stat.id]"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style lang="scss" scoped>
table caption {
  font-size: 1.5rem;
  font-weight: 600;
}
</style>
