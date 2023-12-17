import axios from "axios";

/*fuete: RequestForm*/
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_APP_API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem('token'),
  },
});

apiClient.interceptors.request.use((config) => {
  config.headers['Authorization'] = 'Bearer ' + localStorage.getItem('token');
  return config;
});

export { apiClient };
