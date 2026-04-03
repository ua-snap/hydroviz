<script setup lang="ts">
import { eraFullNamesHtml, scenarioFullNames } from '~/types/modelsScenarios'
import { fnc, roundSigFig } from '~/utils/general'
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
            <span class="number">{{
              fnc(
                roundSigFig(
                  Number(streamStats['historical']['1976-2005'][stat.id])
                )
              )
            }}</span>
          </td>
          <td>
            <span class="number">
              {{
                fnc(
                  roundSigFig(
                    Number(streamStats['projected'][appEra].mid[stat.id])
                  )
                )
              }}
            </span>
            <Diff
              :past="
                roundSigFig(
                  Number(streamStats['historical']['1976-2005'][stat.id])
                )
              "
              :future="
                roundSigFig(
                  Number(streamStats['projected'][appEra].mid[stat.id])
                )
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

          <th scope="col">Minimum, {{ scenarioFullNames['rcp45'] }}</th>
          <th scope="col">Maximum, {{ scenarioFullNames['rcp85'] }}</th>
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
            <span class="number">{{
              fnc(
                roundSigFig(
                  Number(streamStats['historical']['1976-2005'][stat.id])
                )
              )
            }}</span>
          </td>
          <td>
            <span class="number">
              {{
                fnc(
                  roundSigFig(
                    Number(streamStats['projected'][appEra].min[stat.id])
                  )
                )
              }}
            </span>
            <Diff
              :past="
                roundSigFig(
                  Number(streamStats['historical']['1976-2005'][stat.id])
                )
              "
              :future="
                roundSigFig(
                  Number(streamStats['projected'][appEra].min[stat.id])
                )
              "
            />
          </td>
          <td>
            <span class="number">
              {{
                fnc(
                  roundSigFig(
                    Number(streamStats['projected'][appEra].max[stat.id])
                  )
                )
              }}
            </span>
            <Diff
              :past="
                roundSigFig(
                  Number(streamStats['historical']['1976-2005'][stat.id])
                )
              "
              :future="
                roundSigFig(
                  Number(streamStats['projected'][appEra].max[stat.id])
                )
              "
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
