<script setup></script>

<template>
  <!-- <nav class=" avbar-expand-lg"><router-link to="/" class="btn btn-primary m-1 mt-3 w-50  " v-if ="$route.path !== '/'">
        logout
      </router-link>
      </nav> -->
<nav class="navbar navbar-expand-lg bg-light">
  <div class="container-fluid">

    
    <div class="ms-auto">
      <router-link
        to="/"
        class="btn btn-primary"
        v-if="$route.path !== '/'"
      >
        Logout
      </router-link>
    </div>

  </div>
</nav>
  <router-view />
</template>

<style scoped>

</style>
