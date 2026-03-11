<script>
import router from '@/routes';
import axios from 'axios';
// import Detailsofdrivestudent from './detailsofdrivestudent.vue';

export default {
    data() {
        return {
            msg: '',
            user_id: '',
            email: '',
            website: '',
            hr_contact: '',
            companyid: '',
            compnayname: ''
            , drive: [],
            shortapplciation: [],
            showInterviewForm: false,
            interview: {
                application_id: null,
                student_id: null,
                cid:localStorage.getItem('compnayid'),
                interview_date: "",
                status: "SCHEDULED",
                feedback: ""
            }


        }

    },
    mounted() {
        this.user_id = localStorage.getItem('userid')
        this.getcomanydetails(this.user_id)

    }
    , methods: {
        async getcomanydetails(user_id) {
            const res = await axios.get(`/api/getcompanydata/${user_id}`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
            const data = res.data
            // console.log(data)
            this.compnayname = data.company_name
            this.email = data.email
            this.website = data.website
            this.hr_contact = data.hr_contact
            this.companyid = data.compnayid;
            this.drive = data.drive;
            this.shortapplciation = data.shortlistapplication

            localStorage.setItem('compnayid', data.compnayid)

            // console.log(res.data)

        },
        async completdrive(id) {
            const res = await axios.get(`/api/completedrive/${id}`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
            this.getcomanydetails(this.user_id);
        }
        ,
        Detailsofdrivestudent(id) {
            router.push(`/company/detailsofstudentdrive/${id}`)
        },
        openInterview(appId, studentId) {

            this.showInterviewForm = true

            this.interview.application_id = appId
            this.interview.student_id = studentId

        },

        closeForm() {
            this.showInterviewForm = false
        },
        async scheduleInterview() {

            await axios.post("/api/interview", this.interview)
            // console.log(this.interview)

            alert("Interview Scheduled")

            this.showInterviewForm = false

        }


    }

}

</script>











<template>
    <div class="container mt-4">
  <div class="card shadow-sm">
    
    <div class="card-body text-center">
      <h4 class="fw-bold">
        Welcome {{  compnayname}} 
      </h4>
      <p class="text-muted">
        Manage your placement drives and view student applications here.
      </p>
    </div>

  </div>
</div>

    
    <h2>upcoming drive </h2>
    <table class="table table-bordered w-75">

        <thead class="mt-3">



            <tr>
                <th> sr.no</th>
                <th>dirve id</th>
                <th>job title</th>
                <th>job description</th>
                <th>eligibiltiy</th>
                <th>deadline</th>

                <!-- <th>drive name</th> -->

                <th>action</th>
            </tr>
        </thead>
        <tbody>

            <tr v-for="(d, index) in drive" :key="index">
                <td>{{ index + 1 }}
                </td>
                <td>{{ d.id }}
                </td>
                <td>{{ d.job_title }}
                </td>
                <td>{{ d.job_description }}
                </td>
                <td>{{ d.eligibility_criteria }}
                </td>
                <td>{{ d.application_deadline }}
                </td>

                <td><button class="btn btn-primary" @click="Detailsofdrivestudent(d.id)">view application of student
                    </button>
                </td>
                <td v-if="d.is_active"><button class="btn btn-primary" @click="completdrive(d.id)">complet</button>
                </td>
                <td v-else><button class="btn btn-danger"> completed or rejected</button></td>
            </tr>
        </tbody>
    </table>

    <h2> shortlist application</h2>
    <table class="table table-bordered w-75">

        <thead class="mt-3">



            <tr>

                <th>sr.no</th>
                <th>student_id</th>
                <th>drive_id</th>
                <th>action</th>
            </tr>
        </thead>
        <tbody>

            <tr v-for="(d, index) in shortapplciation" :key="index">
                <template v-if="d.status === 'Shortlisted'">
                    <td>{{ index + 1 }}
                    </td>
                    <td>{{ d.student_id }}</td>
                    <td>{{ d.drive_id }}</td>
                    <!-- <td>{{ d.status }}</td> -->
                    <td><button class="btn btn-primary btn-sm" @click="openInterview(d.id, d.student_id)">
                            Schedule Interview
                        </button> </td>
                </template>






            </tr>
        </tbody>
    </table>
    <div v-if="showInterviewForm" class="card p-3 mt-4 w-50">

        <h5>Schedule Interview</h5>

        <div class="mb-2">
            <label>Interview Date</label>
            <input type="date" class="form-control" v-model="interview.interview_date">
        </div>

        <div class="mb-2">
            <label>Status</label>
            <select class="form-control" v-model="interview.status">
                <option value="SCHEDULED">Scheduled</option>
                <!-- <option value="Completed">Completed</option> -->
            </select>
        </div>

        <div class="mb-2">
            <label>Feedback</label>
            <textarea class="form-control" v-model="interview.feedback"></textarea>
        </div>

        <div class="mt-2">

            <button class="btn btn-success me-2" @click="scheduleInterview">
                Save Interview
            </button>

            <button class="btn btn-danger" @click="closeForm">
                Close
            </button>

        </div>

    </div>




</template>