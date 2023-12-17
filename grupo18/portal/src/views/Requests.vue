<script setup>
import Requests from '../components/Requests.vue';
</script>

<template>
  <main>
    <div class="requests">
      <Requests />
    </div>
  </main>
</template>

<style>
@media (min-width: 1024px) {
  .requests {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>