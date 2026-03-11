<script>
import axios from 'axios';

export default {
  
  components: {
    
  },
  methods: {

    async exportApplications() {

      try {

        const res = await axios.post(`/api/exportapplications/${localStorage.getItem("userid")}`)

        alert(res.data.message)

      } catch (error) {

        console.log(error)
        alert("Export failed")

      }

    }}
}
</script>
<template>
  <!-- <h1>welcome malikk</h1> -->

  <div class="d-flex vh-100% " style="background-color:#f3a7a7;min-height: 100vh;">
    <aside class="p-4 border-end " style="width:200px">
      <div class="sticky-top  pt-4">

      <router-link to="/student/updateprofile" class="btn btn-primary mb-1 w-100 custom-btn ">
        profile
      </router-link>
      <router-link to="/student/dashboard" class="btn btn-primary mb-1 w-100 custom-btn ">
        Dashboard
      </router-link>
      <router-link to="/student/studentapplication" class="btn btn-primary mb-1 w-100 custom-btn mt-3">
        application history
      </router-link>
       <button class="btn btn-primary mb-1 w-100 custom-btn" @click="exportApplications">
          Export Applications CSV
        </button>
      
      
      
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