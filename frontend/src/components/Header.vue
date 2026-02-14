<script setup></script>

<template>
  <div class="bg-gray-900 p-2 px-4 flex justify-between items-center">
    <div class="text-xl text-yellow-500">Ultraskate Dashboard</div>
    <nav class="flex gap-4">
      <router-link to="/" class="text-white hover:text-yellow-300">Home</router-link>
      <router-link to="/event" class="text-white hover:text-yellow-300">Grid</router-link>
      <router-link to="/event/graph" class="text-white hover:text-yellow-300">Graph</router-link>
    </nav>
  </div>
</template>

<style scoped></style>
