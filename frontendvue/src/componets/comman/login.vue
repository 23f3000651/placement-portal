<script>

export default {
    data() {
        return {
            value: "login"
            , email: '',
            password: '',
            name: '',
            phone: '',
            address: '',
            msg: '',
            role: ''
        }
    },
    mounted() {
        localStorage.removeItem('token');
        localStorage.removeItem('role');
    },
    methods: {
        login() {
            this.value = "login"
        },
        register() {
            this.value = "register"
            this.role = ''


        },
        roleselct(role) {
            this.role = role
        },
        formsubmit(v) {
            // console.log(v);
            if (v === 'login') {
                const data = {
                    email: this.email,
                    password: this.password
                    // role:this.role
                }
                fetch('api/login', {
                    method: 'POST'
                    , headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                }).then(res => res.json())
                    .then(data => {

                        localStorage.setItem('token', data.token);
                        localStorage.setItem('userid',data.userid);
                        // console.log(localStorage.getItem('token'))

                        if (data.suscess && data.role == 'admin') {
                            localStorage.setItem('role', data.role);
                            this.$router.push('/admin/dashboard')
                        }
                        else if (data.suscess && data.role == 'student') {
                            // console.log('ho gaya ya tak')
                            localStorage.setItem('role', data.role);
                            this.$router.push('/student/dashboard')
                        }
                        else if (data.suscess && data.role == 'company') {
                            localStorage.setItem('role', data.role);
                            this.$router.push('/company/dashboard')
                        }
                        else {
                            this.msg = data.msg
                        }



                    })


            }
            else {
                const data = {
                    email: this.email,
                    password: this.password,
                    name: this.name,
                    role: this.role ? this.role.toUpperCase() : "",
                    contact: this.phone,
                    website: this.address




                }
                // console.log('yeh per pouch gaye')
                if (!this.role) {
                    alert(' selct role first')
                    this.msg = 'selcet ther role first '

                    return
                }
                // console.log(data.role)
                fetch('api/register', {
                    method: 'POST'
                    , headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                })
                    .then(res => res.json())
                    .then(data => {
                        this.msg = data.msg

                    })
                console.log("register ka liya apply hua")
            }
        }
    }
}

</script>



<template>
    <h1>aou sa login or register page mate</h1>
    <!-- <div class="app"> -->
    {{ role }}
    <div class="start">

        <div class="inside">
            <div class="center"><button type="button" class="btn btn-primary" @click=login>login</button>
                <button type="button" class="btn btn-primary ms-3" @click=register>register</button>
            </div>

            <div v-if="value === 'register'" class="center">
                <button type="button" class="btn btn-primary mt-1" @click="roleselct('company')">company
                    register</button>
                <button type="button" class="btn btn-primary mt-1 ms-2" @click="roleselct('student')">student
                    register</button>
            </div>
            <div>

                <div class="center mt-3" style="color:red; background-color: black;">{{ msg }}</div>

                <form class="mt-5">
                    <div v-if="role === 'company' && value === 'register'" class="mb-3">
                        <label for="name" class="form-label">company name</label>
                        <input type="email" v-model="name" class="form-control" name="name"
                            aria-describedby="emailHelp">
                    </div>

                    <div v-if="value === 'register' && role === 'student'" class="mb-3">
                        <label for="name" class="form-label"> student name</label>
                        <input type="email" v-model="name" class="form-control" name="name"
                            aria-describedby="emailHelp">
                    </div>

                    <div v-if="value === 'register' && role === 'company'" class="mb-3">
                        <label for="name" class="form-label">hr contact</label>
                        <input type="number" class="form-control" v-model="phone" name="name"
                            aria-describedby="emailHelp">
                    </div>


                    <div v-if="value === 'register' && role === 'company'" class="mb-3">
                        <label for="name" class="form-label">website url</label>
                        <input type="email" class="form-control" v-model="address" name="name"
                            aria-describedby="emailHelp">
                    </div>
                    <!-- ya to fix hai ise change nhi karna hai emial or passsword comman hai -->
                    <div class="mb-3">
                        <label for="exampleInputEmail1" class="form-label">Email address</label>
                        <input type="email" class="form-control" v-model="email" id="exampleInputEmail1"
                            aria-describedby="emailHelp">
                        <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
                    </div>

                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="password" id="exampleInputPassword1">
                    </div>


                </form>
                <div class="center"><button class="btn btn-primary " @click="formsubmit(value)">{{ value }}</button>
                </div>
            </div>
        </div>
    </div>
    <!-- </div> -->

</template>



<style scoped>
* {
    font-style: italic;
}

h1 {
    display: flex;
    justify-content: center;
    justify-items: center;
    margin-top: 4%;
    /* font-style: italic; */
    color: black;
    background-color: aliceblue;
}

.start {

    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    background-color: aquamarine;
    /* display: flex;

    justify-content: center;
    justify-items: center;
    background-color: aqua;

    margin-top: 4%;
    padding: 1%;
    background-color: aqua; */
}

.center {
    display: flex;
    justify-content: center;
    justify-items: center;
}

.inside {
    width: 350px;
    padding: 25px;
    border-radius: 12px;
    background: #f8f9fa;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    background-color: aqua;
    /* display: flex;
    justify-content: center;
    justify-items: center; */

}
</style>