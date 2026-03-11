<script>
import axios from 'axios';
export default {
    data() {
        return {
            company: []
            , student: [],
            total_drive: '',
            total_students: '',
            total_company: '',
            total_application:'',
            msg: '',
            search: ""

        }


    }, methods: {

        async searchCompany() {
            if (this.search === "") {
                this.getcompany()
                this.getstudent()
                return
            }

            const res = await axios.get("/api/company", {
                params: {
                    q: this.search
                },
                headers: {
                    Authorization: "Bearer " + localStorage.getItem("token")
                }
            })

            this.company = res.data.companieslist

            const resu = await axios.get('/api/student', {params: {
                    q: this.search
                }, headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
            this.student = resu.data

        },
        async getcompany() {



            try {

                const token = localStorage.getItem("token")
                // console.log(token)
                const res = await axios.get('/api/company', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                })
                this.company = res.data.companieslist;
                this.total_drive = res.data.total_drive;
                this.total_company = res.data.total_company;
                this.total_students = res.data.total_student;
                this.total_application=res.data.total_application;
                this.msg = res.data.msg
            }
            catch (error) {

                console.log(error.response.data.msg)


            }


        },


        async getstudent() {
            const res = await axios.get('/api/student', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
            this.student = res.data
        },

        async sblacklist(id) {
            const res = await axios.put(`/api/sblacklist/${id}`, {}, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            })
            alert(res.data.msg)
            this.getstudent()
        },
        async usblacklist(id) {
            const res = await axios.put(`/api/usblacklist/${id}`, {}, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            })
            // alert(res.data.msg)
            this.getstudent()
        },

        async cblacklist(id) {
            const res = await axios.put(`/api/cblacklist/${id}`, {}, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('token')}`
                }
            })
            alert(res.data.msg)
            this.getcompany()


        },
        async ucblacklist(id) {
            // console.log(localStorage.getItem("token"))
            const res = await axios.put(`/api/ucblacklist/${id}`, {}, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
            // alert(res.data.msg)

            this.getcompany()


        }

    }
    , mounted() {
        this.getcompany()
        this.getstudent()
    }
}

</script>


<template>
    {{ msg }}
    <input type="text" v-model="search" @input="searchCompany" placeholder="Search " />
 
    <div class="container  text-center" style=background-color:aqua ; >
        <div class="row p-3">
            <div class="col-3">
                <div class="card m-3" style="width:250px;">
                    <div class="card-body">
                        <div class="card-title">
                            <h3> Total compnay</h3>
                        </div>
                        {{ total_company }}
                    </div>
                </div>
            </div>
            <div class="col-3">
                <div class="card  m-3" style="width:250px;">
                    <div class="card-body">
                        <div class="card-title">
                            <h3> Total drive</h3>
                        </div>
                        {{ total_drive }}
                    </div>
                </div>
            </div>
            <div class="col-3">

                <div class="card m-3" style="width:250px;">
                    <div class="card-body">
                        <div class="card-title">
                            <h3> Total student</h3>
                        </div>
                        {{ total_students }}
                    </div>
                </div>
            </div>
            <div class="col-3">

                <div class="card m-3" style="width:250px;">
                    <div class="card-body">
                        <div class="card-title">
                            <h3> Total application</h3>
                        </div>
                        {{ total_application}}
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- {{ student }} -->
    <!-- <h2>{{ company }}</h2> -->
    <label for="table">
        <h3>register compnay</h3>
    </label>
    <table name="table" class="table table-bordered">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>wegs8te</th>
                <th>hr phone</th>
                <th>status</th>
            </tr>
        </thead>
        <tbody>


            <tr v-for="company in company" :key="company.id">
                <td>{{ company.id }}</td>
                <td>{{ company.name }}</td>
                <td>{{ company.website }}</td>
                <td>{{ company.hr_contact }}</td>
                <td>{{ company.approval_status }}</td>
                <td v-if="company.approval_status === false">
                    blacklisted
                    <span><button class="btn btn-primary" @click="ucblacklist(company.id)"> unblacklist </button>
                    </span>
                </td>
                <td v-else>
                    <button class="btn btn-primary" @click="cblacklist(company.id)"> blacklist </button>
                </td>

            </tr>
        </tbody>
    </table>

    <label for="t2">
        <h3>register student</h3>
    </label>
    <table name="t2" class="table table-bordered">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>email</th>
            </tr>
        </thead>
        <tbody>


            <tr v-for="s in student" :key="s.id">
                <td>{{ s.id }}</td>
                <td>{{ s.name }}</td>
                <td>{{ s.email }}</td>
                <td v-if="s.is_active">

                    <button class="btn btn-primary" @click="sblacklist(s.id)">blacklist</button>
                </td>

                <td v-else>
                    unblacklist
                    <span>

                        <button class="btn btn-primary" @click="usblacklist(s.id)">unblacklist</button>
                    </span>
                </td>


            </tr>
        </tbody>
    </table>

</template>
<style scoped>
.custombtn {
    border-radius: 30px;
    width: auto;
}

.custombtn:hover {
    background-color: #14d3b7;

}
</style>