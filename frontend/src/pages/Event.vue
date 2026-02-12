<script setup>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { fetchEventByYear, fetchAllEvents } from '@/fetch/fetchEvents'
import SelectButton from 'primevue/selectbutton'
import Select from 'primevue/select'

const props = defineProps({
    year: {
        type: String,
        required: false
    }
})

const router = useRouter()

const event = ref(null)
const eventList = ref([])
const options = ref(['Skateboard', 'Inline', 'Quad'])
const value = ref('Skateboard')
const selectedEventYear = ref(null)

const fetchAndSetEvent = (year) => {
    if (!year) return
    console.log(`Fetching event data for year: ${year}`)
    fetchEventByYear(year)
        .then((response) => {
            event.value = response
            selectedEventYear.value = parseInt(year, 10) // Ensure dropdown is in sync
        })
        .catch((error) => {
            console.error(error)
            // Maybe redirect to a 404 page or show an error message
        })
}

// Watch for changes in the dropdown selection
watch(selectedEventYear, (newYear) => {
    if (newYear && newYear !== parseInt(props.year, 10)) {
        router.push({ name: 'EventByYear', params: { year: newYear } })
    }
})

// Watch for changes in the route parameter (via props)
watch(() => props.year, (newYear) => {
    fetchAndSetEvent(newYear)
}, { immediate: true }) // `immediate: true` runs the watcher on component load

// Initial load of all events for the dropdown
fetchAllEvents()
    .then((response) => {
        eventList.value = response
        if (!props.year) {
            // If no year is in the URL, find the most recent one and redirect.
            const years = (response || []).map((evt) => new Date(evt.date).getFullYear())
            if (years.length) {
                const mostRecent = Math.max(...years)
                router.replace({ name: 'EventByYear', params: { year: mostRecent } })
            }
        }
    })
    .catch((error) => {
        console.error(error)
    })


// Filter performances by sport regarding the value of the SelectButton
const filteredPerformances = computed(() => {
    if (!event.value || !Array.isArray(event.value.performances)) return []
    return event.value.performances.filter((performance) =>
        performance.sport.toLowerCase().includes(value.value.toLowerCase()),
    )
})

const eventListOptions = computed(() => {
    return eventList.value.map((evt) => {
        const dateObj = new Date(evt.date)
        return {
            label: `${evt.track.city} ${dateObj.getFullYear()}`,
            value: dateObj.getFullYear(),
        }
    })
})

const rows = computed(() => (event.value && Array.isArray(event.value.performances) ? event.value.performances : []))
</script>

<template>
    <div class="p-4">
        <div class="flex items-center justify-center pb-4 gap-5">
            <Select v-model="selectedEventYear" :options="eventListOptions" optionLabel="label" optionValue="value"
                placeholder="Select an Event" class="w-full md:w-56"></Select>

            <div class="card flex justify-center">
                <SelectButton v-model="value" :options="options" />
            </div>
        </div>

        <DataTable :value="filteredPerformances" sortMode="multiple" tableStyle="{}">
            <Column header="#">
                <template #body="slotProps">
                    {{ (slotProps.rowIndex ?? slotProps.index ?? 0) + 1 }}
                </template>
            </Column>
            <Column field="athlete.name" header="Athlete" sortable></Column>
            <Column field="age_group" header="Age Group" sortable></Column>
            <Column field="category" header="Category" sortable></Column>
            <Column field="sport" header="Sport" sortable></Column>
            <Column field="total_laps" header="Laps" sortable></Column>
            <Column field="total_km" header="KM" sortable></Column>
            <Column field="total_miles" header="Miles" sortable></Column>
            <Column field="total_time_hhmmss" header="Time" sortable></Column>
        </DataTable>
    </div>
</template>

<style scoped></style>
