<script setup>
import RequestDetail from '../components/RequestDetail.vue';
</script>

<template>
  <main>
    <div class="form">
      <RequestDetail />
    </div>
  </main>
</template>

<style>
@media (min-width: 1024px) {
  .form {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
