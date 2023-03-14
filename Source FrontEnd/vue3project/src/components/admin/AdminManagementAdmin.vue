<template>
    <div>
        <div class="d-flex justify-content-between">
            <!-- Button trigger modal -->
            <div>
                <router-link to="/admin"> Dashboard Admin </router-link><i class="fa-solid fa-angles-right"></i>
                <router-link :to="{ name: 'AdminManagementAdmin' }"> Management Admin</router-link>
            </div>
            <div>
                <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
                    <i class="fa-solid fa-user-plus"></i>
                </button>
            </div>
        </div>
        <br>
        <div >
            <table class="table table-hover table-bordered">
                <thead class="thead-dark">
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">ID</th>
                        <!-- <th scope="col" class="text-center"><i class="fa-solid fa-envelope"></i> Email</th> -->
                        <th scope="col" ><i class="fa-solid fa-envelope"></i> Email</th>
                        <th scope="col" ><i class="fa-solid fa-at"></i> Full Name</th>
                        <th scope="col" ><i class="fa-solid fa-phone"></i> Phone</th>
                        <th scope="col" ><i class="fa-regular fa-calendar-plus"></i> Create At</th>
                        <th scope="col" ><i class="fa-solid fa-calendar-plus"></i> Update At</th>
                        <!-- <th></th> -->
                        <th></th>
                    </tr>
                </thead>
                <tbody v-for="(admin,index) in admins" :key="index">
                    <tr>
                        <th scope="row">{{ (pageN-1)*5+index+1 }}</th>
                        <td>{{ admin.id.length > 20 ? admin.id.slice(0, 20) + '...' : admin.id }}</td>
                        <td>{{ admin.email.length > 30 ? admin.email.slice(0, 30) + '...' : admin.email }}</td>
                        <td>{{ admin.fullname }}</td>
                        <td>{{ admin.phone }}</td>
                        <td>{{ formatDate(admin.create_at.toDate()) }}</td>
                        <td>{{ formatDate(admin.update_at.toDate()) }}</td>
                        <!-- <td>{{ admin.update_time != null ? admin.update_time.slice(0, 26) : admin.update_time }}</td> -->
                        <!-- <td style=""><button type="button" class="btn btn-outline-primary" @click="editRole(ad.id,ad.role)">Save</button></td> -->
                        <td style=""><button type="button" class="btn btn-outline-danger" @click="openModel(admin.id)" data-toggle="modal" data-target="#exampleModalDelete">Delete</button></td>
                    </tr>
                </tbody>
            </table>

            <div id="divpaginate">
                <paginate class="pag" id="nvm"
                    :page-count="Math.ceil(this.quantity/5)"
                    :page-range="3"
                    :margin-pages="2"
                    :click-handler="clickCallback"
                    :initial-page="this.pageN"
                    :prev-text="'Prev'"
                    :next-text="'Next'"
                    :container-class="'pagination'"
                    :page-class="'page-item'">
                </paginate>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Add Account</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="register()" class="col-12">
                            <div class="form-group">
                                <label for="exampleInputEmail1">Email address</label>
                                <!-- minlength and maxlength -->
                                <input type="email" minlength="16" required v-model="admin.email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
                                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
                            </div>
                            <div class="form-group">
                                <label for="exampleInputPassword1">Password</label>
                                <input required minlength="6" v-model="admin.password" type="password" class="form-control" id="exampleInputPassword1">
                            </div>
                            <div class="form-group form-check">
                                <input type="checkbox" class="form-check-input" id="exampleCheck1">
                                <label class="form-check-label" for="exampleCheck1">Check me out</label>
                            </div>
                            <div class="modal-footer">
                            <button id="closeAdd" type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                            <button type="submit" class="btn btn-success"><i class="fa-solid fa-floppy-disk"></i> Add</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <!-- Model Delete admin -->
        <div class="modal fade" id="exampleModalDelete" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Warning</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-warning" role="alert">
                            Are you sure you want to delete this account ? <br>
                            This account will be permanently deleted from the system !
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-dismiss="modal" @click="closeDelete" id="btnClose2">Close</button>
                        <button type="button" class="btn btn-outline-danger" @click="deleteadminInCollection"><i class="fa-solid fa-trash"></i> Delete</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Model Delete admin -->
        <!-- {{ number1 }} -->
        <Notification></Notification>

    </div>
</template>

<script>

// import { getAuth, createAdminWithEmailAndPassword } from "firebase/auth";
// import { getAuth } from "firebase/auth";
// import { getAuth,deleteAdmin, createAdminWithEmailAndPassword } from "firebase/auth";
import { fireStoreCore } from './../../configs/firebase';
import firebase from 'firebase/compat/app';
import bcrypt from 'bcryptjs';

