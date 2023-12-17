<template>
    <form @submit.prevent="handleSubmit" class="custom-form">    
      <div>
          <label for="description">Descripción del trabajo:</label>
          <textarea v-model="noteText" id="description" required maxlength="255"></textarea>
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
        noteText: '',
        request_id: '',
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
        this.request_id = this.$route.params.requestId;
    },
    methods: {
      async handleSubmit() {
        if (this.noteText == '') {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Debes completar el campo.',
          });
          return;
        }
        const data = {
          text: this.noteText,
          requirement_id: this.request_id,
        };
  
        try {
          const response = await apiClient.post('/api/me/requests/addNote', data);
          Swal.fire({
            icon: 'success',
            title: 'Éxito',
            text: 'Nota enviada con éxito',
          }).then(() => {
            this.$router.push({ path: `/notes/${this.request_id}` });
          });
  
        } catch (error) {
            Swal.fire({
              title: 'Error',
              text: 'Error al cargar la nota.',
              icon: 'error',
              confirmButtonText: 'Ok',
            }); 
            this.$router.push({ name: 'home' });
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
  