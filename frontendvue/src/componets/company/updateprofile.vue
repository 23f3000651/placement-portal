<script>
import axios from 'axios';

export default{
data() {
  return {
    company: {
      name: "",
      website: "",
      phone: ""
    },
    user_id:'',
    showForm: false
  };
},
mounted(){
    this.user_id=localStorage.getItem('userid')
    this.openUpdateForm(this.user_id)
    
},
methods: {
  async openUpdateForm(user_id) {
    try {
      const res = await axios.get(`/api/profile/${user_id}`);
      this.company = res.data;   
      this.showForm = true;
    } catch (err) {
      console.error(err);
    }
  },

  async updateProfile() {
    try {
      await axios.put(`/api/profile/${this.user_id}`, this.company);
      alert("Updated!");
      this.showForm = false;
    // this.openUpdateForm(this.user_id);
    } catch (err) {
      console.error(err);
    }
  }
}}
</script>

<template>
<div v-if="showForm" class="card p-2 mt-4">
  <form @submit.prevent="updateProfile()">
    
    <div class="mb-3">
      <label class="form-label">Company Name</label>
      <input 
        v-model="company.name" 
        type="text" 
        class="form-control"
        placeholder="Enter company name"
      />
    </div>

    <div class="mb-3">
      <label class="form-label">Website</label>
      <input 
        v-model="company.website" 
        type="text" 
        class="form-control"
        placeholder="Enter website"
      />
    </div>

    <div class="mb-3">
      <label class="form-label">hr contact</label>
      <input 
        v-model="company.phone" 
        type="text" 
        class="form-control"
        placeholder="Enter phone"
      />
    </div>

    <button type="submit" class="btn btn-primary">
      Save
    </button>

  </form>
</div>
</template>