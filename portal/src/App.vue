<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { apiClient } from './api';
import { ref, onMounted } from 'vue';
import Swal from 'sweetalert2';
const token = ref(localStorage.getItem('token'));
const router = useRouter();

const logout = async () => {
  if (token.value) {
    await apiClient.get(`/api/auth/logout_jwt`);
    localStorage.removeItem('token');
    Swal.fire({
              icon: 'success',
              title: 'Éxito',
              text: 'Cierre de Sesión exitoso',
            }).then(() => {
              window.location.reload();
            });
  }
};

const login = () => {
  router.push({ name: 'login' });
};

onMounted(() => {
  window.addEventListener('storage', () => {
    token.value = localStorage.getItem('token');
  });
});
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="../public/logo.png" width="125" height="125" />

    <div class="wrapper">
      <div class="text">
        <h1 class="green">CIDEPINT</h1>
        <h3>
          Centro de Investigación y Desarrollo en Tecnología de Pinturas y Recubrimientos
        </h3>
      </div>
      <nav>
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/services">Servicios</RouterLink>
        <RouterLink to="/myRequests">Pedidos</RouterLink>
        <RouterLink to="/Statistics">Estadisticas</RouterLink>
      </nav>
      <div v-if="token">
        <button @click="logout">Cerrar Sesion</button>
      </div>
      <div v-else>
        <button @click="login">Iniciar Sesion</button>
      </div>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}

h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
  text-align: center;
}

h3 {
  font-size: 1.2rem;
  text-align: center;
}

.text h1,
.text h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .text h1,
  .text h3 {
    text-align: left;
  }
}
</style>
