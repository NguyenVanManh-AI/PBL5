<template>
    <div>
        <button type="button" class="mb-4 btn btn-secondary rounded" @click="home"><i class="fa-solid fa-house-user"></i></button>
        <!-- <HeaderUser></HeaderUser> -->
        <div v-if="isUser" class="d-flex justify-content-center">
            <div class="d-flex justify-content-center alert alert-primary col-6" role="alert" >
                Dashboard User
            </div>
        </div>
        <div v-if="isUser" class="d-flex justify-content-center">
            <router-link class="mx-4" :to="{ name: 'UserAccount' }"> <i class="fa-solid fa-circle-user"></i> My Account </router-link>
            <router-link class="mx-4" :to="{ name: 'UserAttentdance' }"> <i class="fa-solid fa-calendar-check"></i> User Attentdance </router-link>
        </div>
        <router-view></router-view>
        <!-- <FooterUser></FooterUser> -->
    </div>
</template>
<script>

// import HeaderUser from './user/HeaderUser';
// import FooterUser from './user/FooterUser';

export default {
    name: "UserComp",
    components: {
        // HeaderUser,
        // FooterUser
    },
    computed: {
        isUser() {
            if(this.$route.path == '/main' || this.$route.path == '/main/')
            return true;
        },
    },
    data(){
        return {
            User:null,
        } 
    },
    methods: {
        home(){
            this.$router.push({name:'UserComp'});
        }
    },
    mounted(){
        if(!window.localStorage.getItem('user')){
            this.$router.push({name:"UserLogin"});
        }
    }
}
</script>

<style>

</style>