<script setup></script>

<template>
  <div class="bg-surface-900 p-2 px-4 flex justify-between items-center border-b border-surface">
    <div class="text-xl text-yellow-500">Ultraskate Dashboard</div>
    <nav class="flex gap-4">
      <router-link to="/" class="text-surface-0 hover:text-primary">Home</router-link>
      <router-link to="/event" class="text-surface-0 hover:text-primary">Grid</router-link>
      <router-link to="/athletes" class="text-surface-0 hover:text-primary">Athletes</router-link>
      <router-link to="/event/graph" class="text-surface-0 hover:text-primary">Graph</router-link>
    </nav>
  </div>
</template>

<style scoped></style>
