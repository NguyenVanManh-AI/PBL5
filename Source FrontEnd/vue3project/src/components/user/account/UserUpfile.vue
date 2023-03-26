<template>
    <div >
        <div>
            <router-link :to="{ name: 'UserAccount' }"> My Account </router-link><i class="fa-solid fa-angles-right"></i>
            <router-link :to="{ name: 'UserUpfile' }"> Upfile </router-link>
        </div>
        <br>
        <hr>
        <br>
        <div class="col-3">
            <FilePicker></FilePicker>
        </div>
        <div class="mt-6">
            <op  v-for="(image,index) in images" :key="index">
                <!-- <span>
                    {{ API_URL + image.image_path }}
                </span> -->
                <img style="width: 100px;display: inline-block;" :src="API_URL + image.image_path">
            </op>
        </div>
        <br>
        <hr>
        <br>
        <button @click="logout" type="button" class="btn btn-danger"><i class="fa-solid fa-arrow-right-from-bracket"></i> Logout</button>
        <Notification></Notification>
    </div>
</template>

<script>
import FilePicker from './FilePicker.vue';
import config from '../../../config.js'; /// +++
import BaseRequest from '../../../restful/user/core/BaseRequest'; /// +++
import useEventBus from '../../../composables/useEventBus' /// +++
import Notification from './../Notification'

export default {
    name: "UserUpfile",
    components: {
        FilePicker,
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
            },
            images:null,
            API_URL:config.API_URL
        }
    },
    mounted(){

        this.user = JSON.parse(window.localStorage.getItem('user')); /// +++

        BaseRequest.get('api/images?id_user='+this.user.id,{
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          console.log(response);
          this.images = response.data;
          const { emitEvent } = useEventBus();
          emitEvent('eventSuccess','Get all images successfully !');
        })
        .catch(error => {
          console.log(error);
          const { emitEvent } = useEventBus();
          emitEvent('eventError','Get all images fail !');
        });
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