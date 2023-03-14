<template>
    <div>
        <button type="button" class="mb-4 btn btn-success rounded" @click="home"><i class="fa-solid fa-house-circle-check"></i></button>
        <button v-if="isAdmin" @click="logout" type="button" class=" float-right ml-3 mb-4 btn btn-danger"><i class="fa-solid fa-arrow-right-from-bracket"></i> Logout</button>
        <div v-if="isAdmin" class="d-flex justify-content-center">
            <div class="d-flex justify-content-center alert alert-success col-6" role="alert" >
                Dashboard Admin
            </div>
        </div>
        <div v-if="isAdmin" class="d-flex justify-content-center">
            <router-link class="mx-4" :to="{ name: 'AdminManagementUser' }"> <i class="fa-solid fa-users"></i> Management User Account </router-link>
            <router-link class="mx-4" :to="{ name: 'AdminManagementAdmin' }"> <i class="fa-solid fa-users-gear"></i> Management Admin Account </router-link>
            <router-link class="mx-4" :to="{ name: 'AdminStatistical' }"> <i class="fa-solid fa-chart-pie"></i> Statistical </router-link>
            <router-link class="mx-4" :to="{ name: 'AdminAccount' }"> <i class="fa-solid fa-user-shield"></i> My Account </router-link>
        </div>
        <router-view></router-view>
    </div>
</template>
<script>

export default {
    name: "AdminComp",
    components: {
    },
    computed: {
        isAdmin() {
            return this.$route.path === "/admin";
        },
    },
    data(){
        return {
            admin:null,
        } 
    },
    methods: {
        home(){
            if(!window.localStorage.getItem('admin')) this.$router.push({name:"AdminLogin"});
            else this.$router.push({name:'AdminComp'});
        },
        logout(){
            window.localStorage.removeItem('admin');
            this.$router.push({name:'AdminLogin'}); 
        }
    },
    mounted(){

    }
}
</script>

<style>

</style>