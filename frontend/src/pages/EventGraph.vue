<!--
  EventGraph.vue — ECharts line chart of race performances over time.

  Displays cumulative distance or average speed for selected athletes across
  one or more events. Supports imperial/metric toggle and sport filtering.

  Vue concepts for React developers:
  - ref()      → like useState(), creates a reactive variable. Access via .value in JS, direct in template.
  - computed() → like useMemo(), auto-recomputes when dependencies change. Read-only.
  - watch()    → like useEffect() with a dependency array. Runs a callback when watched value changes.
  - <script setup> → the component body itself (no return statement needed, everything is auto-exposed to template).
  - v-model    → two-way binding (like value + onChange combined). PrimeVue components use this for selection state.
  - v-for      → like .map() in JSX, but declarative in the template.
  - v-if       → like conditional rendering with {condition && <Component/>}.

  URL sync pattern (shared with EventGrid):
  - Selected events are stored as query params: /event/graph?event=homestead_2024&event=homestead_2023
  - Two watchers keep URL and component state in sync (dropdown → URL, URL → fetch).
  - `updatingFromQuery` flag prevents infinite loops between the two watchers.
-->
<script setup>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    DataZoomComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import MultiSelect from 'primevue/multiselect'
import SelectButton from 'primevue/selectbutton'
import Button from 'primevue/button'
import Chip from 'primevue/chip'
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchEventGraphData, fetchAllEvents } from '@/fetch/fetchEvents'
import { toSlug } from '@/utils/eventSlug'

// ECharts tree-shaking: register only the modules this page needs
use([CanvasRenderer, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, DataZoomComponent])

const router = useRouter()
const route = useRoute()

// --- State ---

const graphData = ref({}) // Keyed by slug: { [slug]: { performances, ... } }
const selectedSlugs = ref([])
const checkedAthletes = ref([])
const eventList = ref([])
const sportOptions = ref([
    { label: 'Skateboard', value: 'Skateboard', disabled: false },
    { label: 'Inline', value: 'Inline', disabled: false },
    { label: 'Quad', value: 'Quad', disabled: false },
])
const selectedSport = ref('Skateboard')

const metricOptions = [
    { label: 'Total distance', value: 'distance' },
    { label: 'Average speed', value: 'speed' },
]
const selectedMetric = ref('distance')

const unitOptions = [
    { label: 'miles', value: 'imperial' },
    { label: 'km', value: 'metric' },
]
const selectedUnit = ref('imperial')
const KPH_FACTOR = 1.60934
const round2 = (v) => Math.round(v * 100) / 100

// --- Data fetching ---

/** Parse event slugs from the URL query string (?event=slug1&event=slug2). */
const getSelectedSlugsFromQuery = () => {
    const raw = route.query.event
    if (!raw) return []
    return Array.isArray(raw) ? raw.filter(Boolean) : [raw]
}

/** Fetch graph data for new slugs, remove data for deselected ones. */
const fetchGraphEvents = async (slugs) => {
    const newSlugs = slugs.filter((s) => !(s in graphData.value))
    await Promise.all(
        newSlugs.map(async (slug) => {
            const [name, year] = slug.split('_')
            const data = await fetchEventGraphData(name, year)
            if (!data.error) graphData.value[slug] = data
        }),
    )
    for (const key of Object.keys(graphData.value)) {
        if (!slugs.includes(key)) delete graphData.value[key]
    }
}

/** Disable sport options that have no performances in the current selection. */
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

// --- Computed data ---

/**
 * Performances filtered by sport, flattened across all selected events.
 * Each entry gets an `athleteKey` that includes the event label when multiple events are selected,
 * so the same athlete from different years can be distinguished.
 * Sorted by total_miles desc (determines default top-5 selection and athlete panel order).
 */
const filteredPerformances = computed(() => {
    const result = []
    for (const [slug, evt] of Object.entries(graphData.value)) {
        const parts = slug.split('_')
        const name = parts[0].charAt(0).toUpperCase() + parts[0].slice(1)
        const year = parts[1]
        const eventLabel = selectedSlugs.value.length > 1 ? `${name} ${year}` : ''
        for (const perf of evt.performances || []) {
            if (perf.sport.toLowerCase().includes(selectedSport.value.toLowerCase())) {
                const athleteKey = eventLabel ? `${perf.athlete} (${eventLabel})` : perf.athlete
                result.push({ ...perf, athleteKey })
            }
        }
    }
    return result.sort((a, b) => b.total_miles - a.total_miles)
})

const athleteOptions = computed(() => {
    return filteredPerformances.value.map((p) => ({
        label: p.athleteKey,
        value: p.athleteKey,
    }))
})

// Auto-select top 5 athletes when the sport/event selection changes
watch(filteredPerformances, (perfs) => {
    const top5 = perfs.slice(0, 5).map((p) => p.athleteKey)
    checkedAthletes.value = top5
})

// --- Chart helpers ---

const CHART_COLORS = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']

/** Build an HTML color dot matching the one ECharts uses in its default tooltips. */
const makeMarker = (color) =>
    `<span style="display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:${color};"></span>`

/**
 * Linearly interpolate the y-value of a series at a given x position.
 * Returns null if x is before the first data point (athlete hasn't started).
 * Returns the last value if x is past the final point (athlete finished).
 * This allows the tooltip to show ALL series at any cursor position, not just
 * series that have an exact data point at that x.
 */
const interpolateY = (data, x) => {
    if (!data.length || x < data[0][0]) return null
    if (x >= data[data.length - 1][0]) return data[data.length - 1][1]
    for (let i = 0; i < data.length - 1; i++) {
        if (x >= data[i][0] && x <= data[i + 1][0]) {
            const t = (x - data[i][0]) / (data[i + 1][0] - data[i][0])
            return data[i][1] + t * (data[i + 1][1] - data[i][1])
        }
    }
    return null
}

