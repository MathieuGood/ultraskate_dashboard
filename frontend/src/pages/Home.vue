<script setup>
import { ref } from 'vue'
import Header from '@/components/Header.vue'
import Athlete from '@/pages/Athlete.vue'
import Event from '@/pages/Event.vue';

const title = ref("Ultraskate Dashboard")

</script>

<template>
    <div class="w-screen h-screen bg-gray-400">
        <Header></Header>
        <Event></Event>
        <Athlete></Athlete>
    </div>
</template>

<style scoped></style>
