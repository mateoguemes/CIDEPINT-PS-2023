import "./assets/main.css"
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import vue3GoogleLogin from "vue3-google-login";

const app = createApp(App);

app.use(vue3GoogleLogin, { clientId: import.meta.env.VITE_APP_GOOGLE_CLIENT_ID});
//780750903019-3i8g5h149245421pkc1svrbosk0f4qes.apps.googleusercontent.com

app.use(createPinia());
app.use(router);
app.mount('#app');
