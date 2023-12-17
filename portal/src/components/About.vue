<script setup>
import AboutItem from './AboutItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
</script>

<template>
  <AboutItem>
    <template #icon>
      <img alt="search icon" src="/manos.png" width="32" height="32">
    </template>
    <template #heading>Servicios</template>
    CIDEPINT cuenta con un sistema de registro de instituciones para que las mismas puedan ofrecer al público sus servicios.
    De esta forma, y através de este portal, podés visualizar un listado de todos los servicios ofrecidos por las instituciones.
  </AboutItem>

  <AboutItem>
    <template #icon>
      <img alt="search icon" src="/lupa.png" width="32" height="32">
    </template>
    <template #heading>Búsqueda</template>
    Mediante una búsqueda por título, descripción, nombre de institución, tipo de servicio, o palabras claves,
    podés realizar una búsqueda para encontrar el servicio que más se ajuste a tu necesidad.
  </AboutItem>

  <AboutItem>
    <template #icon>
      <img alt="search icon" src="/pincel.png" width="32" height="32">
    </template>
    <template #heading>Solicitudes</template>
    Si encontraste un servicio que cumple con tus expectativas, podés realizar una solicitud del mismo a la institución.
    Luego de completar un formulario simple, se envía una solicitud a la institución para que ésta la gestione y se ponga en contacto con vos.
  </AboutItem>

  <AboutItem>
    <template #icon>
      <CommunityIcon />
    </template>
    <template #heading>Pedidos</template>
    También podés revisar tus pedidos realizados, filtrarlos y responder a los comentarios que el administrador de la institución te haya dejado.
  </AboutItem>
</template>
