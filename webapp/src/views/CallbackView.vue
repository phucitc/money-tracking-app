<template>
  <div>
    <h2>Callback</h2>
  </div>
</template>
<script>
import {useRoute} from 'vue-router';
import axios from "axios";
import {useAuth0} from "@auth0/auth0-vue";
import {mapState, mapActions} from 'vuex';

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
        this.$router.push('/')
      } else {
        // action: Login
        await auth0.checkSession();
        this.auth0AccessToken = await auth0.getAccessTokenSilently()
        if (await auth0.isAuthenticated.value) {
          this.auth0Token = auth0.idTokenClaims.value.__raw

          this.updateToken(this.auth0Token)
          this.updateAccessToken(this.auth0AccessToken)
          this.updateIsAuth(true)

          // TODO: Send request to server to llogin then redirect to URL
          this.$router.push('/dashboard')
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