import useEventBus from '../../composables/useEventBus'
import Paginate from 'vuejs-paginate-next';
import Notification from './Notification'

export default {

    name: "AdminManagementAdmin",
    components: {
        Notification,
        paginate: Paginate,
    },
    data(){
        return {
            admin:{
                email:'',
                password:''
            },
            uid:null,
            number1:0,
            admins:[],
            quantity:null,
            pageN:1,
            pageSize:5,
            idDelete:null
        }
    },
    mounted(){
        // setInterval(() => {
        //     this.number1++;
        // }, 1000);
        this.getAdmins(1);
    },
    methods: {
        formatDate(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            const seconds = String(date.getSeconds()).padStart(2, '0');
            return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        },
        // register(){ // Không thêm tài khoản vào Authentication nữa 
            // createAdminWithEmailAndPassword(getAuth(),this.Admin.email,this.Admin.password)
            // .then((data) => {
            //     // console.log(data);
            //     this.uid = data.Admin.uid;
            //     this.setData(data);
            //         // create admin 
            //         // let id_admin = fireStoreCore.collection("Admins").doc().id;
            // })
            // .catch((error) => {
            //     const { emitEvent } = useEventBus();
            //     emitEvent('eventError',error.code);
            //     // console.log(error);
            // })
        // },
        register() {
            fireStoreCore.collection("admins").where("email", "==", this.admin.email).get()
            .then(async (querySnapshot) => { // lưu ý để async ở đây để sử dụng await ở dưới
                if (querySnapshot.size > 0) {
                    const { emitEvent } = useEventBus();
                    emitEvent('eventError', 'Email already exists!');
                } else {
                    let id_admin = fireStoreCore.collection("admins").doc().id;
                    let createdAt = firebase.firestore.FieldValue.serverTimestamp();
    
                    const salt = await bcrypt.genSalt(10);
                    const hashedPassword = await bcrypt.hash(this.admin.password, salt); // sử dụng await để đợi quá trình hash password
    
                    fireStoreCore.collection("admins").doc(id_admin).set({
                        fullname: "",
                        phone: "", 
                        email: this.admin.email,
                        password: hashedPassword,
                        create_at: createdAt,
                        update_at: createdAt,
                    }).then(() => {
                        this.getAdmins(this.pageN);
                        var closeAdd = window.document.getElementById('closeAdd');
                        closeAdd.click();
                        const { emitEvent } = useEventBus();
                        emitEvent('eventSuccess','Account successfully created !');
                    }).catch(() => {
                        const { emitEvent } = useEventBus();
                        emitEvent('eventError','Add Fail !');
                    });
                }
            })
            .catch(() => {
                const { emitEvent } = useEventBus();
                emitEvent('eventError', 'An error occurred while checking email existence!');
            });
        },
        getAdmins(n) {
            this.admins = [];
            fireStoreCore.collection("admins").orderBy("create_at", "desc").get()
            .then((querySnapshot) => {
                querySnapshot.forEach((doc) => {
                    this.admins.push(doc.data());
                    let l = this.admins.length;
                    this.admins[l-1].id = doc.id;
                });
                this.quantity = querySnapshot.size;
                if(n*5 > this.quantity) this.admins = this.admins.slice((n-1)*5);
                else this.admins = this.admins.slice((n-1)*5,n*5);
            });
        },
        clickCallback:function(pageNum){
            this.pageN = pageNum;
            this.getAdmins(pageNum);
        },
        openModel:function(id){
            this.idDelete = id;
        },
        deleteadminInCollection(){
            // this.deleteAdminInAuthentication();
            const adminsRef = fireStoreCore.collection('admins')
            const docRef = adminsRef.doc(this.idDelete)
            docRef.delete()
            .then(() => {
                var btnClose2 = window.document.getElementById('btnClose2');
                btnClose2.click();
                const { emitEvent } = useEventBus();
                emitEvent('eventSuccess','Account successfully created !');

                if(this.admins.length == 1) {
                    this.getAdmins(1);
                    this.pageN--;
                }
                else this.getAdmins(this.pageN);
            })
            .catch((error) => {
                const { emitEvent } = useEventBus();
                emitEvent('eventError','An error occurred while deleting the account: ' + error.code);
            })
        },
        // deleteAdminInAuthentication(){ // Với Authentication Chỉ có thể xóa tài khoản hiện tại của bản thân 
        //     // không cho phép xóa tài khoản khác . 
        //     const auth = getAuth(fireStoreCore);
        //     deleteAdmin(auth, '46ql3c7DZyQoK6ebSowWvFpUc2v1')
        //         .then(() => {
        //         console.log("Admin deleted successfully.");
        //         // Do something after Admin is deleted
        //         })
        //         .catch((error) => {
        //         console.error("Error deleting Admin:", error);
        //         });
        // }
    }
}
</script>
<style scoped>

</style>