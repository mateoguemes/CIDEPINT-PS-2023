<template>
  <div class="login-container">
    <h1>Iniciar Sesion</h1>
    <div class="form-container">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">Email:</label>
          <input v-model="email" placeholder="Email" type="email" class="form-input" required>
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input v-model="password" placeholder="Contraseña" type="password" class="form-input" required>
        </div>
        <button type="submit">Iniciar Sesión</button>
      </form>
    </div>

    <div class="google-login-container">
      <button @click="handleGoogleLogin">
        <img src="/google_login_button.png" alt="Iniciar con Google">
      </button>
    </div>
      <a :href="register_url">Registrarse con Google</a>
  </div>
</template>
<script>
import axios from 'axios';
import { apiClient } from '../api';
import Swal from 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import { googleTokenLogin } from "vue3-google-login"

export default {
  data() {
    return {
      email: "",
      password: "",
      register_url: "",
      emailG: ""
    };
  },
  mounted() {
    this.register_url = (window.location.href.includes("localhost")) ? "https://127.0.0.1:5000/register?google=True&portal=True" : "https://admin-grupo18.proyecto2023.linti.unlp.edu.ar/register?google=True&portal=True";
  },
  methods: {
    async handleSubmit() {
      let endpoint = "/api/auth/login_jwt";
      try {
        var data = {
          email: this.email,
          password: this.password
        }
        const response = await apiClient.post(endpoint, data);
        if (response.status === 200) {
          localStorage.setItem("token", response.data.token);
        }
        Swal.fire({
            icon: 'success',
            title: 'Éxito',
            text: 'Inicio de sesión exitoso',
          }).then(() => {
            this.$router.push({ name: `home` });
          });
      }
      catch (error) {
        Swal.fire({
              title: 'Error',
              text: 'Credenciales inválidas.',
              icon: 'error',
              confirmButtonText: 'Ok',
            }); 
            this.$router.push({ name: 'login' });
        console.error(error.message);
      }
    },

    async handleGoogleLogin() {
      try {
        const response = await googleTokenLogin();
        if (response && response.access_token) {
          const token= response.access_token;
          const googleProfileInfo = await this.getGoogleProfileInfo(token);
          if (googleProfileInfo && googleProfileInfo.email) {
            const userEmail = googleProfileInfo.email;
            this.emailG = userEmail;
            this.sendGoogleTokenToServer(response.access_token);
          } else {
            console.error("No se pudo obtener el correo electrónico del perfil del usuario.");
          }
        } else {
          console.error("No se pudo obtener la información del perfil del usuario.");
        }
      } catch (error) {
        console.error(error.message);
      }
    },

    async getGoogleProfileInfo(googleAccessToken) {
      // Obtener información del perfil del usuario utilizando el token de Google
      const response = await axios.get(`https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=${googleAccessToken}`);
      return response.data;
    },

    async sendGoogleTokenToServer(googleAccessToken) {
      let endpoint = "/api/auth/login_jwt_google";
      try {
        const response = await apiClient.post(endpoint, { token: googleAccessToken });
        if (response.status === 200) {
          this.verificarRegistroEnBD()
        }
      } catch (error) {
        console.error("Error al iniciar sesión con Google:", error);
        console.log("Response data:", error.response.data);
      }
    },
    async verificarRegistroEnBD() {
      try {
        const response = await apiClient.post("/api/auth/verificar_registro", {
          email: this.emailG,
        });
        if (response.status === 200) {
          const verificarRegistro = response.data.message === "Usuario registrado en la base de datos";
          if (!verificarRegistro) {
            Swal.fire({
              title: 'Error',
              text: 'Usted No Esta Registrado.',
              icon: 'error',
              confirmButtonText: 'Ok',
            }); 
          } else {
            localStorage.setItem("token", response.data.token);
              Swal.fire({
              icon: 'success',
              title: 'Éxito',
              text: 'Inicio de sesión exitoso',
            }).then(() => {
              this.$router.push({ name: `home` });
            });
          }
        } 
      } catch (error) {
        console.error("Error al verificar registro en la base de datos:", error);
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;

}

.form-container {
  width: 300px;
  margin: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.google-login-container {
  margin-top: 20px;
}

.google-login-container button {
  background: none;
  border: none;
  cursor: pointer;
}

.google-login-container img {
  width: 1000px; /* Cambia el tamaño del botón de Google según tus necesidades */
  max-width: 200px; /* Ajusta el tamaño según tus necesidades */
}

@media (max-width: 600px) {
  .form-container {
    width: 80%;
  }
}
</style>
/*Por lo que encontre vue3-google-login exporta:
  export { callbackTypes_d as CallbackTypes, _default$1 as GoogleLogin, decodeCredential, 
  _default as default, googleAuthCodeLogin, googleLogout, googleOneTap, googleSdkLoaded, googleTokenLogin };"*/