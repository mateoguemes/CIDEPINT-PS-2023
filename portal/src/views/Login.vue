<script setup>
import LoginForm from '../components/LoginForm.vue'
</script>

<template>
  <main>
    <div class="login">
      <LoginForm/>
    </div>
  </main>
</template>

<style>
@media (min-width: 1024px) {
  .login {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>