<template>
  <div>
    <section id="service-details">
      <h2>Información del Servicio</h2>
      <div class="details-container">
        <div class="info">
          <template v-if="service">
            <p>Nombre del Servicio: {{ service.name }}</p>
            <p>Descripción: {{ service.description }}</p>
          </template>
          <br>
          <h2>Institución que brinda el servicio</h2>
          <template v-if="institution">
            <p>Nombre de la Institución: {{ institution.name }}</p>
            <p>Dirección: {{ institution.address }}</p>
          </template>              
        </div>
        <div class="map-container">
          <form @submit.prevent="requestService">
            <button type="submit" class="request-button">Solicitar</button>
          </form>
          <br>
          <h2 class="detailmaps">¿Cómo llegar?</h2>
          <div id="map" class="leaflet-map"></div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-control-geocoder/dist/Control.Geocoder.css';
import 'leaflet-control-geocoder/dist/Control.Geocoder.js';
import { apiClient } from '../api';

export default {
  data() {
    return {
      service: null,
      institution: null,
      isAuthenticated: false,
    };
  },
  watch: {
    $route(newRoute, oldRoute) {
      if (newRoute.params.id !== oldRoute.params.id) {
        this.fetchServiceDetails();
      }
    },
  },
  mounted() {
    this.isAuthenticated = !!localStorage.getItem('token');
    this.fetchServiceDetails();
  },
  methods: {
    async fetchServiceDetails() {
      try {
        const serviceId = this.$route.params.id;
        const serviceResponse = await apiClient.get(`/api/services/${serviceId}`);
        const institutionResponse = await apiClient.get(`/api/institution-for-service/${serviceId}`)
        this.service = serviceResponse.data && serviceResponse.data.length > 0 ? serviceResponse.data[0] : null;
        this.institution = institutionResponse.data;
        if (this.service && this.institution) {
          this.initializeMap();
        }
      } catch (error) {
        console.error('Error al obtener detalles del servicio', error);
      }
    },
    initializeMap() {
      console.log('COORDENADAS DE LA UBICACION',this.institution.location)
      var coordinates = this.institution.location.split(',').map(coord => parseFloat(coord));
      if (!isNaN(coordinates[0]) && !isNaN(coordinates[1])) {
        var map = L.map('map').setView(coordinates, 15);
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        var defaultIcon = new L.Icon.Default();
        
        L.marker(coordinates, { icon: defaultIcon }).addTo(map)
          .bindPopup(`<b>${this.institution.name}</b><br>${this.institution.days_and_opening_hours}<br>${this.institution.email}`)
          .openPopup();
        
        L.Control.geocoder().addTo(map);
      } else {
        console.error('Coordenadas no válidas:', coordinates);
      }
    },
    requestService() {
      const service_id = this.$route.params.id;
      if (!this.isAuthenticated) {
        this.$router.push({ name: 'login' });
      } else {
        console.log('Solicitud de servicio enviada correctamente');
        this.$router.push({ name: 'request', params: { serviceId: service_id } });
      }
    },
  },
};
</script>

<style scoped>
#service-details {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.detailmaps{
  text-align: center;
}
.details-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.info {
  width: 100%;
  margin-bottom: 20px;
}

.map-container {
  width: 100%;
}

.leaflet-map {
  height: 200px;
  width: 100%;
}

.request-button {
  display: block;
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 2px solid #000;
  border-radius: 5px;
  background-color: #c7c5c5;
  color: #000;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.request-button:hover {
  background-color: rgba(11, 19, 250, 0.973)}

@media (min-width: 768px) {
  .info {
    width: 48%;
  }

  .map-container {
    width: 48%;
  }
}
</style>