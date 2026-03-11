,<script>
import axios from 'axios';


export default{
     data(){
        return{
            applicationlist:[],
           
            show:false,
            data:'',
            student: {
        user_id: '',
        Student_name: "",
        education: "",
        skills: "",
        experience: "",
        resume_link: ""
        ,email:''
        
      }

        }


    },
    mounted(){
        this.getapplicataion()
       

    },
    methods:{


 
        async getapplicataion(){
            const res= await axios.get('/api/getapplication',{headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}})
            
            this.applicationlist=res.data;
        },

        async getstudetndetails(id){
            const res= await axios.get(`/api/getstudentforadmin/${id}`,{headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}})
            this.student=res.data
            
            console.log(res.data)

        }
        ,
        showstudent(){
            this.show=true;
        }
        ,hidestuedent(){
            this.show=false;
        }
    }
}
</script>


<template>
    <!-- {{ student }}{{ interviewlist }} -->
      <hr>



<label for table><h3>application list</h3></label>
<table name='tabel' class="table table-bordered">
    <thead>
        <tr>
        <th>id</th>
        <th>drive id</th>
        <th>student id</th>
        <th>status</th>
        <th>acition</th>
        </tr>
    </thead>
    <tbody>
        
        <tr v-for="app in applicationlist">
            <td>{{app.id}}</td>
            <td>{{app.drive_id}}</td>
            <td>{{app.student_id}}</td>
            <td>{{app.status}}</td>
            <td><button class="btn btn-primary" @click="getstudetndetails(app.student_id) ,showstudent()">view </button></td>
            
        </tr>
    </tbody>
</table>











  <div v-if="show" class="d-flex justify-content-center">
  <div class="card p-2 w-75">
    
    <div class="card-header d-flex justify-content-between align-items-center">
      <h5 class="mb-0">Student Details</h5>
      <button class="btn btn-sm btn-danger" @click="hidestuedent">close</button>
    </div>

    <div class="card-body  text-center ">
      <p><strong>Name:</strong> {{ student.Student_name }}</p>
      <p><strong>Education:</strong> {{ student.education }}</p>
      <p><strong>Skills:</strong> {{ student.skills }}</p>
      <p><strong>Experience:</strong> {{ student.experience }}</p>
      
    </div>

    <div class="card-footer text-center">
      
        <a :href="student.resume_link" ><button class="btn btn-secondary" >View Resume</button></a>
    </div>

  </div>
</div>
















</template>