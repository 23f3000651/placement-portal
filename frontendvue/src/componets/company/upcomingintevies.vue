<script>
import axios from 'axios';


export default {
    data() {
        return {
            data: {
                cid: null
            },
            student: {
                id: null,
                student_name: null,
                education: null,
                skills: null,
                experience: null,
                resume_link: null,
               



            },
            //  studentdetails: null,
            msg: null,
            interviewlist: [],
            selectedApp: null,
            offer_letter: "",
            new_status: "completed",
            placed:false,
            feedbacke: ""
        }

    },
    methods: {
        async getinterview() {

            const res = await axios.put("/api/interview", this.data)
            const result = res.data;
            this.msg = result.msg;
            this.interviewlist = result.intervielist
            // console.log(result)
        }

        ,
        async showDetails(appid) {
            this.selectedApp = appid

            const res = await axios.get(`/api/interviewupdate/${appid}`)
            const data = res.data
            this.student = data.student
            // console.log(data)

        },
        async updateInterview(appid) {
            const postdata={
                    offer_letter: this.offer_letter,
                    new_status :this.new_status,
                    feedbacke :this.feedbacke,
                    placed:this.placed
            }

            const res = await axios.post(`/api/interviewupdate/${appid}`, postdata)
            const data = res.data
            this.student = data.student
            

        }
    },

    mounted() {

        this.data.cid = localStorage.getItem('compnayid')
        this.getinterview()

    }
}

</script>


<template>
    <h2>this is intveire page </h2>
    <!-- {{ interviewlist }} -->
      <!-- {{ student }} -->

    <div v-for="i in interviewlist" :key="i.appid">

        <div v-if="i.status === 'SCHEDULED'" class="card p-3 m-2">

            <h5>Interview Date: {{ i.d }}</h5>
            <h3>{{ i.appid }}</h3>

            <button class="btn btn-primary" @click="showDetails(i.id)">
                Details
            </button>

            <!-- Hidden div -->
            <div v-if="selectedApp == i.id" class="mt-3 border p-3">

                <div v-if="student" class="card p-2 mb-3">

                    <h5>Student Details</h5>

                    <p><b>Name:</b> {{ student.student_name }}</p>

                    <p><b>Skills:</b> {{ student.skills }}</p>

                    <p><b>Experience:</b> {{ student.experience }}</p>

                    <a :href="student.resume_link" target="_blank">
                        View Resume
                    </a>

                </div>

                <input v-model="offer_letter" placeholder="Offer Letter Link" class="form-control mb-2">
<label>interview status</label> 
                <select v-model="new_status" class="form-control mb-2">
                    <option value="OFFERE">offere</option>
                    <option value="REJECTED">REJECTED</option>
                    <option  value="completed" selected>complete</option> </select>
                   <label>placemnt status</label> 
                <select v-model="placed" class="form-control mb-2">
                    <option :value="true">yes</option>
                    <option :value="false">No</option>
                    

                </select>
                <div class="mb-2">
                    <label>Feedback</label>
                    <textarea class="form-control" v-model="feedbacke"></textarea>
                </div>

                <button class="btn btn-success" @click="updateInterview(i.id)">
                    Update
                </button>

            </div>

        </div>

    </div>
</template>