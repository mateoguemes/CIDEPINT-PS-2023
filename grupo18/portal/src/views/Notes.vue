<script setup>
import Notes from '../components/Notes.vue';
</script>

<template>
  <main>
    <div class="notes">
      <Notes />
    </div>
  </main>
</template>

<style>
@media (min-width: 1024px) {
  .notes {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>