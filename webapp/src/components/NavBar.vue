<template>
  <div class="item">
    <div >
      <router-link to="/">Home</router-link>
      <div v-if="this.isAuth">
        <div>
        <router-link to="/dashboard">Dashboard</router-link>
        </div>
        <div>
        <router-link to="/profile">Profile</router-link>
        </div>
        <button @click="logout">Logout</button>
      </div>
      <div v-else>
         <button @click="login">Log in</button>
         <button @click="signup">Signup</button>
      </div>
    </div>
  </div>
</template>

<script>
import {useAuth0} from '@auth0/auth0-vue';
import store from "@/ultils/store";
export default {
  data() {
    return {
      isAuth: false
    }
  },
  setup() {
      const auth0 = useAuth0();
      return {
        login() {
          auth0.loginWithRedirect();
        },
        signup() {
          auth0.loginWithRedirect( {authorizationParams: {screen_hint: 'signup'}});
        },
        logout() {
          auth0.logout();
        }
      };
    },
  mounted() {
    this.isAuth = store.getters.getIsAuth
  },
  methods: {
    // login() {
    //   const auth0 = useAuth0();
    //   auth0.loginWithRedirect();
    // },
    // signup() {
      // createAuth0({
      //   domain: "dev-e0hn8bw4osg50wqz.us.auth0.com",
      //   clientId: "gsV2RRopEbPsVoz1R5XcpVPNtXgM1Uhb",
      //   authorizationParams: {
      //     redirect_uri: 'http://localhost:5000/callback',
      //   screen_hint: 'signup'
      //   }
      // })
      // console.log("AAA")
      // const auth0 = useAuth0();
      // this.$auth0.authorizationParams.screen_hint = 'signup'
      // auth0.loginWithRedirect();
    // },
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>