<template>
  <Header/>
  <div class="container-fluid dashboard user-dashboard">
    <div class="row">
      <LeftSideBar/>
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div
            class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
          <h1 class="h2"><strong>Create new</strong></h1>
        </div>
        <form class="row g-3 needs-validation" novalidate  @submit.prevent="submit_form">
          <div class="col-md-6">
            <div class="col-md-12 mb-3">
              <label for="long_url" class="form-label"><strong>Destination</strong></label>
              <input type="text" class="form-control" id="long_url" required
                v-model="this.long_url">
              <div class="valid-feedback">
                Looks good!
              </div>
            </div>
            <div class="col-md-12 mb-3">
              <label for="title" class="form-label"><strong>Title</strong> <small>(optional)</small></label>
              <input type="text" class="form-control" id="title" required
                v-model="this.title">
              <div class="valid-feedback">
                Looks good!
              </div>
            </div>

            <div class="row">
              <div class="col-md-12">
                <h5>Short link
                  <span class="svg-pos-sub-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-magic" viewBox="0 0 16 16">
                    <path d="M9.5 2.672a.5.5 0 1 0 1 0V.843a.5.5 0 0 0-1 0v1.829Zm4.5.035A.5.5 0 0 0 13.293 2L12 3.293a.5.5 0 1 0 .707.707L14 2.707ZM7.293 4A.5.5 0 1 0 8 3.293L6.707 2A.5.5 0 0 0 6 2.707L7.293 4Zm-.621 2.5a.5.5 0 1 0 0-1H4.843a.5.5 0 1 0 0 1h1.829Zm8.485 0a.5.5 0 1 0 0-1h-1.829a.5.5 0 0 0 0 1h1.829ZM13.293 10A.5.5 0 1 0 14 9.293L12.707 8a.5.5 0 1 0-.707.707L13.293 10ZM9.5 11.157a.5.5 0 0 0 1 0V9.328a.5.5 0 0 0-1 0v1.829Zm1.854-5.097a.5.5 0 0 0 0-.706l-.708-.708a.5.5 0 0 0-.707 0L8.646 5.94a.5.5 0 0 0 0 .707l.708.708a.5.5 0 0 0 .707 0l1.293-1.293Zm-3 3a.5.5 0 0 0 0-.706l-.708-.708a.5.5 0 0 0-.707 0L.646 13.94a.5.5 0 0 0 0 .707l.708.708a.5.5 0 0 0 .707 0L8.354 9.06Z"/>
                  </svg>
                  </span>
                </h5>

              </div>

              <div class="col-md-4 mb-3">
                <label for="domain" class="form-label"><strong>Domain</strong></label>
                <select class="form-select" id="domain" required disabled
                  v-model="this.domain_id">
                  <option v-for="option in this.domains" :value="option.id">{{ option.domain_name }}</option>
                </select>
                <div class="invalid-feedback">
                  Please select your domain.
                </div>
              </div>
              <div class="col-md-8 mb-3">
                <label for="alias_name" class="form-label"><strong>Custom back-half</strong> (optional)</label>
                <input type="text" class="form-control" id="alias_name"
                  v-model="this.alias_name">
              </div>
            </div>
            <div class="col-md-12 text-center">
              <button class="btn btn-primary" type="submit" @click="this.create_url()">Create</button>
            </div>

          </div>

        </form>
      </main>
    </div>
  </div>
</template>
<script>
import Header from "@/user/components/Header.vue";
import LeftSideBar from "@/user/components/LeftSideBar.vue";
import {useAuth0} from "@auth0/auth0-vue";
import axios from "axios";
import {get_end_point} from "@/ultils/helper";

export default {
  components: {
    Header,
    LeftSideBar
  },
  data() {
    return {
      axios_config: {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': ''
        }
      },
      long_url: '',
      long_url_disable: false,
      title: '',
      domain_id: 0,
      domains: [
        {
          id: 0,
          domain_name: 'zipit.link',
          selected: true
        },
        {
          id: 1,
          domain_name: 'zip.ly',
          selected: false
        }
      ],
      alias_name: '',
      alias_error_msg: '',
      short_url: '',
      is_show_result: false,
      btn_copy_text: 'Copy',
      btn_copy_text_alias: 'Copy',
      btn_zip_url_text: 'Zip your URL',
      btn_zip_another_text: 'Zip another URL',
      form_css_was_validated: '',
      qrcode_base64: '',
      qrcode: '',
      list_alias: [],
      token_non_user: '',
      urls_recent: [],
      is_loading_urls_recent: true,
      tooltips: {
        edit_link: [],
        visit_url: [],
      },
      toast: {
        header_content: '',
        date_friendly: '',
        message: '',
      },
    }
  },
  created() {
    const auth0 = useAuth0()
    this.axios_config.headers.Authorization = 'Bearer ' + auth0.idTokenClaims.value.__raw
  },
  methods: {
    submit_form() {
    },
    async create_url() {
      const response = await axios.post(get_end_point() + '/user/url', {
        long_url: this.long_url,
        title: this.title,
        domain_id: this.domain_id,
        alias_name: this.alias_name,
      }, this.axios_config).finally(() => {
      });
      console.log(response)
      this.$router.push('/dashboard/urls')
    }
  }
}
</script>