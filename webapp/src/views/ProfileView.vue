<script setup>
import NavBar from '../components/NavBar.vue'
</script>
<template>
  <div class="profile">
    <NavBar/>
    <router-link to="/profile">Profile</router-link>
    <h1>This is an Profile page</h1>
  </div>
</template>

<script>
export default {
  setup() {
  },
  mounted() {
    console.log(this.$store.getters.getAccessToken)
  },
  methods: {
  }
};
</script>


<style>
@media (min-width: 1024px) {
  .profile {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>