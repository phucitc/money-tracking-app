<template>
  <div>
    <h2>Signup</h2>
     <div>
      <button @click="login">Log in</button>
       <button @click="signup">Signup</button>
    </div>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import {useAuth0} from '@auth0/auth0-vue';


export default {
  setup() {
      const auth0 = useAuth0();
      return {
        login() {
          auth0.loginWithRedirect();
        },
        signup() {
          auth0.loginWithRedirect( {authorizationParams: {screen_hint: 'signup'}});
        }
      };
    },
  data() {
    console.log(import.meta.env);
    return {
      email: '',
      password: '',
      errorMessage: ''
    };
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