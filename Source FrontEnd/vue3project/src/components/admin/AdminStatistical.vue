<template>
    <div id="administrator">
        <div>
            <router-link :to="{ name: 'AdminComp' }"> Dashboard Admin </router-link><i class="fa-solid fa-angles-right"></i>
            <router-link :to="{ name: 'AdminStatistical' }"> Admin Statistical </router-link>
        </div>
        <br>
        <hr>
        <div class="row">
            <div class="col-6">
                <LineChart></LineChart>
            </div>
            <div class="col-4">
                <DoughnutChart></DoughnutChart>
            </div>
        </div>
        <div class="row">
            <div class="col-6">
                <BarChart></BarChart>
            </div>
        </div>
        <Notification></Notification>
    </div>
</template>

<script>

// import BaseRequest from '../../restful/admin/core/BaseRequest';
// import useEventBus from '../../composables/useEventBus'
import Notification from './Notification'
// import config from '../../config.js'

import LineChart from './admin_chart/LineChart.vue'
import DoughnutChart from './admin_chart/DoughnutChart.vue'
import BarChart from './admin_chart/BarChart.vue'
// import Paginate from 'vuejs-paginate-next';

// import ParticleVue32 from "./particle/ParticleVue32.vue";

export default {
    name:"AdminStatistical",
    components:{
        Notification,
        // ParticleVue32,
        LineChart,
        DoughnutChart,
        BarChart
        // Paginate
    },
    setup() {
        // document.title = "Meta Shop - Statistical"
    },
    data(){
        return {
            user:{
                id:'',
                fullname:'',
                email:'',
                phone:'',
                password:'',
                create_at:'',
                update_at:'',
            },
        }
    },
    mounted(){
        this.admin = JSON.parse(window.localStorage.getItem('admin'));
    },
    methods:{
    },
    watch:{
    }
}
</script>

<style scoped>

</style>
