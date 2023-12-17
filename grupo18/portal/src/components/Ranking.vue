<template>
        <div class="col-md-4 mb-4">
            <div class="card">
                <div class="card-body">
                    <h4>Servicios más solicitados</h4>
                    <div v-if="data">
                        <Bar :data="data" :options="options"/>
                    </div>
                </div>
            </div>
        </div>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
    
</template>

<script lang="ts">

    import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
    import { Bar } from 'vue-chartjs';
    import { apiClient } from '../api';
    import axios from 'axios';
  
    ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

    export default {
        components: {
            Bar
        },
        data() {
            return {
                data: null,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                },
            };
        },

        async mounted() {
            await this.loadRequests();
        },

        methods: {
            async loadRequests() {
                try {
                    const response = await apiClient.get(`/api/requirements/servicesQuantities`);
                    let result = response.data.data;

                    let dataset = [{
                        label: 'Solicitudes realizadas',
                        backgroundColor: '#f87979',
                        data: Object.values(result)
                    }]

                    this.data = {
                        labels: Object.keys(result),
                        datasets: dataset
                    };
                }
                catch (error) {
                    console.error(error);
                }
            }
        },
    };
    
</script>