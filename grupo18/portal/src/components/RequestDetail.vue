<template>
    <div v-if="request">
      <div class="details-container">
        <router-link :to="{ name: 'service-detail', params: { id: request.service_id } }" class="view-service-link">Más detalles sobre el servicio</router-link>
        <h1>Nombre del servicio: {{ request.service_name }}</h1>
        <div class="request-details">
            <div>
                <strong>Descripción del servicio:</strong> {{ request.description }}
            </div>
            <div>
                <strong>Detalle del cliente:</strong> {{ request.client_description }}
            </div>
            <div>
                <strong>Fecha de peticion:</strong> {{ formatDate(request.creation_date) }}
            </div>
            <div>
                <strong>Fecha de cierre:</strong> {{ request.close_date ? formatDate(request.close_date) : 'No se ha cerrado' }}
            </div>
            <div>
                <strong>Estado:</strong> {{ request.current_status }}
            </div>
            <div>
                <strong>Observacion sobre el estado:</strong> {{ request.observation }}
            </div>
        </div>
        <router-link :to="{ name: 'notes', params: { requestId: request_id } }" class="view-notes-link">Ver notas</router-link>
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
      request_id: null,
      request: null,
    };
  },

  async mounted() {
    this.request_id = this.$route.params.requestId
    await this.loadNotes();
  },

  methods: {
    async loadNotes() {
      try {
        const response = await apiClient.get(`/api/me/requests/${this.request_id}`);
        this.request = response.data.data;
      } catch (error) {
          Swal.fire({
            title: 'Error',
            text: 'No podes ver esta solicitud',
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
.details-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.request-details {
  margin-top: 20px;
}

.request-details div {
  margin-bottom: 10px;
}

.request-details strong {
  margin-right: 5px;
}

.view-service-link,
.view-notes-link {
  display: inline-block;
  margin-top: 10px;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.view-notes-link {
  background-color: transparent;
  border: 2px solid #4caf50;
  color: #4caf50;
}
</style>