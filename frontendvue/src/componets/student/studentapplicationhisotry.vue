<script>
// import router from '@/routes';
import axios from 'axios';
// import Detailsofdrivestudent from './detailsofdrivestudent.vue';

export default {
  data() {
    return {
      msg: '',
      details: {
        company: {},
        drive: {}
      }
      , aplicationlist: [],
      interviewlist: [],
      showDetails: false
      // drive:[]



    }

  },
  mounted() {
    this.user_id = localStorage.getItem('userid')
    this.getstudetails(this.user_id)
    this.getinterview(this.user_id)


  }
  , methods: {
    async getstudetails(user_id) {
      const res = await axios.get(`/api/studentdata/${user_id}`)
      const data = res.data

      this.aplicationlist = data.applicationlist
      this.studentid = data.studentid
      localStorage.setItem('student_id', data.student_id)

      // console.log(res.data)

    }, async getinterview(id) {

      const res = await axios.get(`/api/supcominginterview/${id}`, this.data)
      const result = res.data;
      this.msg = result.msg;
      
      this.interviewlist = result.intervielist
      // console.log(result)
    },
    async Detailofapplication(id) {
      const res = await axios.get(`/api/detailofapplication/${id}`)
      const data = res.data

      this.details = res.data
      this.showDetails = true
    },
    closeDetails() {
      this.details = null
      this.showDetails = false
    }

  }
}
</script>

<template>
  <!-- {{ aplicationlist }} -->
    <h2 class="text-center">application history</h2>

  <div class="container mt-4">

    <div class="row g-2">

      <div class="col-md-4" v-for="application in aplicationlist" :key="application.id">
        <div class="card h-100 shadow-sm">

          <div class="card-body d-flex flex-column">

            <h5 class="card-title mb-3">
              aplication_id: {{ application.id }}
            </h5>
            <h5 class="card-title mb-3">
              drive_id: {{ application.drive_id }}
            </h5>


            <p class="card-text mb-4">
              Status:
              <span class="badge" :class="application.status === 'Applied'
                ? 'bg-success'
                : 'bg-warning text-dark'">
                {{ application.status }}
              </span>
            </p>

            <div class="mt-auto">
              <button class="btn btn-primary btn-sm w-100" @click="Detailofapplication(application.id)">
                View Details
              </button>
            </div>

          </div>

        </div>
      </div>

    </div>

  </div>
  <!-- {{ details }} -->
  <div v-if="showDetails" class="container mt-4 w-50">

    <div class="card ">
      <div class="card-header d-flex justify-content-between">
        <h5 class="mb-0">Company & Drive Details</h5>
        <button class="btn btn-danger btn-sm" @click="closeDetails">
          Close
        </button>
      </div>

      <div class="card-body">


        <h6 class="fw-bold">Company Info</h6>
        <p><strong>Name:</strong> {{ details.company.compnayname }}</p>
        <p><strong>HR Contact:</strong> {{ details.company.companywebsite }}</p>
        <p><strong>Website :</strong> {{ details.company.hrcontact }}</p>

        <hr>

        <h6>Drive Info</h6>
        <p><strong>drive_id:</strong> {{ details.drive.id }}</p>
        <p><strong>Job Title:</strong> {{ details.drive.job_title }}</p>
        <p><strong>Description:</strong> {{ details.drive.job_description }}</p>
        <p><strong>Eligibility:</strong> {{ details.drive.eligibiltiy }}</p>
        <p><strong>Deadline:</strong> {{ details.drive.application_deadline }}</p>

      </div>
    </div>
    <!-- {{ details }} -->
  </div>


  <!-- {{ interviewlist }} -->

  <h2 class="text-center"> upcoming inteview</h2>
  <div class="container mt-4">

  <div v-if="interviewlist.filter(i => i.status !== 'completed').length === 0">
    <h4>No Interview</h4>
  </div>

  <div class="row g-2" v-else>

    <div
      class="col-md-4"
      v-for="inte in interviewlist"
      :key="inte.id" 
       >

       

         
         <div class="card h-100 shadow-sm" v-if="inte.status!=='completed'">
           <div class="card-body">
             
             <h5>Application ID: {{ inte.id }}</h5>
             <p>Date: {{ inte.d }}</p>
             
            </div>
          </div>
        

    </div>

  </div>

</div>
  



</template>

<style scoped></style>