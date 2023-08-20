<template>
  <div class="container">
    <div class="row">
      <div class="col text-center py-4">
        <h2 class="text-success">Logout...</h2>
      </div>
    </div>
  </div>
</template>
<script>
import {useAuth0} from '@auth0/auth0-vue';
export default {
  mounted() {
    this.logout()
  },
  setup() {
      const auth0 = useAuth0();
      return {
        logout() {
          auth0.logout();
        },
      };
    },
};
</script>
