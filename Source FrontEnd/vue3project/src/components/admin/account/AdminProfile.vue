<template>
    <div >
        <div>
            <router-link :to="{ name: 'AdminAccount' }"> My Account </router-link><i class="fa-solid fa-angles-right"></i>
            <router-link :to="{ name: 'AdminProfile' }"> Admin Profile </router-link>
        </div>
        <br>
        <hr>
        <form class="col-6 mt-6 mb-6" @submit.prevent="save()">
            <div class="form-group row">
                <label for="staticEmail" class="col-sm-2 col-form-label"><i class="fa-solid fa-at"></i> Full Name</label>
                <div class="col-sm-10">
                    <input type="text" v-model="admin.fullname" required class="form-control-plaintext" placeholder="Full Name">
                </div>
            </div>
            <div class="form-group row">
                <label for="staticEmail" class="col-sm-2 col-form-label"><i class="fa-solid fa-envelope"></i> Email</label>
                <div class="col-sm-10">
                    <input type="email" v-model="admin.email" required class="form-control-plaintext" placeholder="email@example.com">
                </div>
            </div>
            <div class="form-group row">
                <label for="inputPassword" class="col-sm-2 col-form-label"><i class="fa-solid fa-phone"></i> Phone</label>
                <div class="col-sm-10">
                    <input type="tel" v-model="admin.phone" required class="form-control-plaintext" placeholder="Phone">
                </div>
            </div>
            <div class="form-group row">
                <label for="inputPassword" class="col-sm-2 col-form-label"><i class="fa-solid fa-calendar-plus"></i> Create At</label>
                <div class="col-sm-10">
                    <input :value="convertTimestampToDatetime(admin.create_at)" type="text" disabled required class="form-control" >
                </div>
            </div>
            <div class="form-group row">
                <label for="inputPassword" class="col-sm-2 col-form-label"><i class="fa-solid fa-calendar-check"></i> Update At</label>
                <div class="col-sm-10">
                    <input :value="convertTimestampToDatetime(admin.update_at)" type="text" disabled required class="form-control" >
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
    name: "AdminProfile",
    components: {
        Notification
    },
    data(){
        return{
            admin:{
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
        this.admin = JSON.parse(window.localStorage.getItem('admin'));
    },
    methods: {
        convertTimestampToDatetime(timestamp) {
            const date = new Date(timestamp.seconds * 1000 + timestamp.nanoseconds / 1000000);
            return date.toLocaleString();
        },
        save() {

            var sys_admin = JSON.parse(window.localStorage.getItem('admin'));
            let UpdateAt = firebase.firestore.FieldValue.serverTimestamp();
            let email = this.admin.email;
            // Kiểm tra email đã được sử dụng chưa
            fireStoreCore.collection('admins').where('email', '==', email).get()
                .then((querySnapshot) => {
                    if (querySnapshot.empty || (querySnapshot.size==1 && email == sys_admin.email)) { 
                        // Cập nhật thông tin người dùng
                        fireStoreCore.collection('admins').doc(this.admin.id)
                            .update({
                                fullname: this.admin.fullname,
                                email: email,
                                phone: this.admin.phone,
                                update_at: UpdateAt,
                            })
                            .then(() => {
                                this.getNewAdmin();
                                const { emitEvent } = useEventBus();
                                emitEvent('eventSuccess','Admin information updated successfully !');
                            })
                            .catch((error) => {
                                const { emitEvent } = useEventBus();
                                emitEvent('eventError','Error while updating Admin information : '+error);
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
        getNewAdmin(){
            fireStoreCore.collection('admins').doc(this.admin.id)
            .get()
            .then(doc => {
                if (doc.exists) {
                    this.admin = doc.data();
                    this.admin.id = doc.id;
                    window.localStorage.setItem('admin', JSON.stringify(this.admin));
                } 
            })
            .catch({});
            window.localStorage.setItem('admin',JSON.stringify(this.admin));
        },
        logout(){
            window.localStorage.removeItem('admin');
            this.$router.push({name:'AdminLogin'}); 
        }
    }
}
</script>
<style scoped>

</style>