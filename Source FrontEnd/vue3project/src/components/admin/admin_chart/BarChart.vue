<template>
  <div >
    <div>
      <canvas id="barChart"></canvas>
    </div>
  </div>
</template>

<script >
import Chart from 'chart.js/auto';
// import useEventBus from '../../../composables/useEventBus'

export default {
    name: 'BarChart' ,
    data(){
        return {

        }
    },
    mounted(){
        // const { onEvent } = useEventBus()
        // onEvent('eventBarChart',data_chart=>{
            var barChart = document.getElementById('barChart');
            var labels = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            var data = {
                labels: labels,
                datasets: [{
                    label: 'Attentdance',
                    data: [1,2,3,4,5,6,7] ,
                    backgroundColor: [
                        'rgb(29, 215, 48, 0.2)',
                        'rgba(255, 205, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(201, 203, 207, 0.2)'
                    ],
                    borderColor: [
                        'rgb(29, 215, 48)',
                        'rgb(255, 159, 64)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)'
                    ],
                    borderWidth: 1
                }]
            };
            new Chart(barChart, {
                type: 'bar',
                data: data,
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                },
            });
        // });
    },
}

</script>
