<template>
  <form @submit.prevent="handleSubmit" class="custom-form">
    <div>
      <p>Servicio: {{ serviceName }}</p>
    </div>

    <div>
      <p>Descripcion del servicio: {{ description }}</p>
    </div>


    <div>
      <p>Institucion que lo provee: {{ institution }}</p>
    </div>

    <div>
        <label for="description">Descripción del trabajo:</label>
        <textarea v-model="jobDescription" id="description" required maxlength="255"></textarea>
    </div>
  
    <button type="submit">Enviar solicitud</button>

    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>

  </form>
</template>

<script>
import axios from 'axios';
import Swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import { apiClient } from '../api';

export default {
  data() {
    return {
      serviceId: null,
      institution: null,
      description: null,
      serviceName: null,
      jobDescription: null,
    };
  },
  async mounted() {
    if (!localStorage.getItem('token')) {
        Swal.fire({
              title: 'Error',
              text: 'Tenes que iniciar sesion.',
              icon: 'error',
              confirmButtonText: 'Ok',
            }); 
            this.$router.push({ name: 'login' });
      }
    this.serviceId = this.$route.params.serviceId;
    await this.loadServiceInfo();
  },
  methods: {
    async loadServiceInfo() {
      try {
        const response = await apiClient.get(`/api/services/${this.$route.params.serviceId}`);
        this.institution = response.data[0].laboratory;
        this.description = response.data[0].description;
        this.serviceName = response.data[0].name;
      } catch (error) {
        console.error(error);
      }
    },
    async handleSubmit() {
      if (!this.jobDescription){
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Debes agregar una descripcion antes de enviar la solicitud.',
        });
        return;
      }
      const data = {
        service_id: this.serviceId,
        title: this.serviceName,
        creation_date: new Date().toISOString(),
        close_date: '',
        status: 'created',
        description: this.jobDescription,
      };
      try {
        const response = await apiClient.post('/api/me/requests', data);
        Swal.fire({
          icon: 'success',
          title: 'Éxito',
          text: 'Solicitud enviada con éxito',
        }).then(() => {
          this.$router.push({ path: '/myRequests' });
        });

      } catch (error) {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Error al enviar la solicitud',
          }).then(() => {
            this.$router.push({ name: 'home' });
          });
      }
    },
  },
};
</script>

<style scoped>
.custom-form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f4f4f4;
  border: 1px solid #ddd;
  border-radius: 8px;
}

label {
  display: block;
  margin-bottom: 8px;
}

select,
textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

textarea{
  height: 120px;
  resize: none;
  max-height: 200px;
  overflow-y: auto;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
