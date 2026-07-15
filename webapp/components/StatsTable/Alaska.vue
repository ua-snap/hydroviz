<script setup lang="ts">
import { scenarioFullNames } from '~/types/modelsScenarios'
import { fnc, roundSigFig } from '~/utils/general'
import { nullValueFooter } from '~/utils/table'
import { computed } from 'vue'

import { statistics } from '~/types/statsVars'
const { $_ } = useNuxtApp()
const props = defineProps(['streamStats', 'wtStats', 'category', 'tableTitle'])

// Support both streamStats and wtStats props
const statsData = computed(() => props.wtStats || props.streamStats)

var statsInCategory = $_.filter(statistics, {
  category: props.category,
})

const tableCaptionHtml = computed(() => {
  return props.tableTitle + ', Mid-Century (2034&ndash;2065)'
})

const hasNullValues = computed(() => {
  if (!statsData.value) return false
  const checkNull = (val: any) => val === null || val === undefined
  return statsInCategory.some((stat: any) => {
    const values = [
      statsData.value['historical']['1990-2021'][stat.id],
      statsData.value['projected']['2034-2065'][stat.id]?.median,
    ]
    return values.some(checkNull)
  })
})
</script>

<template>
  <div v-if="statsData" class="my-6">
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
          <th scope="col" width="20%">
            Median, {{ scenarioFullNames['ssp370'] }}
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
                  Number(statsData['historical']['1990-2021'][stat.id])
                )
              )
            }}</span>
          </td>
          <td>
            <span class="number">
              {{
                fnc(
                  roundSigFig(
                    Number(statsData['projected']['2034-2065'][stat.id].median)
                  )
                )
              }}
            </span>
            <Diff
              :past="
                roundSigFig(
                  Number(statsData['historical']['1990-2021'][stat.id])
                )
              "
              :future="
                roundSigFig(
                  Number(statsData['projected']['2034-2065'][stat.id].median)
                )
              "
            />
          </td>
        </tr>
      </tbody>
      <tfoot v-if="hasNullValues">
        <tr>
          <td colspan="5" v-html="nullValueFooter"></td>
        </tr>
      </tfoot>
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
