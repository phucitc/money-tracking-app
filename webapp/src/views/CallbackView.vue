<template>
  <div>
    <h2>Callback</h2>
  </div>
</template>
<script>
import { useRoute } from 'vue-router';
import axios from "axios";

export default {
  data() {
    console.log(import.meta.env);
    return {
      auth0_code: '',
      auth0_state: '',
    };
  },
  setup() {
    console.log(import.meta.env);
  },
  mounted() {
    this.postData();
  },
  methods: {
    async postData() {
      try {
        const route = useRoute();
        this.auth0_code = route.query.code;
        this.auth0_state = route.query.state;
        console.log(this.auth0_code)
        const response = await axios.post(import.meta.env.VITE_BE_URL + '/callback', {
          auth0_code: this.auth0_code,
          auth0_state: this.auth0_state
        });
        // Handle the response
        console.log(response.data);
      } catch (error) {
        // Handle error
        console.error(error);
      }
    },
  }
};
</script>