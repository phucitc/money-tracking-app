<template>
  <Header />
  <div class="container-fluid dashboard">
    <div class="row">
      <LeftSideBar />
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div
            class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
          <h1 class="h2">Dashboard - Early Access</h1>
        </div>

      </main>

     </div>
  </div>

</template>

<script>
import store from "@/ultils/store";
import {Bar} from 'vue-chartjs'
import BarChart from "@/components_share/BarChart.vue";
import LineChart from "@/components_share/LineChart.vue";
import Header from "@/user/components/Header.vue";
import LeftSideBar from "@/user/components/LeftSideBar.vue";


export default {
  components: {LeftSideBar, Header, LineChart, BarChart},
  data() {
    return {}
  },
  setup() {
  },
  mounted() {
  },
  methods: {}
};
</script>

