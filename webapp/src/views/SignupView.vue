<template>
  <div>
    <h2>Signup</h2>
    <form @submit.prevent="signup">
      <div>
        <label>Email:</label>
        <input type="email" v-model="email" required>
      </div>
      <div>
        <label>Password:</label>
        <input type="password" v-model="password" required>
      </div>
      <button type="submit">Signup</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import auth0 from 'auth0-js';

export default {
  data() {
    console.log(import.meta.env);
    return {
      email: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    signup() {
      const webAuth = new auth0.WebAuth({
        domain: import.meta.env.VITE_AUTH0_DOMAIN,
        clientID: import.meta.env.VITE_AUTH0_CLIENTID,
        responseType: 'code',
        responseMode: 'redirectUri',
        redirectUri: import.meta.env.VITE_AUTH0_CALLBACK,
      });

      webAuth.signup(
        {
          email: this.email,
          password: this.password,
          connection: 'Username-Password-Authentication',
          responseType: 'token code',
          responseMode: 'redirectUri',
          redirectUri: import.meta.env.VITE_AUTH0_CALLBACK,
        },
        (err) => {
          if (err) {
            console.error('Error signing up:', err);
            this.errorMessage = err
          } else {
            console.log('Sigcd nup successful!');
          }
        }
      );
    },
  },
};
</script>

<style scoped>
/* Add your custom styles here */
</style>