<template>
  <div class="login">
     <button @click="login">Log in</button>
     <button @click="signup">Signup</button>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .login {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

<script>
import {useAuth0} from '@auth0/auth0-vue';
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
      };
    },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>