<template>
  <header class="p-3 text-bg-dark">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none">
          <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap">
            <use xlink:href="#bootstrap"></use>
          </svg>
        </a>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li><a href="#" class="nav-link px-2 text-secondary">Home</a></li>
          <li><a href="#" class="nav-link px-2 text-white d-none">Features</a></li>
          <li><a href="#" class="nav-link px-2 text-white d-none">Pricing</a></li>
          <li><a href="#" class="nav-link px-2 text-white d-none">FAQs</a></li>
          <li><a href="#" class="nav-link px-2 text-white d-none">About</a></li>
        </ul>

        <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3 " role="search">
          <input type="search" class="form-control form-control-dark text-bg-dark d-none" placeholder="Search..."
                 aria-label="Search">
        </form>

        <div class="text-end">
          <button type="button" class="btn btn-outline-light me-2" @click="login">Login</button>
          <button type="button" class="btn btn-warning" @click="signup">Sign-up</button>
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