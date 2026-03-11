<script>
import axios from 'axios';


export default{
    data(){
        return{
            msg:'',
            studentid:'',
            studentname:'',
            user_id:'',
            email:'',
            companyid: null,
            company:[]
            ,aplicationlist:[],
            drive:[]



        }

    },
    mounted(){
        this.user_id=localStorage.getItem('userid')
        this.getstudetails(this.user_id)
        
        
    }
    ,methods:{
        async getstudetails(user_id){
            const res= await axios.get(`/api/studentdata/${user_id}`)
            const data=res.data
            this.company=data.compnaylist
            this.email=data.email
            this.studentname=data.studentname
            this.aplicationlist=data.applicationlist
            this.studentid=data.studentid
            localStorage.setItem('student_id',data.student_id)

            // console.log(res.data)

        },
        async getdive(companyid){
            this.companyid=companyid
            // const res =await
            const res= await axios.get(`/api/getdrive/${companyid}`)
            // console.log(`run hua ${companyid}`)
            const data= res.data
            this.drive=data.data
        },
        cleardrive(){
            this.drive=[]
        },
        async applyfordrive(id){
            const studentdrive={
                studentname:this.studentname,
                driveid: id,
                studentid:this.studentid

            }
            await axios.post("/api/applydrive",studentdrive)
            await this.getdive(this.companyid)
            

            

        }
    
    }

}

</script>






<template>


 <div class="container m-4 w-50  mx-auto">
  <div class="card shadow-sm">
    
    <div class="card-body text-center">
      <h4 class="fw-bold">
            Welcome {{ studentname}} 
      </h4>
      <p class="text-muted">
       find out company and apply for dirve
      </p>
    </div>

  </div>
</div>


  <div class=" row ms-5 ">

      <div class="card mb-5 w-75 ">
          <div class="card-header d-flex justify-content-center  ">
              
              
              
        <h2> approved compnay </h2>
    </div>
    <div class="card-body">

        <table class="table table-bordered ">
            
            <thead class="mt-3">
                <tr>
               <th>company id</th>
               <th>compnay name</th>
               
            <th >compnay email</th>
            <th >drive detials</th>
        </tr>

        </thead>
        <tbody>
                    
            <tr v-for="c in company" :key="c.id">
                <template v-if="c.is_active">
                

                    <td>{{c.id}}
                    </td>
                    <td>{{c.company_name}}
                    </td>
                    <td>{{c.email}}
                    </td>
                    
                    
                    <td><button class="btn btn-primary" @click="getdive(c.id)">  details</button>
                    </td>
                    
                    </template>

            </tr>
        </tbody>
    </table>
</div>
</div>
    <div class="card  mt-5 w-75 p-3" v-if="drive.length > 0">
        <div class="card-header d-flex justify-content-between ">

            <h3 class="mb-0">Drive</h3>

            <button class="btn btn-danger btn-sm" @click="cleardrive()" >close</button>
        </div>
        <div class="card-body">

            <table class="table table-bordered ">
                
                <thead class="mt-3">
                    <tr>
                        <th>drive id</th>
                        <th>company id</th>
                        <th>job title</th>
                        <th>job des</th>
           <th>eligibility_criteria</th></tr>
           
            
        </thead>
        <tbody>
            
            
            <tr v-for="c in drive" :key="c.id">
                
                
                <td>{{c.drive.id}}
                </td>
                <td>{{c.drive.company_id}}
                </td>
                <td>{{c.drive.job_title}}
                </td>
                    <td>{{c.drive.job_description}}
                    </td>
                    <td>{{c.drive.eligibility_criteria}}
                    </td>
                    
                    <td><button class="btn btn-primary" @click="applyfordrive(c.drive.id)" v-if="!c.applications?.some(a => a.student_id === studentid) && c.drive.is_active">apply</button> 
                        <button class="btn btn- btn-success" v-else-if="!c.drive.is_active" > not avelbale</button> 
                        <button class="btn btn- btn-success" v-else > alereday appily</button> </td>
                        
                        
                        
                    </tr>
                </tbody>
            </table>
        </div>
        </div>
    
    <!-- {{ drive }} -->
            </div>
</template>