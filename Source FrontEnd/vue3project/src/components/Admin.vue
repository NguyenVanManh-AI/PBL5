<template>
    <div>
        <div v-if="isAdmin" class="d-flex justify-content-center">
            <div class="d-flex justify-content-center alert alert-primary col-6" role="alert" >
                Dashboard Admin
            </div>
        </div>
        <div v-if="isAdmin" class="d-flex justify-content-center">
            <router-link class="mx-4" :to="{ name: 'AdminManagementUser' }"> Management User Account </router-link>
            <router-link class="mx-4" :to="{ name: 'AdminManagementAdmin' }"> Management Admin Account </router-link>
            <router-link class="mx-4" :to="{ name: 'AdminStatistical' }"> Statistical </router-link>
            <router-link class="mx-4" :to="{ name: 'AdminProfile' }"> My Account </router-link>
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
    
    },
    mounted(){

    }
}
</script>

<style>

</style>