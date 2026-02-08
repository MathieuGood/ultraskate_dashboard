<script setup lang="ts">


import { ref } from 'vue'
import Header from './components/Header.vue';

const title = ref("Ultraskate Dashboard")


</script>

<template>
  <Header />
  <div class="bg-red-300">
    {{ title }}
  </div>
</template>

<style scoped></style>
