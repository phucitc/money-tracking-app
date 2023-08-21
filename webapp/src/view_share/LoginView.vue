<template>

</template>

<script>
import {useAuth0} from '@auth0/auth0-vue';
import Login from "@/components_share/Login.vue";
export default {
  // components: {Login},
  // data() {
  //   return {
  //     isAuth: false
  //   }
  // },
  created() {
    const auth0 = useAuth0();
    auth0.loginWithRedirect();
  },

  // setup() {
  //     const auth0 = useAuth0();
  //     return {
  //       login() {
  //         auth0.loginWithRedirect();
  //       },
  //       signup() {
  //         auth0.loginWithRedirect( {authorizationParams: {screen_hint: 'signup'}});
  //       },
  //     };
  //   },

};
</script>

<style scoped>
/* Add your custom styles here */
</style>