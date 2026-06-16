<script setup lang="ts">
import { fnc, roundSigFig } from '~/utils/general'
import { computed } from 'vue'

import { streamflowStatistics } from '~/types/statsVars'
const { $_ } = useNuxtApp()
const props = defineProps(['streamStats', 'category', 'tableTitle'])

var statsInCategory = $_.filter(streamflowStatistics, {
  category: props.category,
})

const tableCaptionHtml = computed(() => {
  return props.tableTitle + ', Mid-Century (2034&ndash;2065)'
})
</script>

<template>
  <div v-if="streamStats" class="my-6">
    <table class="table">
      <caption class="mb-4" v-html="tableCaptionHtml"></caption>
      <thead>
        <tr>
          <th scope="col" width="10%">Statistic</th>
          <th scope="col" width="30%">Description</th>
          <th scope="col" width="20%">Units</th>
          <th scope="col" width="20%">
            Modeled Historical<br />(1990&ndash;2021)
          </th>
          <th scope="col" width="20%">Median</th>
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
                  Number(streamStats['historical']['1990-2021'][stat.id])
                )
              )
            }}</span>
          </td>
          <td>
            <span class="number">
              {{
                fnc(
                  roundSigFig(
                    Number(
                      streamStats['projected']['2034-2065'][stat.id].median
                    )
                  )
                )
              }}
            </span>
            <Diff
              :past="
                roundSigFig(
                  Number(streamStats['historical']['1990-2021'][stat.id])
                )
              "
              :future="
                roundSigFig(
                  Number(streamStats['projected']['2034-2065'][stat.id].median)
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
table {
  width: 100%;
  caption {
    font-size: 1.5rem;
    font-weight: 600;
  }
}
</style>
