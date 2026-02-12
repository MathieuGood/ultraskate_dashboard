<script setup lang="ts">
import { ref } from 'vue'

const title = ref('Ultraskate Dashboard')
</script>

<template>
  <div class="p-4">
    <h1 class="text-3xl font-bold mb-4">Welcome to the Ultraskate Dashboard!</h1>
    <p class="mb-4">Explore event data and athlete performances.</p>
    <router-link to="/event" class="text-blue-500 hover:underline">Go to Event Page</router-link>
  </div>
</template>

<style scoped></style>