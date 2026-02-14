<script setup>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import MultiSelect from 'primevue/multiselect'
import SelectButton from 'primevue/selectbutton'
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchEventByCityYear, fetchAllEvents } from '@/fetch/fetchEvents'

const router = useRouter()
const route = useRoute()

const events = ref({})
const selectedSlugs = ref([])
const eventList = ref([])
const options = ref([
    { label: 'Skateboard', value: 'Skateboard', disabled: false },
    { label: 'Inline', value: 'Inline', disabled: false },
    { label: 'Quad', value: 'Quad', disabled: false },
])
const value = ref('Skateboard')

const toSlug = (evt) => {
    const city = evt.track.city.toLowerCase().replace(/ /g, '-')
    return `${city}_${new Date(evt.date).getFullYear()}`
}

const getSelectedSlugsFromQuery = () => {
    const raw = route.query.event
    if (!raw) return []
    return Array.isArray(raw) ? raw.filter(Boolean) : [raw]
}

const fetchEvents = async (slugs) => {
    const newSlugs = slugs.filter((s) => !(s in events.value))
    await Promise.all(
        newSlugs.map(async (slug) => {
            const [city, year] = slug.split('_')
            const data = await fetchEventByCityYear(city, year)
            if (!data.error) events.value[slug] = data
        }),
    )
    // Clean up deselected events
    for (const key of Object.keys(events.value)) {
        if (!slugs.includes(key)) delete events.value[key]
    }
}

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

const allPerformances = computed(() => {
    const result = []
    for (const [slug, evt] of Object.entries(events.value)) {
        const city = evt.track?.city || ''
        const year = new Date(evt.date).getFullYear()
        const eventLabel = `${city} ${year}`
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

const showEventColumn = computed(() => selectedSlugs.value.length > 1)

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
    router.push({ name: 'EventGrid', query })
})

// Watch route query -> sync state and fetch data
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

// Load event list for dropdown, redirect if no query params
fetchAllEvents()
    .then((response) => {
        eventList.value = response
        if (!route.query.event) {
            // Redirect to most recent event
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
