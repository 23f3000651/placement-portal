import { createRouter, createWebHistory } from 'vue-router'
import Login from './componets/comman/login.vue'

import adminlayout from './layouts/adminlayout.vue'
import AdminDashboard from './componets/admin/Dashboard.vue'
import companyaplication from '@/componets/admin/company.vue'
import studetadmin from '@/componets/admin/studnetapplication.vue'



import studentlayout from './layouts/studentlayout.vue'
import studentdashbord from '@/componets/student/Dashboard.vue'
import studentapplication from '@/componets/student/studentapplicationhisotry.vue'
import updateprofileforstudent from '@/componets/student/updateprofile.vue'



import compnaylayout from './layouts/compnaylayout.vue'
import companydashbord from './componets/company/Dashboard.vue'
import Createcompany from './componets/company/createcompany.vue'
import detailsofdrivestudent from './componets/company/detailsofdrivestudent.vue'
import updaateprofile from './componets/company/updateprofile.vue'
import upcominginterview from './componets/company/upcomingintevies.vue'


const routes = [
{ path: '/', component:  Login},




{path:"/student",component: studentlayout,meta: { role: "student" },
  children:[
    {path: 'dashboard', component:studentdashbord},
    {path: 'studentapplication',component:studentapplication},
    {path: 'updateprofile', component:updateprofileforstudent}
    
  ]
},



{path:"/company",component:compnaylayout,meta: { role: "company" },
  children:[
    {path: 'dashboard', component:companydashbord},
    {path:'createcompnay',component:Createcompany},
    {path:'detailsofstudentdrive/:driveid',component:detailsofdrivestudent,props: true},
    {path: "profile",component:updaateprofile},
    {path:"upcominginterview",component:upcominginterview}
    
  ]
},



{path: "/admin",component:adminlayout, meta: { role: "admin" },

  children:[
    { path: 'dashboard', component: AdminDashboard },
    {path:'companyaplication', component:companyaplication},
    {path:'studetnapplication',component:studetadmin}

    
  ]
}
]
const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token');
    const role = localStorage.getItem('role');

    if (to.path === '/') {
        next();
        return;
    }

    if (!token|| token === "undefined") {
        next('/');
    }
    else if (to.meta.role && to.meta.role !== role) {
        next('/'); // role mismatch
    }
    else {
        next();
    }
});

export default router