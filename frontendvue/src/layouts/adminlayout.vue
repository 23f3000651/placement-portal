<script>
// import Navbar from "@/componets/admin/AdminNavbar.vue";

export default {
  // name:'APP',
  components: {
    // HelloWorld,login,
    // Navbar
  }
}
</script>
<template>
  <!-- <h1>welcome malikk</h1> -->

  <div class="d-flex vh-100% " style="background-color:#f3a7a7;min-height: 100vh;">
    <aside class="p-4 border-end " style="width:200px">
      <div class="sticky-top  pt-4">

      <router-link to="/admin/dashboard" class="btn btn-primary mb-1 w-100 custom-btn ">
        Dashboard
      </router-link>
      <router-link to="/admin/companyaplication" >
        <button class="btn btn-primary w-100 custom-btn mb-1 ">company aplication</button>

        <!-- <button class="btn btn-primary mb-1 w-100 rounded-top-left">Departments</button> -->
      </router-link>
      <router-link to="/admin/studetnapplication" >
        <button class="btn btn-primary w-100 custom-btn mb-1 ">stuent application</button>

        <!-- <button class="btn btn-primary mb-1 w-100 rounded-top-left">Departments</button> -->
      </router-link>
      <router-link to="/" class="btn btn-primary mb-1 w-100 custom-btn ">
        logout
      </router-link>

      
      </div>

    </aside>




    <main class="p-4 flex-fill " style="background-color: antiquewhite;">



      
      <router-view />
    </main>
  </div>
</template>
<style scoped>
.custom-btn {
  border-top-right-radius: 30px;
  
}

.custom-btn:hover{
  background-color: #182c49;  
  transform: translateX(35px);
}

</style>