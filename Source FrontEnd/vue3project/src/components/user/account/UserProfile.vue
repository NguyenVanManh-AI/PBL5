<template>
    <div >
        <div>
            <router-link :to="{ name: 'UserAccount' }"> My Account </router-link><i class="fa-solid fa-angles-right"></i>
            <router-link :to="{ name: 'UserProfile' }"> User Profile </router-link>
        </div>
        <br>
        <hr>
        <form class="col-6 mt-6 mb-6" @submit.prevent="save()">
            <div class="form-group row">
                <label for="staticEmail" class="col-sm-2 col-form-label"><i class="fa-solid fa-at"></i> Full Name</label>
                <div class="col-sm-10">
                    <input type="text" v-model="user.fullname" required class="form-control-plaintext" placeholder="Full Name">
                </div>
            </div>
            <div class="form-group row">
                <label for="staticEmail" class="col-sm-2 col-form-label"><i class="fa-solid fa-envelope"></i> Email</label>
                <div class="col-sm-10">
                    <input type="email" v-model="user.email" required class="form-control-plaintext" placeholder="email@example.com">
                </div>
            </div>
            <div class="form-group row">
                <label for="inputPassword" class="col-sm-2 col-form-label"><i class="fa-solid fa-phone"></i> Phone</label>
                <div class="col-sm-10">
                    <input type="tel" v-model="user.phone" required class="form-control-plaintext" placeholder="Phone">
                </div>
            </div>
            <div class="form-group row">
                <label for="inputPassword" class="col-sm-2 col-form-label"><i class="fa-solid fa-calendar-plus"></i> Create At</label>
                <div class="col-sm-10">
                    <input :value="convertTimestampToDatetime(user.create_at)" type="text" disabled required class="form-control" >
                </div>
            </div>
            <div class="form-group row">
                <label for="inputPassword" class="col-sm-2 col-form-label"><i class="fa-solid fa-calendar-check"></i> Update At</label>
                <div class="col-sm-10">
                    <input :value="convertTimestampToDatetime(user.update_at)" type="text" disabled required class="form-control" >
                </div>
            </div>
            <button type="submit" class="btn btn-outline-success"><i class="fa-solid fa-floppy-disk"></i> Save</button>
        </form>
        <hr>
        <br>
        <button @click="logout" type="button" class="btn btn-danger"><i class="fa-solid fa-arrow-right-from-bracket"></i> Logout</button>
        <Notification></Notification>
    </div>
</template>

<script>
import { fireStoreCore } from './../../../configs/firebase';
import firebase from 'firebase/compat/app';
import useEventBus from '../../../composables/useEventBus'
import Notification from './../Notification'

export default {
    name: "UserProfile",
    components: {
        Notification
    },
    data(){
        return{
            user:{
                id:'',
                fullname:'',
                email:'',
                phone:'',
                img_url:'',
                vector:'',
                password:'',
                create_at:'',
                update_at:'',
            }
        }
    },
    mounted(){
        this.user = JSON.parse(window.localStorage.getItem('user'));
    },
    methods: {
        convertTimestampToDatetime(timestamp) {
            const date = new Date(timestamp.seconds * 1000 + timestamp.nanoseconds / 1000000);
            return date.toLocaleString();
        },
        save() {

            var sys_user = JSON.parse(window.localStorage.getItem('user'));
            let UpdateAt = firebase.firestore.FieldValue.serverTimestamp();
            let email = this.user.email;
            // Kiểm tra email đã được sử dụng chưa
            fireStoreCore.collection('users').where('email', '==', email).get()
                .then((querySnapshot) => {
                    if (querySnapshot.empty || (querySnapshot.size==1 && email == sys_user.email)) { 
                        // Cập nhật thông tin người dùng
                        fireStoreCore.collection('users').doc(this.user.id)
                            .update({
                                fullname: this.user.fullname,
                                email: email,
                                phone: this.user.phone,
                                update_at: UpdateAt,
                            })
                            .then(() => {
                                this.getNewUser();
                                const { emitEvent } = useEventBus();
                                emitEvent('eventSuccess','User information updated successfully !');
                            })
                            .catch((error) => {
                                const { emitEvent } = useEventBus();
                                emitEvent('eventError','Error while updating user information : '+error);
                            });
                    } else {
                        const { emitEvent } = useEventBus();
                        emitEvent('eventError','Email already in use !');
                    }
                })
                .catch((error) => {
                    const { emitEvent } = useEventBus();
                    emitEvent('eventError','Error when checking email : '+error);
                })
        },
        getNewUser(){
            fireStoreCore.collection('users').doc(this.user.id)
            .get()
            .then(doc => {
                if (doc.exists) {
                    this.user = doc.data();
                    this.user.id = doc.id;
                    window.localStorage.setItem('user', JSON.stringify(this.user));
                } 
            })
            .catch({});
            window.localStorage.setItem('user',JSON.stringify(this.user));
        },
        logout(){
            window.localStorage.removeItem('user');
            this.$router.push({name:'UserLogin'}); 
        }
    }
}
</script>
<style scoped>

</style>