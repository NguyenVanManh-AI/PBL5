<template>
    <div class="d-flex center" >
        AdminManagementAdmin
        <form @submit.prevent="register()" class="col-6">
            <div class="form-group">
                <label for="exampleInputEmail1">Email address</label>
                <input type="email" required v-model="user.email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
            </div>
            <div class="form-group">
                <label for="exampleInputPassword1">Password</label>
                <input required v-model="user.password" type="password" class="form-control" id="exampleInputPassword1">
            </div>
            <div class="form-group form-check">
                <input type="checkbox" class="form-check-input" id="exampleCheck1">
                <label class="form-check-label" for="exampleCheck1">Check me out</label>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
        </form>
        <h1>Status : {{ this.status }}</h1>
    </div>
</template>

<script>

import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
import { fireStoreCore } from './../../configs/firebase';

export default {

    name: "AdminManagementAdmin",
    components: {
        
    },
    data(){
        return {
            user:{
                email:'',
                password:''
            },
            status:null,
            uid:null,
        }
    },
    methods: {
        register(){
            createUserWithEmailAndPassword(getAuth(),this.user.email,this.user.password)
            .then((data) => {
                this.status = "Thanh cong !";
                console.log(data);
                this.uid = data.user.uid;
                this.setData();
                    // create admin 
                    // let id_admin = fireStoreCore.collection("admins").doc().id;
                    
            })
            .catch((error) => {
                this.status = "That bai";
                console.log(error);
            })
        },
        setData(){
            fireStoreCore.collection("admins").doc(this.uid).set({
                fullname: "",
                phone:"" ,
                email:this.user.email,
                create_at:"",
                update_at:""
            });
        }

    }
}
</script>
<style scoped>

</style>