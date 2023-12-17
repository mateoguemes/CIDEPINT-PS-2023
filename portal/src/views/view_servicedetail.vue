<template>
    <div>
      <ServiceDetail :id="id" />
    </div>
  </template>
  
  <script>
  import ServiceDetail from '../components/servicedetail.vue';
  
  export default {
    components: {
      ServiceDetail,
    },
    data() {
      return {
        id: null,
      };
    },
    beforeRouteEnter(to, from, next) {
      const id = to.params.id;
      next(vm => (vm.id = id));
    },
  };
  </script>
  
  
  
  