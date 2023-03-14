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
        login() {
            fireStoreCore.collection("users").where("email", "==", this.user.email).get()
            .then(async (querySnapshot) => {
                if (querySnapshot.size > 0) {
                    for (const doc of querySnapshot.docs) {
                        const user = doc.data();
                        const hashedPassword = user.password; // hashedPassword được lấy ra từ firestore
                        const isMatch = await bcrypt.compare(this.user.password, hashedPassword);
                        if (isMatch) {
                            const { emitEvent } = useEventBus();
                            emitEvent('eventSuccess','Login successful !');
                            var system_user = {
                                id:doc.id,
                                email:this.user.email,
                                fullname:user.fullname,
                                phone:user.phone,
                                img_url:'',
                                vector:user.vector,
                                password:user.password,
                                create_at:user.create_at,
                                update_at:user.update_at,
                            };
                            window.localStorage.removeItem('user');
                            window.localStorage.setItem('user',JSON.stringify(system_user));
                            setTimeout(() => {
                                this.$router.push({name:'UserProfile'}); 
                            }, 1000);
                        } else {
                            const { emitEvent } = useEventBus();
                            emitEvent('eventError','Wrong password !');
                        }
                    }
                } else {
                    const { emitEvent } = useEventBus();
                    emitEvent('eventError', 'Email does not exist !');
                }
            })
            .catch((error) => {
                console.log(error+' Xử lý lỗi');
            });
        }
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