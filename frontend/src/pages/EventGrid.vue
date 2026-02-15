<!--
  EventGrid.vue — DataTable view of race performances.

  Displays all performances in a sortable PrimeVue DataTable with multi-event
  selection and sport filtering. Shows an "Event" column when multiple events
  are selected so the user can distinguish rows.

  Vue concepts for React developers:
  - ref()      → like useState(), creates a reactive variable. Access via .value in JS, direct in template.
  - computed() → like useMemo(), auto-recomputes when dependencies change. Read-only.
  - watch()    → like useEffect() with a dependency array. Runs a callback when watched value changes.
  - <script setup> → the component body itself (no return statement needed, everything is auto-exposed to template).
  - v-model    → two-way binding (like value + onChange combined). PrimeVue components use this for selection state.
  - v-for      → like .map() in JSX, but declarative in the template.
  - v-if       → like conditional rendering with {condition && <Component/>}.

  URL sync pattern (shared with EventGraph):
  - Selected events are stored as query params: /event?event=homestead_2024&event=homestead_2023
  - Two watchers keep URL and component state in sync (dropdown → URL, URL → fetch).
  - `updatingFromQuery` flag prevents infinite loops between the two watchers.
-->
<script setup>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import MultiSelect from 'primevue/multiselect'
import SelectButton from 'primevue/selectbutton'
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchEventByNameYear, fetchAllEvents } from '@/fetch/fetchEvents'
import { toSlug } from '@/utils/eventSlug'

const router = useRouter()
const route = useRoute()

// --- State ---

const events = ref({}) // Keyed by slug: { [slug]: { performances, ... } }
const selectedSlugs = ref([])
const eventList = ref([])
const options = ref([
    { label: 'Skateboard', value: 'Skateboard', disabled: false },
    { label: 'Inline', value: 'Inline', disabled: false },
    { label: 'Quad', value: 'Quad', disabled: false },
])
const value = ref('Skateboard')

// --- Data fetching ---

/** Parse event slugs from the URL query string (?event=slug1&event=slug2). */
const getSelectedSlugsFromQuery = () => {
    const raw = route.query.event
    if (!raw) return []
    return Array.isArray(raw) ? raw.filter(Boolean) : [raw]
}

/** Fetch event data for new slugs, remove data for deselected ones. */
const fetchEvents = async (slugs) => {
    const newSlugs = slugs.filter((s) => !(s in events.value))
    await Promise.all(
        newSlugs.map(async (slug) => {
            const [name, year] = slug.split('_')
            const data = await fetchEventByNameYear(name, year)
            if (!data.error) events.value[slug] = data
        }),
    )
    for (const key of Object.keys(events.value)) {
        if (!slugs.includes(key)) delete events.value[key]
    }
}

/** Disable sport options that have no performances in the current selection. */
const updateSportOptions = () => {
    const allPerfs = Object.values(events.value).flatMap((evt) => evt.performances || [])
    const sports = allPerfs.map((p) => p.sport.toLowerCase())
    const hasSport = (optValue) => sports.some((s) => s.includes(optValue.toLowerCase()))
    options.value = options.value.map((opt) => ({
        ...opt,
        disabled: !hasSport(opt.value),
    }))
    if (!hasSport(value.value)) {
        const firstAvailable = options.value.find((opt) => !opt.disabled)
        if (firstAvailable) value.value = firstAvailable.value
    }
}

// --- Computed data ---

/** All performances flattened across selected events, with an eventLabel for display. */
const allPerformances = computed(() => {
    const result = []
    for (const [slug, evt] of Object.entries(events.value)) {
        const name = evt.name || ''
        const year = new Date(evt.date).getFullYear()
        const eventLabel = `${name} ${year}`
        for (const perf of evt.performances || []) {
            result.push({ ...perf, eventLabel })
        }
    }
    return result
})

const filteredPerformances = computed(() => {
    return allPerformances.value.filter((performance) =>
        performance.sport.toLowerCase().includes(value.value.toLowerCase()),
    )
})

/** Show "Event" column only when comparing multiple events. */
const showEventColumn = computed(() => selectedSlugs.value.length > 1)

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
    router.push({ name: 'EventGrid', query })
})

watch(
    () => route.query.event,
    async (newVal) => {
        updatingFromQuery = true
        const slugs = getSelectedSlugsFromQuery()
        selectedSlugs.value = slugs
        if (slugs.length) {
            await fetchEvents(slugs)
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
                const mostRecent = sorted[0]
                const slug = toSlug(mostRecent)
                if (slug) {
                    router.replace({ name: 'EventGrid', query: { event: slug } })
                }
            }
        }
    })
    .catch((error) => {
        console.error(error)
    })
</script>

<template>
    <div class="p-4">
        <!-- Toolbar: event selector + sport filter -->
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
                    v-model="value"
                    :options="options"
                    optionLabel="label"
                    optionValue="value"
                    optionDisabled="disabled"
                />
            </div>
        </div>

        <DataTable :value="filteredPerformances" sortMode="multiple" tableStyle="{}">
            <Column header="#">
                <template #body="slotProps">
                    {{ (slotProps.rowIndex ?? slotProps.index ?? 0) + 1 }}
                </template>
            </Column>
            <Column v-if="showEventColumn" field="eventLabel" header="Event" sortable />
            <Column field="athlete.name" header="Athlete" sortable />
            <Column field="age_group" header="Age Group" sortable />
            <Column field="category" header="Category" sortable />
            <Column field="sport" header="Sport" sortable />
            <Column field="total_laps" header="Laps" sortable />
            <Column field="total_km" header="KM" sortable />
            <Column field="total_miles" header="Miles" sortable />
            <Column field="total_time_hhmmss" header="Time" sortable />
        </DataTable>
    </div>
</template>

<style scoped></style>
