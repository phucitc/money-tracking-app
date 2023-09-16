<template>
  <Header />
  <div class="container-fluid dashboard">
    <div class="row">
      <LeftSideBar />
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 py-4">
        <div class="row">
          <div class="col-md-2"></div>
          <div class="col-md-8">
            <h2><strong>Links</strong></h2>
          </div>
          <div class="col-md-2"></div>
        </div>
        <div class="row mt-4">
          <div class="col-md-2"></div>
          <div class="col-md-8">
            <SpinnerBorder :is_loading="this.is_loading" />

            <div class="card mb-3" v-for="(url_alias, index) in this.list_aliases">
              <div class="card-body">
                <div class="row">
                  <div class="col-md-1 text-center">
                    <div class="form-check mt-1">
                      <input class="form-check-input cursor-pointer" type="checkbox" value="" />
                      <img :src="url_alias.destination_logo" class="img-fluid"  alt="url logo"/>
                    </div>

                  </div>

                  <div class="col-md-8">
                    <h5 class="card-title">Title</h5>
                    <h6 class="card-subtitle mb-2">
                      <a
                          :href=url_alias.short_url
                          class="text-decoration-none"
                          target="_blank">{{ url_alias.short_url }}</a>
                    </h6>
                    <p class="card-text">
                      <a
                          :href=url_alias.long_url
                          target="_blank"
                          class="text-decoration-none text-black">{{ url_alias.long_url }}</a></p>
                    <div>
                      <span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 16">
                          <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1v-3zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V7zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1V2z"/>
                        </svg>
                      </span>
                      <span class="mx-2">
                        <span class="badge text-bg-light small">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-lock-fill" viewBox="0 0 16 16">
                            <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/>
                          </svg>
                          <span class="position-relative tp-2 text-black cursor-pointer">Click data</span>
                        </span>
                      </span>
                      <span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar" viewBox="0 0 16 16">
                          <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
                        </svg>
                        <span class="position-relative tp-2">&nbsp;{{ url_alias.created_at }}</span>
                      </span>
                    </div>
                  </div>

                  <div class="col-md-3 text-end">
                      <div class="clearfix mt-1"></div>
                      <button type="button" class="btn btn-secondary btn-sm me-2" @click="copy_url(url_alias)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-copy" viewBox="0 0 16 16">
                          <path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V2Zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H6ZM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1H2Z"/>
                        </svg>
                        {{ url_alias.copied ? "Copied" : "Copy" }}
                      </button>
                      <button type="button" class="btn btn-secondary btn-sm me-2" @click="this.open_modal_edit_url(url_alias)">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                          <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                        </svg>
                      </button>
                      <div class="btn-group">
                        <button class="btn btn-secondary btn-sm dropdown-toggle no-dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots" viewBox="0 0 16 16">
                              <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z"/>
                            </svg>
                        </button>
                        <ul class="dropdown-menu">
                          <li><a class="dropdown-item" href="#">Delete</a></li>
                        </ul>
                      </div>

                  </div>
                </div>

              </div>
            </div>
            <div class="clearfix"></div>
            <div class="d-flex justify-content-center">
            <nav aria-label="" >
              <ul class="pagination">
                <li v-for="index in this.total_pages"
                    :class="{'page-item': true, 'active': index === this.current_page}"
                    :aria-current="index === this.current_page ? 'page': ''">
                  <span v-if="index === this.current_page" class="page-link"> {{ index }}</span>
                  <span v-else>
                    <a class="page-link" href="#">{{ index }}</a>
                  </span>
                </li>
              </ul>
            </nav>
              </div>
          </div>
          <div class="col-md-2"></div>
        </div>

      </main>
    </div>
  </div>
  <ModalURL :url_alias="this.modal_url_alias_data"/>

</template>
<script>
import LeftSideBar from "@/user/components/LeftSideBar.vue";
import Header from "@/user/components/Header.vue";
import {useAuth0} from "@auth0/auth0-vue";
import axios from "axios";
import {get_end_point, copy_url} from "@/ultils/helper";
import SpinnerBorder from "@/components_share/SpinnerBorder.vue";
import ModalURL from "@/user/components/ModalURL.vue";
import {Modal} from "bootstrap";
export default {
  components: {
    ModalURL,
    SpinnerBorder,
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
      list_aliases: [],
      total_pages: 0,
      current_page: 1,
      is_loading: true,
      modal_url: null,
      modal_url_alias_data: {},
    }
  },
  created() {
    const auth0 = useAuth0()
    this.axios_config.headers.Authorization = 'Bearer ' + auth0.idTokenClaims.value.__raw
  },
  mounted() {
    this.get_list_aliases()
    this.modal_url = new Modal(document.getElementById('modal_url'), {})
  },
  methods: {
    copy_url,
    async get_list_aliases() {
      const response = await axios.get(get_end_point() + '/user/url', this.axios_config)
          .finally(() => {
                this.is_loading = false
              }
          );
      const data = response.data
      this.list_aliases = data.list_aliases
      this.total_pages = data.total_pages
    },
    open_modal_edit_url(url_alias) {
      this.modal_url_alias_data = url_alias
      this.modal_url.show()
    }
  }
}
</script>