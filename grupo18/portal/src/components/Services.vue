<template>
    <div>
      <div class="filter-form">
          <form @submit.prevent="handleSubmit" class="full-width-form">
              <div>
              <label for="textInput">Buscar por nombre</label>
                  <input type="text" v-model="textInput" id="textInput" name="textInput" />
              </div>
              <div>
                <label for="typeInput">Filtar por tipo:</label>
                <select id="typeInput" v-model="typeInput">
                  <option v-for="(type, index) in serviceTypes" :key="index" :value="type">{{ type }}</option>
                </select>
              </div>
              <button type="submit">Filtrar</button>
          </form>
          <button class="" @click="loadAllServices">Limpiar filtros</button>
      </div>
 
 
      <div v-if="services && services.length">
        <table class="custom-table">
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Descripción</th>
              <th v-if="filterApplied">Coindidencias en</th>
              <th>Ver más</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="services.length === 1">
              <td>{{ services[0].service.name }}</td>
              <td>{{ services[0].service.description }}</td>
              <td v-if="filterApplied">{{ services[0].match }}</td>
              <td>
                <router-link :to="{ name: 'service-detail', params: { id: services[0].service.id }}">Ver más</router-link>
              </td>
            </tr>
            <tr v-else v-for="(serviceItem, index) in services" :key="index">
              <td>{{ serviceItem.service.name }}</td>
              <td>{{ serviceItem.service.description }}</td>
              <td v-if="filterApplied">{{ serviceItem.match }}</td>
              <td>
                <router-link :to="{ name: 'service-detail', params: { id: serviceItem.service.id }}">Ver más</router-link>
              </td>
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
        <h1>No hay servicios activos aún.</h1>
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
        services: [],
        textInput: "",
        typeInput: null,
        perPage: null,
        actualPage: 1,
        totalPages: 0,
        totalElements: 1,
        serviceTypes: [],
        filterApplied: false,
        };
    },
 
 
    async mounted() {
        var api_response = await apiClient.get("/api/services-types/");
        this.serviceTypes = api_response.data.data;
        await this.loadAllServices();
        this.totalPages = (this.totalElements > this.perPage) ? Math.ceil(this.totalElements / this.perPage) : 1;
    },
    methods: {
        async loadAllServices() {
        try {
        const response = await apiClient.get(`/api/services/index?page=${this.actualPage}`);
        this.services = response.data.data;
        this.actualPage = response.data.page;
        this.totalElements = response.data.total;
        this.perPage = response.data.per_page;
        } catch (error) {
        if (error.response.status === 400){
            Swal.fire({
                title: 'Error',
                text: 'Parámetros inválidos',
                icon: 'error',
                confirmButtonText: 'Ok',
            });
            this.$router.push({ name: 'home' });
          }
        }
        },
        async handleSubmit (){
          var response;
          this.filterApplied = !(this.textInput === "" || this.textInput === null) && this.typeInput !== null
          try{
            if(this.typeInput){
              if(this.textInput !== null && this.textInput !== "")
                response = await apiClient.get(`/api/services/search_advanced?q=${this.textInput}&type=${this.typeInput}&page=${this.actualPage}`);
              else{
                response = await apiClient.get(`/api/services/search_by_type?q=${this.typeInput}&page=${this.actualPage}`);
              }
            }
            else{
              response = await apiClient.get(`/api/services/search_advanced?q=${this.textInput}&page=${this.actualPage}`);
            }
            this.services = response.data.data;
          }
          catch (error) {
            if (error.response.status === 400){
                Swal.fire({
                    title: 'Error',
                    text: 'El nombre es obligatorio para la búsqueda',
                    icon: 'error',
                    confirmButtonText: 'Ok',
                });
            }
          }
        },
        async loadPage(page) {
        if (page >= 1 && page <= (this.totalPages)) {
            this.actualPage = page;
            if(this.textInput == "" && this.typeInput== ""){
                await this.loadAllServices();
            }
            else{
                await this.handleSubmit();
            }
        }
      },
    },
 }
 
 
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
 .filter-form {
  width: 50%;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-bottom: 20px;
 }
 
 
 .filter-form label, .filter-form select, .filter-form input, .filter-form button {
  margin-bottom: 10px;
  display: block;
 }
 
 
 .full-width-form {
  width: 100%;
  box-sizing: border-box;
 }
 
 
 .full-width-form label {
  display: block;
  margin-bottom: 5px;
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
 
 
 .filter-form form {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
 }
 
 
 .filter-form div {
  flex: 1 1 calc(50% - 10px);
  margin-bottom: 10px;
  margin-right: 10px;
 }
 
 
 .filter-form select, .filter-form input, .filter-form button {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
 }
 
 
 .filter-form button {
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
 }
 
 
 .filter-form button:hover {
  background-color: #45a049;
 }
 
 
 .filter-form button:disabled {
  background-color: #dddddd;
  cursor: not-allowed;
 }
 </style>
 
 
 
 
 