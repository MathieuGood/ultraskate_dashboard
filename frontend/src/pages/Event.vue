<script setup>

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { ref, computed } from 'vue'
import { fetchEventByYear } from '@/fetch/fetchEvents'

const event = ref(null)
fetchEventByYear(2023).then((response) => {
    console.log('fetchEventByYear response (body):', response)
    console.log('performances length:', Array.isArray(response.performances) ? response.performances.length : 0)
    event.value = response
}).catch((error) => {
    console.error(error)
})

// Parse event.date to a more readable format
const eventYear = computed(() => {
    if (!event.value || !event.value.date) return ''
    const dateObj = new Date(event.value.date)
    return dateObj.getFullYear()
})

const rows = computed(() => (event.value && Array.isArray(event.value.performances)) ? event.value.performances : [])

</script>


<template>
    <div class="p-4">
        <div class="text-xl py-3">
            {{ event ? `${event.track.city} ${eventYear}` : '' }}
        </div>
        <DataTable :value="rows" sortMode="multiple" tableStyle="{}">
            <Column field="athlete.name" header="Athlete" sortable ></Column>
            <Column field="age_group" header="Age Group" sortable ></Column>
            <Column field="category" header="Category" sortable ></Column>
            <Column field="sport" header="Sport" sortable ></Column>
            <Column field="total_laps" header="Laps" sortable ></Column>
            <Column field="total_km" header="KM" sortable ></Column>
            <Column field="total_miles" header="Miles" sortable ></Column>
            <Column field="total_time_hhmmss" header="Time" sortable ></Column>
        </DataTable>
    </div>
</template>


<style scoped></style>
