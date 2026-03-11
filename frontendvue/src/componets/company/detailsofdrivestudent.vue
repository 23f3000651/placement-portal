<script>
import axios from 'axios';
export default {
    data() {
        return {

            applcationlist: [],
            selectedStudent: null,
            updatedStatus: '',
            massage:''

        }

    },
    props: ['driveid'],


    mounted() {
        console.log(this.driveid)
        this.studentwhoapplyfordrive(this.driveid)

    },

    methods: {
        async studentwhoapplyfordrive(driveid) {
            const res = await axios.get(`/api/studentwhoappplyfordrive/${driveid}`,{headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}})
            this.applcationlist = res.data
        },


        openDetails(student) {
            this.selectedStudent = student
            this.updatedStatus = student.status
        },
        closeDetails() {
            this.selectedStudent = null
        },

        async updateStatus() {
            const data= {
                application_id: this.selectedStudent.application_id,
                role: this.updatedStatus
            }
            const res=await axios.post("/api/update-status", data,{headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}})
            this.massage=res.data.message

            // console.log(data)
            alert('api hit for this')

        }
    }}
</script>
<template>
    <!-- {{ applcationlist }}  -->
      {{ massage }}

      
      <div class="card mt-3 p-4 text-center" >
        <div class="card-header ">
            <div class="card-title "> <h2>total application in drive</h2></div>
        </div>
        <div class="card-body ">
            <h3>{{ applcationlist.length }}</h3>
        </div>
           </div>
      

    <!-- this is list of studetn who apply for drive    {{ driveid }} -->

    <br>
    <!-- <div class=" d-flex"> -->
    <div class="card m-2   " v-for="student in applcationlist" :key="student.application_id"  @click="openDetails(student)">
        <div class="card-body">
            <h5>{{ student.student_name }}</h5>
            <p>{{ student.email }}</p>
            <span class="badge bg-success">
                {{ student.status }}
            </span>
        </div>
    </div>
    <!-- </div> -->

<div v-if="selectedStudent" class="container mt-4">
  <div class="card shadow">

    <div class="card-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Student Application Details</h5>
      <button class="btn btn-danger btn-sm" @click="closeDetails">
        Close
      </button>
    </div>

    <div class="card-body">

      <p><strong>Name:</strong> {{ selectedStudent.student_name }}</p>
      <p><strong>Email:</strong> {{ selectedStudent.email }}</p>
      <p><strong>Application ID:</strong> {{ selectedStudent.application_id }}</p>

      <div class="mb-3">
        <label class="form-label">Change Status</label>
        <select class="form-select" v-model="updatedStatus">
          <option value="Applied">Applied</option>
          <option value="Shortlisted">Shortlisted</option>
          <option value="Rejected">Rejected</option>
        </select>
      </div>

      <button class="btn btn-primary" @click="updateStatus">
        Save Changes
      </button>

    </div>
  </div>
</div>
</template>