<template>
    <div >
        <div>
            <router-link :to="{ name: 'AdminAccount' }"> My Account </router-link><i class="fa-solid fa-angles-right"></i>
            <router-link :to="{ name: 'AdminChangePassword' }"> Change Password </router-link>
        </div>
        <br>
        <hr>
        <form class="col-6 mt-6 mb-6" @submit.prevent="change()">
            <div class="form-group row">
                <label for="staticEmail" class="col-sm-4 col-form-label"><i class="fa-solid fa-key"></i> Current Password</label>
                <div class="col-sm-8">
                    <input type="password" v-model="changepw.current_password" required class="form-control" placeholder="Current Password">
                </div>
            </div>
            <div class="form-group row">
                <label for="staticEmail" class="col-sm-4 col-form-label"><i class="fa-solid fa-key"></i> New Password</label>
                <div class="col-sm-8">
                    <input type="password" v-model="changepw.new_password" required class="form-control" placeholder="New Password">
                </div>
            </div>
            <div class="form-group row">
                <label for="staticEmail" class="col-sm-4 col-form-label"><i class="fa-solid fa-key"></i> Confrim New Password</label>
                <div class="col-sm-8">
                    <input type="password" v-model="changepw.new_password_confirmation" required class="form-control" placeholder="Confrim New Password">
                </div>
            </div>

            <button type="submit" class="btn btn-outline-success"><i class="fa-solid fa-bolt"></i> Change</button>
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
import bcrypt from 'bcryptjs';

export default {
    name: "AdminChangePassword",
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
                password:'',
                create_at:'',
                update_at:'',
            },
            changepw:{
              current_password:'',
              new_password:'',
              new_password_confirmation:'',
            },
        }
    },
    mounted(){
        this.admin = JSON.parse(window.localStorage.getItem('admin'));
    },
    methods: {
        change(){
            // Kiểm tra mật khẩu cũ
            var current_password = this.changepw.current_password;
            var new_password = this.changepw.new_password;
            var new_password_confirmation = this.changepw.new_password_confirmation;
            
            bcrypt.compare(current_password, this.admin.password, (err, res) => {
                if (err || !res) {
                    // Mật khẩu cũ không đúng
                    const { emitEvent } = useEventBus();
                    emitEvent('eventError', 'Old password is incorrect !');
                } else {
                    // Mật khẩu cũ đúng, tiếp tục kiểm tra mật khẩu mới
                    if (new_password.length < 6) {
                        // Mật khẩu mới phải ít nhất 6 kí tự
                        const { emitEvent } = useEventBus();
                        emitEvent('eventError', 'New password must be at least 6 characters !');
                    } else if (new_password !== new_password_confirmation) {
                        // Mật khẩu nhập lại không trùng khớp
                        const { emitEvent } = useEventBus();
                        emitEvent('eventError', 'Re-entered password does not match !');
                    } else {
                        // Hash mật khẩu mới
                        const saltRounds = 10;
                        bcrypt.hash(new_password, saltRounds, (err, hash) => {
                            if (err) {
                                // Lỗi khi hash mật khẩu mới
                                const { emitEvent } = useEventBus();
                                emitEvent('eventError', 'Error when changing password : '+err);
                            } else {
                                // Cập nhật mật khẩu mới vào firebase
                                fireStoreCore
                                .collection('admins')
                                .doc(this.admin.id)
                                .update({
                                    password: hash,
                                    update_at: firebase.firestore.FieldValue.serverTimestamp(),
                                })
                                .then(() => {
                                    const { emitEvent } = useEventBus();
                                    emitEvent('eventSuccess', 'Your password has been updated !');
                                })
                                .catch((error) => {
                                    const { emitEvent } = useEventBus();
                                    emitEvent('eventError', 'Error when changing password : '+error);
                                });
                            }
                        });
                    }
                }
            })
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