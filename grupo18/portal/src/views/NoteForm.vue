<script setup>
import NoteForm from '../components/NoteForm.vue';
</script>

<template>
  <main>
    <div class="form">
      <NoteForm />
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
