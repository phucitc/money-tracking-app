<template>
  <header class="p-3 text-zt-dark">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none">
          <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap">
            <use xlink:href="#bootstrap"></use>
          </svg>
        </a>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li>
            <router-link to="/admin" class="nav-link px-2 text-white text-logo">ZIPIT</router-link>
          </li>
          <li><router-link to="/admin/urls" class="nav-link px-2 text-white">URLs</router-link></li>
        </ul>
        <div class="text-end">
          <button type="button" class="btn bg-primary-300 text-white" @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </header>
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
        logout() {
          auth0.logout()
        },
      };
    },
};
</script>