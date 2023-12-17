<script setup>
import RequestForm from '../components/RequestForm.vue';
</script>

<template>
  <main>
    <div class="form">
      <RequestForm />
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
