<script setup lang="ts">
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchAthleteByName, type AthleteProfile } from '@/fetch/fetchAthletes'

const route = useRoute()
const athlete = ref<AthleteProfile | null>(null)

onMounted(async () => {
    const name = route.params.name as string
    athlete.value = await fetchAthleteByName(name)
})
</script>

<template>
    <div class="p-4" v-if="athlete">
        <!-- Athlete info -->
        <div class="mb-6">
            <h1 class="text-2xl font-bold text-yellow-500 mb-2">{{ athlete.name }}</h1>
            <div class="flex gap-6 text-sm flex-wrap">
                <span v-if="athlete.gender"><span class="text-muted-color">Gender:</span> {{ athlete.gender }}</span>
                <span v-if="athlete.city"><span class="text-muted-color">City:</span> {{ athlete.city }}</span>
                <span v-if="athlete.state"><span class="text-muted-color">State:</span> {{ athlete.state }}</span>
                <span v-if="athlete.country"><span class="text-muted-color">Country:</span> {{ athlete.country }}</span>
                <span v-if="athlete.team"><span class="text-muted-color">Team:</span> Yes</span>
            </div>
        </div>

        <!-- Career totals -->
        <div class="flex gap-6 mb-6 flex-wrap">
            <div class="bg-gray-800 rounded-lg p-4 text-center min-w-32">
                <div class="text-2xl font-bold text-yellow-500">{{ athlete.event_count }}</div>
                <div class="text-sm text-muted-color">Events</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4 text-center min-w-32">
                <div class="text-2xl font-bold text-yellow-500">{{ athlete.total_miles }}</div>
                <div class="text-sm text-muted-color">Total Miles</div>
            </div>
            <div class="bg-gray-800 rounded-lg p-4 text-center min-w-32">
                <div class="text-2xl font-bold text-yellow-500">{{ athlete.total_km }}</div>
                <div class="text-sm text-muted-color">Total KM</div>
            </div>
        </div>

        <!-- Performances table -->
        <DataTable :value="athlete.performances" sortMode="multiple" tableStyle="{}">
            <Column field="year" header="Year" sortable />
            <Column field="event_name" header="Event" sortable />
            <Column field="sport" header="Sport" sortable />
            <Column field="category" header="Category" sortable />
            <Column field="total_laps" header="Laps" sortable />
            <Column field="total_miles" header="Miles" sortable />
            <Column field="total_km" header="KM" sortable />
            <Column field="average_speed_mph" header="Avg MPH" sortable />
            <Column field="average_speed_kph" header="Avg KPH" sortable />
            <Column field="total_time_hhmmss" header="Time" sortable />
        </DataTable>
    </div>
</template>

<style scoped></style>
