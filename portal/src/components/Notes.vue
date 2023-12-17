<template>
  <div v-if="notes.length">
    <router-link :to="{ name: 'request-detail', params: { requestId: request_id } }">Volver al detalle del servicio</router-link>
    <table class="note-table">
      <thead>
        <tr>
          <th>Emisor</th>
          <th>Texto</th>
          <th>Fecha de Inserción</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="note in notes" :key="note.id">
          <td>{{ note.from_laboratory ? 'Laboratorio' : 'Cliente'}}</td>
          <td>{{ note.text }}</td>
          <td>{{ formatDate(note.inserted_at) }}</td>
        </tr>
      </tbody>
    </table>
    <router-link :to="{ name: 'noteForm', params: { requestId: request_id } }" class="add-note-link">Agregar nota</router-link>
  </div>
  <p v-else>
    Todavia no hay notas para esta solicitud. Agregá una haciendo click <router-link :to="{ name: 'noteForm', params: { requestId: request_id } }">acá</router-link>.
  </p>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import { apiClient } from '../api';

export default {
  data() {
    return {
      notes: [],
      request_id: null,
    };
  },

  async mounted() {
    this.request_id = this.$route.params.requestId
    await this.loadNotes();
  },

  methods: {
    async loadNotes() {
      try {
        const response = await apiClient.get(`/api/me/requests/${this.request_id}/notes`);
        this.notes = response.data;
      } catch (error) {
          Swal.fire({
            title: 'Error',
            text: 'No tienes permisos para ver las notas de esta solicitud',
            icon: 'error',
            confirmButtonText: 'Ok',
          }); 
          this.$router.push({ name: 'home' });
        console.error(error);
      }
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
.note-table {
  border-collapse: collapse;
  table-layout: fixed;
  width: 100%;
  max-width: 600px;
  margin-top: 20px;
}

.note-table th,
.note-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.note-table th {
  background-color: #f2f2f2;
}

.add-note-link {
  display: inline-block;
  margin-top: 10px;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

p {
  margin-top: 20px;
}

p router-link {
  color: #4caf50;
  text-decoration: none;
  font-weight: bold;
}
</style>
