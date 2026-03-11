<script>

import axios from "axios"

export default {

  data() {
    return {
      student: {
        student_name: "",
        education: "",
        skills: "",
        experience: "",
        resume_link: ""
      },
      userId: localStorage.getItem("userid")
    }
  },

  methods: {

    async getProfile() {

      const res = await axios.get(`/api/studentprofile/${this.userId}`)

      this.student = res.data
    },

    async updateProfile() {

      await axios.put(`/api/studentprofile/${this.userId}`, this.student)

      alert("Profile Updated")
    }

  },

  mounted() {
    this.getProfile()
  }

}

</script>

<template>

  <div class="container mt-5">

    <div class="card ">

      <div class="card-header bg-primary text-white text-center">
        <h4 class="mb-0">Student Profile</h4>
      </div>

      <div class="card-body">

        <form @submit.prevent="updateProfile">

          <div class="row m-2 p-3 text-end">

            <div class=" mb-3">
              <label class="form-label">Student Name</label>
              <input type="text" class="form-control" v-model="student.student_name" placeholder="Enter your name">
            </div>

            <div class="mb-3">
              <label class="form-label">Education</label>
              <input type="text" class="form-control" v-model="student.education" placeholder="B.Tech / MCA / etc">
            </div>

            
            
            <div class="mb-3">
              
              <label class="form-label">Skills</label>

            <textarea class="form-control" rows="3" v-model="student.skills" placeholder="Python, SQL, Flask, Vue">
</textarea>

</div>


          <div class="mb-3">

            <label class="form-label">Experience</label>

            <textarea class="form-control" rows="3" v-model="student.experience" placeholder="Internships / Projects">
</textarea>

</div>


<div class="mb-3 ">
  
  <label class="form-label ">Resume Link</label>
  
  <input type="text" class="form-control" v-model="student.resume_link" placeholder="Paste resume link">
  
</div>


</div>
<div class="text-center">
  
  <button class="btn btn-success">
              Update Profile
            </button>

          </div>

        </form>

      </div>

    </div>

  </div>

</template>