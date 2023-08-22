<script setup>
import AdminTopMenu from "@/admin/components/AdminTopMenu.vue";
</script>

<template>
  <main>
    <div v-if="this.is_auth != null">
      <div v-if="this.is_auth">
        <AdminTopMenu />
      </div>
      <div v-else>
        <div class="container">
          <div class="row">
            <div class="col text-center py-5">
              <h2 class="text-danger">Sorry, Access restrict!</h2>
              <router-link to="/" class="btn btn-primary">Back to home</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from "axios";
import {get_end_point} from "@/ultils/helper";
import store from "@/ultils/store";

export default {
  data() {
    return {
      endpoint: get_end_point(),
      urls: [],
      is_auth: null
    }
  },
  beforeCreate() {
    if (!store.getters.getToken) {
      this.$router.push('/')
    }
  },
  created() {
    this.get_all_urls();
  },
  setup() {
  },
  mounted() {
  },
  methods: {
    get_all_urls() {
      const token = store.getters.getToken;

      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      };

      axios.get(this.endpoint + '/admin-api/get-urls', config)
      .then(response => {
        this.is_auth = true
        this.urls = response.data
      })
      .catch(error => {
        if (error.response.status === 401) {
          this.is_auth = false
        }
      })
    }
  }
};
</script>
