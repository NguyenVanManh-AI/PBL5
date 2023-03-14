<template>
  <div >
    <div>
      <canvas id="myChart2"></canvas>
    </div>
  </div>
</template>

<script >
  // import {Chart} from 'chart.js'
import Chart from 'chart.js/auto';
import useEventBus from '../../../composables/useEventBus'
// import BaseRequest from '../../../restful/admin/core/BaseRequest';

export default {
    name: 'DoughnutChart' ,
    data(){
        return {
            data_donut : [120,456,234,100],
            labels_donut : ['Late','On leave','Unauthorized absences','Arrive on time','Stainless'],
        }
    },
    mounted(){
        const ctx = document.getElementById('myChart2');
        var data = {
            labels: this.labels_donut,
            datasets: [{
                label: 'Order number',
                data: this.data_donut,
                backgroundColor: [
                    'rgb(255, 205, 86)',
                    'rgb(54, 162, 235)',
                    '#7ED957',
                    '#008037',
                    'rgb(255, 99, 132)',
                ],
                hoverOffset: 4
            }]
        };
        var mc = new Chart(ctx, {
            type: 'doughnut',
            data: data,
            options: {
                plugins: {
                    // title: {
                    //     display: true,
                    //     text: 'Custom Chart Title',
                    //     padding: {
                    //         top: 10,
                    //         bottom: 30
                    //     }
                    // }
                }
            }
        });

        const { onEvent } = useEventBus()
        onEvent('event2AdminStatistical',ob=>{
            mc.destroy(); 
            data = {
                labels: ob.labels_donut,
                datasets: [{
                    label: 'Order number',
                    data:ob.data_donut,
                    backgroundColor: [
                    'rgb(255, 205, 86)',
                    'rgb(54, 162, 235)',
                    '#7ED957',
                    '#008037',
                    'rgb(255, 99, 132)',
                    ],
                    hoverOffset: 4
                }]
                };
            mc = new Chart(ctx, {
                type: 'doughnut',
                data: data,
                options: {
                    plugins: {
                        // title: {
                        //     display: true,
                        //     text: 'Custom Chart Title',
                        //     padding: {
                        //         top: 10,
                        //         bottom: 30
                        //     }
                        // }
                    }
                }
            });
        });
    },
}

</script>
