<script setup>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import MultiSelect from 'primevue/multiselect'
import SelectButton from 'primevue/selectbutton'
import Checkbox from 'primevue/checkbox'
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchEventGraphData, fetchAllEvents } from '@/fetch/fetchEvents'

use([CanvasRenderer, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

const router = useRouter()
const route = useRoute()

const graphData = ref({})
const selectedSlugs = ref([])
const checkedAthletes = ref([])
const eventList = ref([])
const sportOptions = ref([
    { label: 'Skateboard', value: 'Skateboard', disabled: false },
    { label: 'Inline', value: 'Inline', disabled: false },
    { label: 'Quad', value: 'Quad', disabled: false },
])
const selectedSport = ref('Skateboard')

const toSlug = (evt) => {
    const city = evt.track.city.toLowerCase().replace(/ /g, '-')
    return `${city}_${new Date(evt.date).getFullYear()}`
}

const getSelectedSlugsFromQuery = () => {
    const raw = route.query.event
    if (!raw) return []
    return Array.isArray(raw) ? raw.filter(Boolean) : [raw]
}

const fetchGraphEvents = async (slugs) => {
    const newSlugs = slugs.filter((s) => !(s in graphData.value))
    await Promise.all(
        newSlugs.map(async (slug) => {
            const [city, year] = slug.split('_')
            const data = await fetchEventGraphData(city, year)
            if (!data.error) graphData.value[slug] = data
        }),
    )
    for (const key of Object.keys(graphData.value)) {
        if (!slugs.includes(key)) delete graphData.value[key]
    }
}

const updateSportOptions = () => {
    const allPerfs = Object.values(graphData.value).flatMap((evt) => evt.performances || [])
    const sports = allPerfs.map((p) => p.sport.toLowerCase())
    const hasSport = (optValue) => sports.some((s) => s.includes(optValue.toLowerCase()))
    sportOptions.value = sportOptions.value.map((opt) => ({
        ...opt,
        disabled: !hasSport(opt.value),
    }))
    if (!hasSport(selectedSport.value)) {
        const firstAvailable = sportOptions.value.find((opt) => !opt.disabled)
        if (firstAvailable) selectedSport.value = firstAvailable.value
    }
}

// All performances across selected events, filtered by sport
const filteredPerformances = computed(() => {
    const result = []
    for (const [slug, evt] of Object.entries(graphData.value)) {
        const parts = slug.split('_')
        const city = parts[0]
        const year = parts[1]
        const eventLabel = selectedSlugs.value.length > 1 ? `${city} ${year}` : ''
        for (const perf of evt.performances || []) {
            if (perf.sport.toLowerCase().includes(selectedSport.value.toLowerCase())) {
                const athleteKey = eventLabel ? `${perf.athlete} (${eventLabel})` : perf.athlete
                result.push({ ...perf, athleteKey })
            }
        }
    }
    return result.sort((a, b) => b.total_miles - a.total_miles)
})

// Available athletes for the checkbox panel
const athleteList = computed(() => {
    return filteredPerformances.value.map((p) => p.athleteKey)
})

// Auto-select top 5 when filtered performances change
watch(filteredPerformances, (perfs) => {
    const top5 = perfs.slice(0, 5).map((p) => p.athleteKey)
    checkedAthletes.value = top5
})

// ECharts option
const chartOption = computed(() => {
    const series = filteredPerformances.value
        .filter((p) => checkedAthletes.value.includes(p.athleteKey))
        .map((p) => ({
            name: p.athleteKey,
            type: 'line',
            showSymbol: false,
            smooth: false,
            data: p.data,
        }))

    return {
        tooltip: {
            trigger: 'axis',
            formatter: (params) => {
                return params
                    .map((p) => {
                        const hours = Math.floor(p.data[0])
                        const minutes = Math.round((p.data[0] - hours) * 60)
                        return `${p.seriesName}: ${p.data[1]} mi @ ${hours}h${String(minutes).padStart(2, '0')}`
                    })
                    .join('<br/>')
            },
        },
        legend: {
            show: false,
        },
        grid: {
            left: 60,
            right: 30,
            top: 20,
            bottom: 40,
        },
        xAxis: {
            type: 'value',
            name: 'Time (hours)',
            min: 0,
            max: 24,
            interval: 2,
            axisLabel: {
                formatter: '{value}h',
            },
        },
        yAxis: {
            type: 'value',
            name: 'Miles',
            min: 0,
        },
        series,
    }
})

const eventListOptions = computed(() => {
    return eventList.value.map((evt) => {
        const dateObj = new Date(evt.date)
        return {
            label: `${evt.track.city} ${dateObj.getFullYear()}`,
            value: toSlug(evt),
        }
    })
})

// Watch dropdown selection -> update URL
let updatingFromQuery = false
watch(selectedSlugs, (newSlugs) => {
    if (updatingFromQuery) return
    const query = newSlugs.length ? { event: newSlugs } : {}
    router.push({ name: 'EventGraph', query })
})

// Watch route query -> sync state and fetch data
watch(
    () => route.query.event,
    async () => {
        updatingFromQuery = true
        const slugs = getSelectedSlugsFromQuery()
        selectedSlugs.value = slugs
        if (slugs.length) {
            await fetchGraphEvents(slugs)
            updateSportOptions()
        }
        updatingFromQuery = false
    },
    { immediate: true },
)

// Load event list for dropdown, redirect if no query params
fetchAllEvents()
    .then((response) => {
        eventList.value = response
        if (!route.query.event) {
            if (response.length) {
                const sorted = [...response].sort(
                    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime(),
                )
                const slug = toSlug(sorted[0])
                if (slug) {
                    router.replace({ name: 'EventGraph', query: { event: slug } })
                }
            }
        }
    })
    .catch((error) => {
        console.error(error)
    })
</script>

<template>
    <div class="p-4 flex flex-col h-[calc(100vh-44px)]">
        <div class="flex items-center justify-center pb-4 gap-5">
            <MultiSelect
                v-model="selectedSlugs"
                :options="eventListOptions"
                optionLabel="label"
                optionValue="value"
                placeholder="Select Events"
                display="chip"
                class="w-full md:w-80"
            />

            <div class="card flex justify-center">
                <SelectButton
                    v-model="selectedSport"
                    :options="sportOptions"
                    optionLabel="label"
                    optionValue="value"
                    optionDisabled="disabled"
                />
            </div>
        </div>

        <div class="flex flex-1 gap-4 min-h-0">
            <!-- Athlete checkbox panel -->
            <div class="w-64 shrink-0 overflow-y-auto border border-gray-700 rounded-lg p-3">
                <div class="text-sm font-semibold text-gray-300 mb-2">
                    Athletes ({{ checkedAthletes.length }}/{{ athleteList.length }})
                </div>
                <div v-for="athlete in athleteList" :key="athlete" class="flex items-center gap-2 py-1">
                    <Checkbox
                        v-model="checkedAthletes"
                        :inputId="athlete"
                        :value="athlete"
                    />
                    <label :for="athlete" class="text-sm text-gray-300 cursor-pointer truncate">
                        {{ athlete }}
                    </label>
                </div>
            </div>

            <!-- Chart -->
            <div class="flex-1 min-h-0">
                <v-chart :option="chartOption" autoresize class="w-full h-full" />
            </div>
        </div>
    </div>
</template>

<style scoped></style>
