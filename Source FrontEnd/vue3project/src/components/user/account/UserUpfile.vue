<template>
    <div >
        <div>
            <router-link :to="{ name: 'UserAccount' }"> My Account </router-link><i class="fa-solid fa-angles-right"></i>
            <router-link :to="{ name: 'UserUpfile' }"> Upfile </router-link>
        </div>
        <br>
        <hr>
        <br>
        <div class="col-8">
            <FilePicker></FilePicker>
        </div>
        <br>
        <hr>
        <br>
        <button @click="logout" type="button" class="btn btn-danger"><i class="fa-solid fa-arrow-right-from-bracket"></i> Logout</button>
    </div>
</template>

<script>
import FilePicker from './FilePicker.vue';

export default {
    name: "UserUpfile",
    components: {
        FilePicker
    },
    methods: {
        logout(){
            window.localStorage.removeItem('user');
            this.$router.push({name:'UserLogin'}); 
        }
    }
}
</script>
<style scoped>

</style>