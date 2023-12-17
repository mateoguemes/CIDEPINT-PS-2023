<template>
    <h1>¿Querés contactarte con nosotros?</h1>
    <ContactItem>
        <template #icon>
            <img alt="search icon" src="/sobre.png" width="32" height="32">
        </template>
        <template #contactWay>Correo electrónico</template>
        <div v-if="data">
            Podés enviarnos un correo electrónico con tus dudas o sugerencias a <a href="mailto:{{ data }}">{{ data }}</a>.
        </div>
    </ContactItem>
</template>

<script lang="ts">
    import { apiClient } from '../api';
    import ContactItem from './ContactItem.vue';
    
    export default {
        data() {
            return {
                data: ""
            }
        },

        async mounted() {
            await this.loadRequests();
        },

        methods: {
            async loadRequests() {
                try {
                    const response = await apiClient.get('/api/config/contactMail');
                    let result = response.data;

                    this.data = result['mail']
                }
                catch (error) {
                    console.error(error);
                }
            }
        },
    }
</script>