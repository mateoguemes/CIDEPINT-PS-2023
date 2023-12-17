<template>
<div>
  <div v-if="requests && requests.length"> 
        <form @submit.prevent="handleSubmit" class="full-width-form">

            <label for="sortInput">Ordenar por:</label>
            <select v-model="sortInput" id="sortInput" required>
                <option value="creation_date">Fecha de Creación</option>
                <option value="service_name">Nombre del Servicio</option>
                <option value="current_status">Estado</option>
            </select>

            <label>Orden:</label>
            <div>
                <label>
                    <input type="radio" v-model="sortOrder" name="sortOrder" value="asc" /> Ascendente
                </label>
                <label>
                    <input type="radio" v-model="sortOrder" name="sortOrder" value="desc" /> Descendente
                </label>
            </div>

            <button type="submit">Aceptar</button>
        </form>

    <table class="custom-table">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Descripción</th>
          <th>Estado</th>
          <th>Fecha de Creación</th>
          <th>Detalle</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.service_name }}</td>
          <td>{{ request.description }}</td>
          <td>{{ request.current_status }}</td>
          <td>{{ formatDate(request.creation_date) }}</td>
          <td><router-link :to="{ name: 'request-detail', params: { requestId: request.requirement_id } }">Ver</router-link></td>
        </tr>
      </tbody>
    </table>

    <div>
      <button @click="loadPage(actualPage - 1)" :disabled="actualPage === 1">Anterior</button>
      <span>Página {{ actualPage }} de {{ totalPages }}</span>
      <button @click="loadPage(actualPage + 1)" :disabled="actualPage === totalPages">Siguiente</button>
    </div>
  </div>

  <div v-else>
    <h1>No tenes pedidos, podes elegir un servicio apretando en "Servicios" o presionando <a href="">aqui</a>.</h1>
  </div>
  
</div>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

import { apiClient } from '../api';

export default {
data() {
    return {
    requests: [], 
    sortInput: '',
    sortOrder: '',
    actualPage: 1,
    totalPages: 1,
    };
},

async mounted() {
    await this.loadRequests();
},

methods: {
    async loadRequests() {
    try {
      const response = await apiClient.get(`/api/me/requests?sort=${this.sortInput}&order=${this.sortOrder}&page=${this.actualPage}`);
      this.requests = response.data.data;
      this.actualPage = response.data.page;
      this.totalPages = response.data.total_pages;
    } catch (error) {
        Swal.fire({
          title: 'Error',
          text: 'Debes estar autenticado para ver tus pedidos',
          icon: 'error',
          confirmButtonText: 'Ok',
        }); 
        this.$router.push({ name: 'login' });
      console.error(error);
    }
    },
    async loadPage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.actualPage = page;
        await this.loadRequests();
      }
    },
    async handleSubmit() {
        this.loadRequests();
        this.sortInput = '';
        this.sortOrder = '';
    },
    formatDate(dateString) {
      const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false, // Mostrar en formato de 24 horas
      };
      const formattedDate = new Date(dateString).toLocaleDateString(undefined, options);
      return formattedDate;
    },
    },
};
</script>

<style scoped>
.filter-form {
  margin-bottom: 20px;
}

.full-width-form {
  display: flex;
  width: 55%;
}

.full-width-form label {
  flex: 1;
  margin-right: 10px;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.custom-table th, .custom-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.custom-table th {
  background-color: #f4f4f4;
}

.custom-table tr:hover {
  background-color: #f9f9f9;
}

@media (min-width: 768px) {
  .filter-form {
    width: 48%;
  }

  .custom-table {
    width: 48%;
  }

  .full-width-form {
    width: 100%;
  }
}
</style>
  