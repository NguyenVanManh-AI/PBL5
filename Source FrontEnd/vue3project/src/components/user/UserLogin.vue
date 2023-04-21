<template>
    <div class="blue col-4 mx-auto userlogin">
        <form @submit.prevent="login()" class="col-12">
            <div class="row">
                <h1 class="col-12 text-center"><i class="fa-solid fa-seedling"></i> User Login</h1>
            </div>
            <br>
            <br>
            <div class="form-group row">
                <label for="exampleInputEmail1"><i class="fa-solid fa-envelope"></i> Email</label>
                <input type="email" required v-model="user.email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
            </div>
            <div class="form-group row">
                <label for="exampleInputPassword1"><i class="fa-solid fa-key"></i> Password</label>
                <input required v-model="user.password" type="password" class="form-control" id="exampleInputPassword1">
            </div>
            <div class="form-group form-check row">
                <input type="checkbox" class="form-check-input" id="exampleCheck1">
                <label class="form-check-label" for="exampleCheck1">Check me out</label>
            </div>
            <div class="row">
                <button type="submit" class="btn btn-outline-primary col-4 mx-auto"><i class="fa-solid fa-paper-plane"></i> Login</button>
            </div>
            <!-- <button class="btn btn-primary" @click="signInWithGoogle">Login with Google</button> -->
        </form>
        <Notification></Notification>
    </div>
</template>
  
<script>
// import { getAuth, signInWithEmailAndPassword } from "firebase/auth";
import bcrypt from 'bcryptjs';
import { fireStoreCore } from './../../configs/firebase';
import useEventBus from '../../composables/useEventBus'
import Notification from './Notification'
import LoginRequest from '../../restful/user/requests/LoginRequest'

export default {
    name: "UserLogin",
    components:{
        Notification,
    },
    data() {
        return {
            user:{
                email:'',
                password:''
            },
            status:null,
        };
    },
    mounted(){
        if(window.localStorage.getItem('user')){
            this.$router.push({name:"UserProfile"});
        }
    },
    methods: {
        login:function(){
            var v = this.user;
            LoginRequest.post('login/',this.user)
            .then( data => {
            this.setdata(data);
            const { emitEvent } = useEventBus();
            emitEvent('eventSuccess','Login Success !');
            setTimeout(()=>{
                this.$router.push({name:'UserProfile'}); 
            }, 1000);
            })
            .catch( () => {
            this.user = v; 
            const { emitEvent } = useEventBus();
            emitEvent('eventError','Login fail !');
            })
        },
        setdata:function(data){
            var user = {
                id:null,
                email:null,
                role:null,
                password:null,
                fullname:null,
                url_video:null,
                phone:null,
                create_at:null,
                update_at:null,
            }
            user = data;
            window.localStorage.setItem('user',JSON.stringify(user));
        },
    },
};
</script>
  

<style scoped>
.userlogin {
    border: 2px solid silver;
    border-radius: 10px;
    padding: 30px;
}
</style>