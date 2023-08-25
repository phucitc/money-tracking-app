<style>
.callback {
  background: var(--zt-primary);
  color: var(--zt-white);
  height: 100%;
  position: fixed;
}
</style>
<template>
  <div class="container-fluid callback">
    <div class="row">
      <div class="col text-center py-5">
        <div class="spinner-grow text-white" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <div class="spinner-grow text-white mx-1" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <div class="spinner-grow text-white" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import {useRoute} from 'vue-router';
import axios from "axios";
import {useAuth0} from "@auth0/auth0-vue";
import {mapState, mapActions} from 'vuex';
import {get_end_point} from "@/ultils/helper";

export default {
  data() {
    return {
      auth0AccessToken: '',
      auth0Token: '',
      isAuth: false
    }
  },
  setup() {
  },
  mounted() {
    this.postData()
  },
  computed: {
    ...mapState(['accessToken']),
  },
  methods: {
    ...mapActions(['updateToken', 'updateIsAuth', 'updateAccessToken']),
    async postData() {
      const auth0 = useAuth0()
      const route = useRoute()
      const action = route.query.action;
      if (action === 'logout') {
        this.updateToken('')
        this.updateAccessToken('')
        this.updateIsAuth(false)
        // TODO: Send request to server to logout then redirect to URL
        console.log("Logout")
        const vue = this
        setTimeout(function () { vue.$router.push('/') }, 1000)
      } else {
        console.log("Logged")
        // action: Login
        await auth0.checkSession();
        this.auth0AccessToken = await auth0.getAccessTokenSilently()
        this.auth0Token = auth0.idTokenClaims.value.__raw
        this.updateToken(this.auth0Token)
        this.updateAccessToken(this.auth0AccessToken)
        this.updateIsAuth(true)
        if (await auth0.isAuthenticated.value) {
          const config = {
            headers: {
              Authorization: `Bearer ${this.auth0Token}`,
              'Content-Type': 'application/json',
            },
          };

          await axios.post(get_end_point() + '/auth', {}, config)
              .then(response => {
                // const redirect_uri = response.data.redirect_uri
                // if (redirect_uri !== undefined && redirect_uri !== '') {
                //   this.$router.push(redirect_uri)
                // } else {
                //   // TODO: show a toast error
                //   // this.$router.push('/')
                // }
                if (route.query.redirect_url !== undefined && route.query.redirect_url !== '') {
                  this.$router.push(route.query.redirect_url)
                } else {
                  this.$router.push('/dashboard')
                }
              })
              .catch(error => {
                // TODO: show a toast error
                console.log(error)
              })
        }
      }


      // try {
      //   // console.log(isAuthenticated)
      //   const route = useRoute();
      //   this.auth0_code = route.query.code;
      //   this.auth0_state = route.query.state;
      //   // console.log(this.auth0_code)
      //   let payload = {
      //     action: 'auth-callback',
      //     auth0_code: this.auth0_code,
      //     auth0_state: this.auth0_state
      //   }
      //   const response = await axios.post(import.meta.env.VITE_BE_URL + '/auth-callback', payload );
      //   // Handle the response
      //   console.log(response.data);
      // } catch (error) {
      //   // Handle error
      //   console.error(error);
      // }
    },
  }
};
</script>