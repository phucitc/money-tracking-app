<template>
  <Header />
  <div class="container-fluid dashboard">
    <div class="row">
      <LeftSideBar />
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 py-4">
        <h2>Your URLs</h2>
        <div class="row mt-4">
          <div class="col-md-2"></div>
          <div class="col-md-8">
            <div class="card mb-3" v-for="(url_alias, index) in this.list_aliases">
              <div class="card-body">
                <div class="row">
                  <div class="col-md-1">

                  </div>
                  <div class="col-md-9">
                    <h5 class="card-title">Title</h5>
                    <h6 class="card-subtitle mb-2"><a href="http://localhost:5000/Fvk6C" class="text-decoration-none" target="_blank">http://localhost:5000/Fvk6C</a></h6>
                    <p class="card-text">vnexpress.net/tp-hcm-co-6-quan-thuoc-dien-sap-nhap-4637538.html</p>
                  </div>
                  <div class="col-md-2">

                  </div>
                </div>

              </div>
            </div>
          </div>
          <div class="col-md-2"></div>
        </div>

      </main>
    </div>
  </div>

</template>
<script>
import LeftSideBar from "@/user/components/LeftSideBar.vue";
import Header from "@/user/components/Header.vue";
import {useAuth0} from "@auth0/auth0-vue";
import axios from "axios";
import {get_end_point} from "@/ultils/helper";
export default {
  components: {
    LeftSideBar,
    Header
  },
  data() {
    return {
      axios_config: {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': ''
        }
      },
      list_aliases: []
    }
  },
  created() {
    const auth0 = useAuth0()
    this.axios_config.headers.Authorization = 'Bearer ' + auth0.idTokenClaims.value.__raw
  },
  mounted() {
    this.get_list_aliases()
  },
  methods: {
    async get_list_aliases() {
      const response = await axios.get( get_end_point() + '/user/url', this.axios_config)
          .finally(() => {

          }
        );
      this.list_aliases = response.data.list_aliases
      console.log(this.list_aliases)
    }
  },

}
</script>