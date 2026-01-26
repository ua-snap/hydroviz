<script setup lang="ts">
import { eras } from '~/types/modelsScenarios'

import { streamflowStatistics } from '~/types/statsVars'
const { $_ } = useNuxtApp()

const props = defineProps(['streamStats', 'category'])

var statsInCategory = $_.filter(streamflowStatistics, {
  category: props.category,
})
</script>

<template>
  <table class="table" v-if="streamStats">
    <thead>
      <tr>
        <th>Statistic</th>
        <th>Description</th>
        <th>1976&ndash;2005</th>
        <th v-for="era in eras" :key="era" v-html="era"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="stat in statsInCategory" :key="stat.id">
        <th scope="row">
          <code>{{ stat.id }}</code>
        </th>
        <td v-html="stat.description"></td>
        <td>
          {{
            Number(
              streamStats.data['dynamic']['CCSM4']['historical']['1976-2005'][
                stat.id
              ]
            )
          }}
          <span style="color: #888" v-html="stat.units_short"></span>
        </td>
        <td v-for="era in Object.keys(eras)" :key="era">
          {{
            Number(streamStats.data['dynamic']['CCSM4']['rcp85'][era][stat.id])
          }}
          <span class="units" v-html="stat.units_short"></span>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<style lang="scss" scoped>
.units {
  color: #888;
}
</style>