// --- ECharts configuration ---

const chartOption = computed(() => {
    const isSpeed = selectedMetric.value === 'speed'
    const isMetric = selectedUnit.value === 'metric'

    // Convert miles→km or mph→kph (same factor applies to both)
    const convertData = (data) => {
        if (!isMetric) return data
        return data.map(([hours, val]) => [hours, round2(val * KPH_FACTOR)])
    }

    // Each series gets an explicit color so the tooltip markers stay in sync
    const series = filteredPerformances.value
        .filter((performance) => checkedAthletes.value.includes(performance.athleteKey))
        .map((p, idx) => ({
            name: p.athleteKey,
            type: 'line',
            showSymbol: false,
            smooth: false,
            triggerLineEvent: true,
            emphasis: {
                focus: 'series',
            },
            color: CHART_COLORS[idx % CHART_COLORS.length],
            data: convertData(isSpeed ? p.speed_data : p.data),
        }))

    return {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'line',
                snap: false, // Follow mouse freely instead of snapping to data points
            },
            // Custom formatter: interpolate ALL series at cursor x-position, sorted by value
            formatter: (params) => {
                if (!params.length) return ''
                const xVal = params[0].axisValue
                const hours = Math.floor(xVal)
                const minutes = Math.round((xVal - hours) * 60)
                const unit = isSpeed
                    ? (isMetric ? 'km/h' : 'mph')
                    : (isMetric ? 'km' : 'mi')
                const entries = series
                    .map((s) => {
                        const y = interpolateY(s.data, xVal)
                        if (y === null) return null
                        return { name: s.name, value: round2(y), color: s.color }
                    })
                    .filter(Boolean)
                    .sort((a, b) => b.value - a.value)
                const lines = entries.map(
                    (e, i) =>
                        `${makeMarker(e.color)} <b>${i + 1}.</b> ${e.name}: <b>${e.value} ${unit}</b>`,
                )
                return `<b>${hours}h${String(minutes).padStart(2, '0')}</b><br/>` + lines.join('<br/>')
            },
        },
        legend: {
            show: false,
        },
        grid: {
            left: 60,
            right: 30,
            top: 20,
            bottom: 55,
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
            name: isSpeed
                ? (isMetric ? 'Speed (km/h)' : 'Speed (mph)')
                : (isMetric ? 'Kilometers' : 'Miles'),
            // Distance starts at 0; speed uses data-driven min to avoid blank space
            min: isSpeed ? (value) => Math.floor(value.min) : 0,
        },
        dataZoom: [
            { type: 'inside', xAxisIndex: 0 },
            { type: 'inside', yAxisIndex: 0 },
            { type: 'slider', xAxisIndex: 0, bottom: 5, height: 20 },
        ],
        series,
    }
})

// --- Event list dropdown ---

const eventListOptions = computed(() => {
    return eventList.value.map((evt) => {
        const dateObj = new Date(evt.date)
        return {
            label: `${evt.name} ${dateObj.getFullYear()}`,
            value: toSlug(evt),
        }
    })
})

// --- URL ↔ state synchronization ---
// Two watchers form a bidirectional sync between selectedSlugs and the URL query.
// The `updatingFromQuery` flag prevents the dropdown→URL watcher from firing
// when we're updating state FROM the URL (which would cause an infinite loop).

let updatingFromQuery = false
watch(selectedSlugs, (newSlugs) => {
    if (updatingFromQuery) return
    const query = newSlugs.length ? { event: newSlugs } : {}
    router.push({ name: 'EventGraph', query })
})

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

// On mount: load all events for the dropdown, redirect to most recent if no query params
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
        <!-- Toolbar: event selector, sport filter, metric toggle, unit toggle -->
        <div class="flex items-center justify-center pb-4 gap-5">
            <MultiSelect v-model="selectedSlugs" :options="eventListOptions" optionLabel="label" optionValue="value"
                placeholder="Select Events" display="chip" class="w-full md:w-80" />

            <div class="card flex justify-center">
                <SelectButton v-model="selectedSport" :options="sportOptions" optionLabel="label" optionValue="value"
                    optionDisabled="disabled" />
            </div>

            <div class="card flex justify-center">
                <SelectButton v-model="selectedMetric" :options="metricOptions" optionLabel="label"
                    optionValue="value" />
            </div>

            <div class="card flex justify-center">
                <SelectButton v-model="selectedUnit" :options="unitOptions" optionLabel="label" optionValue="value" />
            </div>
        </div>

        <div class="flex flex-1 gap-4 min-h-0">
            <!-- Athlete selection panel -->
            <div class="w-64 shrink-0 flex flex-col border border-surface rounded-lg p-3 min-h-0">
                <MultiSelect v-model="checkedAthletes" :options="athleteOptions" optionLabel="label" optionValue="value"
                    filter autoFilterFocus placeholder="Search athletes..." :maxSelectedLabels="0"
                    :selectedItemsLabel="`${checkedAthletes.length} selected`" class="w-full mb-2" />
                <div class="flex items-center justify-between mb-2">
                    <span class="text-sm font-semibold text-muted-color">
                        Selected ({{ checkedAthletes.length }})
                    </span>
                    <Button v-if="checkedAthletes.length" icon="pi pi-times" label="Clear" severity="danger" text
                        size="small" @click="checkedAthletes = []" />
                </div>
                <div class="overflow-y-auto flex-1 flex flex-col gap-1">
                    <Chip v-for="athlete in checkedAthletes" :key="athlete" :label="athlete" removable
                        class="text-xs" @remove="checkedAthletes = checkedAthletes.filter((a) => a !== athlete)" />
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
