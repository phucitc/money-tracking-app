<script setup>
import NavBar from '../components/NavBar.vue'
</script>
<template>
  <NavBar/>
  <div class="dashboard">
    <h1>This is an Dashboard page</h1>
  </div>
</template>

<script>
import store from "@/ultils/store";

export default {
  setup() {
  },
  mounted() {
    // console.log(store.getters.getToken)
  },
  methods: {
  }
};
</script>


<style>
@media (min-width: 1024px) {
  .dashboard {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>