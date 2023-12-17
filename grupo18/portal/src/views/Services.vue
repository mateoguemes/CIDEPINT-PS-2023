<script setup>
import Services from '../components/Services.vue';
</script>


<template>
   <main>
     <div class="services">
       <Services />
     </div>
   </main>
 </template>
  <style>
 @media (min-width: 1024px) {
   .services {
     min-height: 100vh;
     display: flex;
     align-items: center;
   }
 }
 </style>