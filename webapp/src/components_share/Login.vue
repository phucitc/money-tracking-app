<template>
  <main>
    <div class="container">
      <div class="row">
        <div class="col py-5 text-center">
          <button type="button" class="btn bg-primary-300 text-white" @click="login">Login</button>
        </div>
      </div>
    </div>
  </main>
</template>

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
        auth0.loginWithRedirect()
      },
    };
  },
};
</script>