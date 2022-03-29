<script>
import { Line, mixins } from 'vue-chartjs'

export default {
  extends: Line,
  props: ['chartData'],
  mixins: [mixins.reactiveProp],

  mounted () {
    this.renderChart(this.chartData, {responsive: true, maintainAspectRatio: false})
  },
  
}
</script>