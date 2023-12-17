<script setup>
    import CakeGraph from '../components/CakeGraph.vue';
    import Ranking from '../components/Ranking.vue';
    import Top10 from '../components/Top10.vue'
</script>

<template>
    <main>
        <div class="container mt-4 bg-white">
            <div class="statistics container mt-5 mb-5 custom-background p-4" style="justify-content: center">
                <CakeGraph />
                <Ranking />
                <Top10 /> 
            </div>
        </div>
    </main>
</template>

<style>
    @media (min-width: 1024px) {
    .statistics {
        min-height: 100vh;
        display: flex;
        align-items: center;
    }
    }

    @media (min-width: 1024px) {
    .statistics {
        min-height: 100vh;
        display: flex;
        align-items: center;
    }
    }
    
    .custom-background {
            background-color: #f2f2f2; 
            border-radius: 10px; 
    }
</style>