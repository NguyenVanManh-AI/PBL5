<template>
    <div>
        <HeaderUser></HeaderUser>
        User Comp
        <button></button>
        <router-view></router-view>
        <FooterUser></FooterUser>
    </div>
</template>
<script>

import HeaderUser from './user/HeaderUser';
import FooterUser from './user/FooterUser';

export default {
    name: "UserComp",
    components: {
        HeaderUser,
        FooterUser
    },
    methods: {
        
    },
    mounted(){

    }
}
</script>
<style scoped>

</style>