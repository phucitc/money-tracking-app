<template>
   <Line id="my-line-chart" :data="chartData" :options="chartOptions" />

</template>

<script>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import {Line} from 'vue-chartjs'

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

export default {
  name: 'LineChart',
  computed: {
    data() {
      return data
    }
  },
  components: {Line},
  data() {
    return {
      chartData: {
        labels: [
          'Sunday',
          'Monday',
          'Tuesday',
          'Wednesday',
          'Thursday',
          'Friday',
          'Saturday'
        ],
        datasets: [{
          data: [15339,
            21345,
            18483,
            24003,
            23489,
            24092,
            12034],
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }]
      },
      chartOptions: {
        responsive: true,
        legend: {
          display: false
        },
        tooltip: {
          boxPadding: 3
        }
      }
    }
  }
}
</script>