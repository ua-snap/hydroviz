<script setup lang="ts">
import { lcs, models, scenarios, eras } from '~/types/modelsScenarios'
import { statVars } from '~/types/statsVars'
import { useStreamSegmentStore } from '~/stores/streamSegment'
const streamSegmentStore = useStreamSegmentStore()
let { streamStats, segmentName } = storeToRefs(streamSegmentStore)

const lcInput = defineModel('lc', { default: 'dynamic' })
const modelInput = defineModel('model', { default: 'CCSM4' })
const scenarioInput = defineModel('scenario', { default: 'rcp60' })
</script>

<template>
  <VizHydrograph />
  <VizMonthlyFlow />
  <section class="section report">
    <div class="container">
      <Loading />
      <div v-if="streamStats">
        <h3
          class="title is-3 is-flex is-justify-content-center is-align-items-center mt-6 mb-5"
        >
          Statistics for {{ segmentName }}
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
                <th class="p-5">Description</th>
                <th class="p-5">1976-2005</th>
                <th v-for="era in Object.keys(eras)" class="p-5">
                  {{ eras[era] }}
                </th>
              </tr>
            </thead>
            <tr v-for="stat in Object.keys(statVars)">
              <th class="p-5" scope="row">{{ stat }}</th>
              <td class="p-5" v-html="statVars[stat].title"></td>
              <td class="p-5">
                {{
                  Number(
                    streamStats.data[lcInput][modelInput]['historical'][
                      '1976-2005'
                    ][stat]
                  ).toFixed(2)
                }}
                <span style="color: #888">{{ statVars[stat].units }}</span>
              </td>
              <td v-for="era in Object.keys(eras)" class="p-5">
                {{
                  Number(
                    streamStats.data[lcInput][modelInput][scenarioInput][era][
                      stat
                    ]
                  ).toFixed(2)
                }}
                <span style="color: #888">{{ statVars[stat].units }}</span>
              </td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.report {
  min-height: 50vh;
}
table {
  th[scope='row'] {
    text-transform: uppercase;
  }
}
.parameter {
  display: inline-block;
  select {
    background-color: #ffffff;
  }
}
</style>
