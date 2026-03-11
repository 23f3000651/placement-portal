<script>
import axios from "axios"

export default {
  name: "CreateDrive",

  data() {
    return {
      driveName: "",
      jobTitle: "",
      jobDescription: "",
      eligibility: "",
      deadline: "",
      companyid: '',
      msg: ''
    }
  },
  mounted() {
    this.companyid = Number(localStorage.getItem('compnayid'))
    // console.log(localStorage.getItem('compnayid'))
  },

  methods: {
    async createDrive() {
      try {
        const drivedata = {
          drive_name: this.driveName,
          job_title: this.jobTitle,
          job_description: this.jobDescription,
          eligibility: this.eligibility,
          deadline: this.deadline,
          companyid: this.companyid
        }

        const res = await axios.post("/api/createdrive", drivedata, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })


        alert("Drive Created Successfully ")


        this.driveName = ""
        this.jobTitle = ""
        this.jobDescription = ""
        this.eligibility = ""
        this.deadline = ""

      } catch (error) {

        
        
        
        
        // console.log(error.response.data.msg)
        this.msg = error.response.data.msg
        alert("Error in creating drive ")
      }
    }
  }
}
</script>

<template>
  {{ msg }}
  <div class="container mt-5">
    <div class="card shadow p-5">
      <h4 class="mb-4">Create a Drive</h4>

      <form @submit.prevent="createDrive">

        <div class="mb-3">
          <label class="form-label">Drive Name</label>
          <input type="text" class="form-control" v-model="driveName" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Job Title</label>
          <input type="text" class="form-control" v-model="jobTitle" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Job Description</label>
          <textarea class="form-control" rows="4" v-model="jobDescription" required></textarea>
        </div>

        <div class="mb-3">
          <label class="form-label">Eligibility Criteria</label>
          <input type="text" class="form-control" v-model="eligibility" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Application Deadline</label>
          <input type="date" class="form-control" v-model="deadline" required />
        </div>

        <div class="text-end">
          <button type="submit" class="btn btn-success px-4">
            Save
          </button>
        </div>

      </form>
    </div>
  </div>
</template>
