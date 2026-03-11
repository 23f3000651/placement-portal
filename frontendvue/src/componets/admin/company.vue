<script>
import axios from 'axios';
export default {
    data() {
        return {
            company: [],
            palcementdirve:[]
        }


    }, methods: {
        async getcompany() {
            const res = await axios.get('/api/company',{headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}})
            this.company = res.data.companieslist;
            this.palcementdirve=res.data.drivelist;



        },
        async activateCompany(id) {
            const res = await axios.put(`/api/activate/${id}`,{},{headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}})
            alert(res.data.msg)
            this.getcompany()
        },
        async activatedrivr(id){
            const res=await axios.put(`/api/changedrivestatus/${id}`,{},{headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}})
            this.getcompany()
            
        }

    }
    , mounted() {
        this.getcompany()
        // this.getplacmentdrive()
    }
}

</script>


<template>
    

    <!-- <h2>{{ company }}</h2> -->
     <h2>compnay</h2>

    <table class="table table-bordered">
        <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>wegs8te</th>
            <th>hr phone</th>
            <th>status</th>
            <th>Action</th>
        </tr></thead>
        
        <tbody>
        

        <tr v-for="company in company" :key="company.id">
            <td>{{ company.id }}</td>
            <td>{{ company.name }}</td>
            <td>{{ company.website }}</td>
            <td>{{ company.hr_contact }}</td>
            <td>{{ company.approval_status }}</td>
            <td>
                <button v-if="company.approval_status === false" class="btn btn-primary btn-sm custombtn"
                    @click="activateCompany(company.id)">
                    Activate
                </button>
                <div v-else style="background-color: aquamarine;" >
                    Already Active
                </div>

            </td>
        </tr>
        </tbody>
    </table>

    <h2>pladcment drive</h2>
    <table class="table table-bordered">
        <thead>
            <tr><th>ID</th>
            <th>compnay id</th>
            <th>job title</th>
            <th>description</th>
            <th>eligibility criteria</th>
            <th>deadline</th>
            <th>Action</th>
        </tr></thead>
        <tbody>
        

        <tr v-for="drive in palcementdirve" :key="company.id">
            <td>{{ drive.id }}</td>
            <td>{{ drive. company_id }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.job_description }}</td>
            <td>{{ drive.eligibility_criteria}}</td>
            <td>{{drive.application_deadline}}</td>
            <td>
                <button  v-if="drive.is_active" class="btn btn-primary btn-sm custombtn"
                    @click="activatedrivr(drive.id)">
                    rejtect drive
                </button>
                <div v-else >
                <button  class="btn btn-primary btn-sm custombtn" @click="activatedrivr(drive.id)">
                    approve dirve
                </button>
                </div>

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

.custombtn:hover{
  background-color: #14d3b7;  
  
}
</style>