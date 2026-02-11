<script setup>
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { ref, computed, watch } from 'vue'
import { fetchEventByYear, fetchAllEvents } from '@/fetch/fetchEvents'
import SelectButton from 'primevue/selectbutton'
import Select from 'primevue/select'

const event = ref(null)
const eventList = ref([])
const options = ref(['Skateboard', 'Inline', 'Quad'])
const value = ref('Skateboard')
const selectedEventYear = ref(null)

fetchAllEvents()
    .then((response) => {
        eventList.value = response
        // set the selected event year to the most recent year available
        const years = (response || []).map((evt) => new Date(evt.date).getFullYear())
        if (years.length) {
            const mostRecent = Math.max(...years)
            selectedEventYear.value = mostRecent
        }
    })
    .catch((error) => {
        console.error(error)
    })

const fetchAndSetEvent = (year) => {
    fetchEventByYear(year)
        .then((response) => {
            console.log('fetchEventByYear response (body):', response)
            console.log('performances length:', Array.isArray(response.performances) ? response.performances.length : 0)
            event.value = response
        })
        .catch((error) => {
            console.error(error)
        })
}

// initial load
fetchAndSetEvent(selectedEventYear.value)

// refetch when the selected event year changes
watch(selectedEventYear, (newYear) => {
    if (newYear) fetchAndSetEvent(newYear)
})

// Filter performances by sport regarding the value of the SelectButton
const filteredPerformances = computed(() => {
    if (!event.value || !Array.isArray(event.value.performances)) return []
    return event.value.performances.filter((performance) =>
        performance.sport.toLowerCase().includes(value.value.toLowerCase()),
    )
})

// Parse event.date to a more readable format
const eventYear = computed(() => {
    if (!event.value || !event.value.date) return ''
    const dateObj = new Date(event.value.date)
    return dateObj.getFullYear()
})

const eventListOptions = computed(() => {
    return eventList.value.map((evt) => {
        const dateObj = new Date(evt.date)
        return {
            // show city and year (e.g. "Miami — 2023") but keep value as year
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
            <Select
                v-model="selectedEventYear"
                :options="eventListOptions"
                optionLabel="label"
                optionValue="value"
                placeholder="Select an Event"
                class="w-full md:w-56"
            ></Select>

            <div class="card flex justify-center">
                <SelectButton v-model="value" :options="options" />
            </div>
        </div>

        <DataTable :value="filteredPerformances" sortMode="multiple" tableStyle="{}">
            <Column header="Position">
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
