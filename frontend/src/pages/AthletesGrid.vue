<script setup lang="ts">
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import SelectButton from 'primevue/selectbutton'
import InputText from 'primevue/inputtext'
import Chip from 'primevue/chip'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { fetchAllAthletes, type AthleteStats } from '@/fetch/fetchAthletes'

const router = useRouter()

// --- State ---

const athletes = ref<AthleteStats[]>([])
const searchQuery = ref('')
const sportFilter = ref('All')
const genderFilter = ref('All')

const sportOptions = [
    { label: 'All', value: 'All' },
    { label: 'Skateboard', value: 'Skateboard' },
    { label: 'Inline', value: 'Inline' },
    { label: 'Quad', value: 'Quad' },
]

const genderOptions = [
    { label: 'All', value: 'All' },
    { label: 'M', value: 'Male' },
    { label: 'F', value: 'Female' },
    { label: 'NB', value: 'Non-binary' },
]

// --- Data fetching ---

onMounted(async () => {
    athletes.value = await fetchAllAthletes()
})

// --- Filtering ---

const filteredAthletes = computed(() => {
    let result = athletes.value

    if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase()
        result = result.filter(
            (a) =>
                a.name.toLowerCase().includes(q) ||
                a.city.toLowerCase().includes(q) ||
                a.state.toLowerCase().includes(q) ||
                a.country.toLowerCase().includes(q),
        )
    }

    if (sportFilter.value !== 'All') {
        result = result.filter((a) => a.sports.some((s) => s.toLowerCase().includes(sportFilter.value.toLowerCase())))
    }

    if (genderFilter.value !== 'All') {
        result = result.filter((a) => a.gender.toLowerCase() === genderFilter.value.toLowerCase())
    }

    return result
})

const onRowClick = (event: any) => {
    router.push({ name: 'AthleteDetail', params: { name: event.data.name } })
}
</script>

<template>
    <div class="p-4">
        <!-- Toolbar: search + sport filter + gender filter -->
        <div class="flex items-center justify-center pb-4 gap-5 flex-wrap">
            <InputText
                v-model="searchQuery"
                placeholder="Search name, city, state, country..."
                class="w-full md:w-80"
            />

            <SelectButton v-model="sportFilter" :options="sportOptions" optionLabel="label" optionValue="value" />

            <SelectButton v-model="genderFilter" :options="genderOptions" optionLabel="label" optionValue="value" />
        </div>

        <DataTable
            :value="filteredAthletes"
            sortMode="multiple"
            paginator
            :rows="50"
            :rowsPerPageOptions="[50, 100, 200]"
            @row-click="onRowClick"
            class="cursor-pointer"
            tableStyle="{}"
        >
            <Column header="#">
                <template #body="slotProps">
                    {{ (slotProps.index ?? 0) + 1 }}
                </template>
            </Column>
            <Column field="name" header="Name" sortable />
            <Column field="gender" header="Gender" sortable />
            <Column field="city" header="City" sortable />
            <Column field="state" header="State" sortable />
            <Column field="country" header="Country" sortable />
            <Column field="sports" header="Sports" sortable>
                <template #body="slotProps">
                    <div class="flex gap-1 flex-wrap">
                        <Chip v-for="sport in slotProps.data.sports" :key="sport" :label="sport" />
                    </div>
                </template>
            </Column>
            <Column field="event_count" header="Events" sortable />
            <Column field="total_miles" header="Total Miles" sortable />
            <Column field="best_event_miles" header="Best Event Miles" sortable />
            <Column field="team" header="Team" sortable>
                <template #body="slotProps">
                    <i v-if="slotProps.data.team" class="pi pi-check text-green-400" />
                </template>
            </Column>
        </DataTable>
    </div>
</template>

<style scoped></style>
