<template>
  <h1 class="text-center pt-5">Shorten a long URL</h1>
  <div class="toolbox">
    <form
        :class="{'row g-3 needs-validation': true, 'was-validated': this.form_css_was_validated}"
        novalidate @submit.prevent="submit_form">
      <div class="col-12">
        <label for="long_url" class="form-label"><strong>Paste a long URL</strong></label>
        <input type="text" class="form-control" name="long_url" id="long_url"
               v-model="this.long_url"
               :disabled="this.long_url_disable"
               placeholder="Example: https://your-domain.com/your-url-too-long" aria-label="Enter a long link"
               required="">
        <div class="invalid-feedback">
          The Long URL field is required.
        </div>
      </div>

      <div v-if="!this.is_show_result" class="m-0">
        <div class="row">
          <div class="col-md-5 col-sm-12 mt-3">
            <label for="basic-url" class="form-label"><strong>Domain</strong></label>
            <input type="text" class="form-control" placeholder="zipit.link" aria-label="Enter a long link" readonly
                   disabled
                   aria-describedby="button-addon2">
          </div>
          <div class="col-md-7 col-sm-12 mt-3">
            <label for="basic-url" class="form-label"><strong>Enter a back-half you want (optional)</strong>&nbsp;<span
                ref="alias_name_info"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                           class="bi bi-info-circle" viewBox="0 0 16 16">
              <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
              <path
                  d="m8.93 6.588-2.29.287-.082.38.45.083c.294.07.352.176.288.469l-.738 3.468c-.194.897.105 1.319.808 1.319.545 0 1.178-.252 1.465-.598l.088-.416c-.2.176-.492.246-.686.246-.275 0-.375-.193-.304-.533L8.93 6.588zM9 4.5a1 1 0 1 1-2 0 1 1 0 0 1 2 0z"/>
            </svg></span>
            </label>
            <input type="text"
                   :class="{'form-control': true, 'error': this.alias_error_msg !== ''}"
                   name="alias_name" v-model="this.alias_name"
                   placeholder="Example: my-link"
                   aria-label="Enter a back-half you want"
                   v-on:change="this.process_alias_name(this.alias_name)"
            >
            <div class="invalid-feedback">
              {{ this.alias_error_msg }}
            </div>
          </div>
        </div>
        <div class="row mt-3">
          <div class="col text-center">
            <button type="submit" class="btn btn-primary btn-large" @click="this.generate_short_link">
              <span v-html="this.btn_zip_url_text"></span>
            </button>
          </div>
        </div>
      </div>

      <div v-if="this.is_show_result">
        <div class="row">
          <div class="col-md-8 col-sm-12">
            <label class="form-label" for="short_url"><strong>Your shorten URLs</strong></label>
            <div class="input-group mb-3">
              <input type="text" class="form-control" name="short_url" id="short_url" v-model="this.short_url"
                     placeholder="https://zipit.link/your-link"
                     aria-label="Enter a long link" readonly disabled
                     aria-describedby="button-addon2">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2"
                      @click="this.copy_url(this.short_url)">{{ this.btn_copy_text }}
              </button>
            </div>

            <div v-for="(item, index) in this.list_alias">
              <div class="input-group mb-3">
                <input type="text" class="form-control" name="short_url" id="alias" v-model="item.alias_name"
                       placeholder="https://zipit.link/your-link"
                       aria-label="Enter a long link" readonly disabled
                       aria-describedby="button-addon2">
                <button class="btn btn-outline-secondary" type="button" id="button-addon2"
                        @click="this.copy_alias_url(index)">{{ item.copied ? "Copied" : "Copy" }}
                </button>
              </div>
            </div>
            <div class="text-center d-none d-sm-block">
              <button class="btn btn-secondary btn-large mx-2" data-bs-toggle="offcanvas"
                      data-bs-target="#offcanvas-urls-recent"
                      aria-controls="staticBackdrop"
                      @click="this.trigger_open_canvas()">My URLs
              </button>
              <button class="btn btn-primary btn-large" @click="this.zip_another_link">{{
                  this.btn_zip_another_text
                }}
              </button>
            </div>
            <div class="mb-4"></div>
          </div>
          <div class="col-md-4 col-sm-12">
            <div class="text-center">
              <div class="qrcode-box overflow-hidden">
                <img :src="this.qrcode_base64" alt="QR Code" class="img-fluid">
                <a :href="this.qrcode"
                   class="link-success link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover btn-download-qrcode">Download</a>
              </div>

            </div>
          </div>
          <div class="col-md-8 col-xs-12 mt-3 d-md-none d-lg-none d-xl-none d-xxl-none">
            <div class="text-center">
              <button class="btn btn-primary btn-large">My URLs</button>
              <button class="btn btn-primary btn-large" @click="this.zip_another_link">{{
                  this.btn_zip_another_text
                }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </form>

    <!-- History !-->
    <div class="offcanvas offcanvas-end non-user-history-width" data-bs-backdrop="static"
         tabindex="-1" id="offcanvas-urls-recent" aria-labelledby="staticBackdropLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasExampleLabel">Your recent URLs</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div v-if="this.is_loading_urls_recent" class="row mb-2">
          <div content="col">
            <div class="w-100 text-center">
              <div class="spinner-border text-center" role="status">
            <span class="visually-hidden">Loading...</span>
            </div>
          </div>
          </div>
        </div>
        <div class="card mb-2" v-for="(item, index) in this.urls_recent">
          <div class="card-body">
            <div class="row">
              <div class="col-md-1">
                <div class="text-center">
                  <img :src="item.destination_logo" alt="Title" class="img-fluid">
                </div>
              </div>
              <div class="col-md-8 ps-0">
                <h5 class="card-title">{{ item.public_id }} - Untitled</h5>
                <h6 class="card-subtitle mb-2">
                  <a :href="item.short_url"
                     class="text-decoration-none"
                     target="_blank">{{ item.short_url }}</a></h6>
                <p class="card-text">
                  {{ item.long_url }}
                </p>

                <a :href="item.short_url" target="_blank" class="btn btn-primary" ref="btn_url_recent_visit_url">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor"
                       class="bi bi-box-arrow-up-right" viewBox="0 0 16 16">
                    <path fill-rule="evenodd"
                          d="M8.636 3.5a.5.5 0 0 0-.5-.5H1.5A1.5 1.5 0 0 0 0 4.5v10A1.5 1.5 0 0 0 1.5 16h10a1.5 1.5 0 0 0 1.5-1.5V7.864a.5.5 0 0 0-1 0V14.5a.5.5 0 0 1-.5.5h-10a.5.5 0 0 1-.5-.5v-10a.5.5 0 0 1 .5-.5h6.636a.5.5 0 0 0 .5-.5z"/>
                    <path fill-rule="evenodd"
                          d="M16 .5a.5.5 0 0 0-.5-.5h-5a.5.5 0 0 0 0 1h3.793L6.146 9.146a.5.5 0 1 0 .708.708L15 1.707V5.5a.5.5 0 0 0 1 0v-5z"/>
                  </svg>
                </a>
                <button class="mx-2 btn btn-success" @click="this.copy_url(item.short_url, true)" ref="btn_url_recent_copy">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor"
                       class="bi bi-clipboard" viewBox="0 0 16 16">
                    <path
                        d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                    <path
                        d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/>
                  </svg>
                </button>
                <button class="me-2 btn btn-success" ref="btn_url_recent_download_qrcode">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-qr-code-scan" viewBox="0 0 16 16">
                    <path d="M0 .5A.5.5 0 0 1 .5 0h3a.5.5 0 0 1 0 1H1v2.5a.5.5 0 0 1-1 0v-3Zm12 0a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 .5.5v3a.5.5 0 0 1-1 0V1h-2.5a.5.5 0 0 1-.5-.5ZM.5 12a.5.5 0 0 1 .5.5V15h2.5a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5v-3a.5.5 0 0 1 .5-.5Zm15 0a.5.5 0 0 1 .5.5v3a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1 0-1H15v-2.5a.5.5 0 0 1 .5-.5ZM4 4h1v1H4V4Z"/>
                    <path d="M7 2H2v5h5V2ZM3 3h3v3H3V3Zm2 8H4v1h1v-1Z"/>
                    <path d="M7 9H2v5h5V9Zm-4 1h3v3H3v-3Zm8-6h1v1h-1V4Z"/>
                    <path d="M9 2h5v5H9V2Zm1 1v3h3V3h-3ZM8 8v2h1v1H8v1h2v-2h1v2h1v-1h2v-1h-3V8H8Zm2 2H9V9h1v1Zm4 2h-1v1h-2v1h3v-2Zm-4 2v-1H8v1h2Z"/>
                    <path d="M12 9h2V8h-2v1Z"/>
                  </svg>
                </button>
                <button class="me-2 btn btn-secondary opacity-50 disable d-none" ref="btn_url_recent_rename_link">Rename</button>
                <button class="btn btn-secondary opacity-50 disable d-none" ref="btn_url_recent_edit_link">Edit</button>
              </div>
              <div class="col-md-3">
                <div>
                  <img :src="item.qrcode_base64" alt="QR Code" class="img-fluid">
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class=""></div>
        </div>
      </div>
    </div>
  </div>
  <ToastHtml :header_content="this.toast.header_content" :date_friendly="this.toast.date_friendly" :message="this.toast.message" />
</template>
<script>
import axios from "axios";
import {convert_space_to_dash, get_border_spinner, remove_protocol, get_csrf, get_end_point} from "@/ultils/helper";
import Cookies from 'js-cookie';
import { v4 as uuidv4 } from 'uuid';
import {Toast, Tooltip} from 'bootstrap';
import ToastHtml from "@/components_share/ToastHtml.vue";


export default {
  components: {ToastHtml},
  data() {
    return {
      long_url: '',
      long_url_disable: false,
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
  setup() {
  },
  created() {
    // this.heartbeat();
    axios.defaults.headers.common['X-CSRFToken'] = get_csrf();
    let zipit_uuid = Cookies.get('Zipit-Uuid');
    if ( zipit_uuid === undefined ) {
      zipit_uuid = uuidv4()
      Cookies.set('Zipit-Uuid', zipit_uuid, { expires: 365 });
    }
    axios.defaults.headers.common['Zipit-Uuid'] = zipit_uuid;
  },
  mounted() {
    new Tooltip(this.$refs.alias_name_info, {
      title: "Special characters are not allowed.",
      placement: 'top',
    });
  },
  updated() {

    if ( this.$refs.btn_url_recent_edit_link !== undefined ) {
      for (let i = 0; i < this.$refs.btn_url_recent_edit_link.length; i++) {
        new Tooltip(this.$refs.btn_url_recent_edit_link[i], {
          title: "Please purchase a subscription to edit your destination link.",
          placement: 'top',
        });
        this.tooltips['edit_link'].push(new Tooltip(this.$refs.btn_url_recent_edit_link[i], {
          title: "Please purchase a subscription to edit your destination link.",
          placement: 'top',
        }));

        new Tooltip(this.$refs.btn_url_recent_rename_link[i], {
          title: "Please login to change your short link.",
          placement: 'top',
        });

        new Tooltip(this.$refs.btn_url_recent_copy[i], {
          title: "Copy",
          placement: 'top',
        });

        new Tooltip(this.$refs.btn_url_recent_download_qrcode[i], {
          title: "Download QRCODE",
          placement: 'top',
        });

        new Tooltip(this.$refs.btn_url_recent_visit_url[i], {
          title: "Visit URL",
          placement: 'left',
        });
      }
    }

  },
  methods: {
    remove_protocol,
    submit_form() {
    },
    trigger_open_canvas() {
      this.is_loading_urls_recent = true;
      this.get_urls();
    },
    process_alias_name(alias) {
      this.alias_name = convert_space_to_dash(alias);
    },
    async generate_short_link() {
      try {
        this.long_url = this.long_url.trim();
        this.alias_name = this.alias_name.trim();
        if ( this.long_url === '' ) {
          this.form_css_was_validated = 'was-validated';
          return;
        }

        // reset error
        this.alias_error_msg = '';

        let btn_zip_url_text_ori = this.btn_zip_url_text;
        this.btn_zip_url_text = get_border_spinner();
        const response = await axios.post( import.meta.env.VITE_BE_URL + '/api/url/short-url', {
          long_url: this.long_url,
          alias_name: this.alias_name,
        }).finally(() => {
          this.btn_zip_url_text = btn_zip_url_text_ori;
        });
        let response_data = response.data
        let short_link = response_data.short_link;
        if (short_link !== '') {
          this.short_url = short_link;
          this.is_show_result = true;
          this.long_url_disable = true;
          this.qrcode_base64 = response_data.qrcode_base64;
          this.qrcode = response_data.qrcode;

          // this.list_alias = response_data.list_alias;
          // let urls_recent = {}
          // if (localStorage.urls_recent) {
          //   urls_recent = JSON.parse(localStorage.urls_recent);
          // }
          // let public_id = response.data.public_id;
          // // // Check if public_id is exist in urls_recent
          // if (urls_recent[public_id] === undefined) {
          //   let url_recent = {
          //     long_url: this.long_url,
          //     short_url: response_data.list_alias.length > 0 ? response_data.list_alias[0]['alias_name'] : this.short_url,
          //     qrcode_base64: this.qrcode_base64,
          //     public_id: public_id,
          //     destination_logo: response_data.destination_logo,
          //   }
          //   urls_recent[public_id] = url_recent
          //   this.urls_recent.push(url_recent)
          //   localStorage.urls_recent = JSON.stringify(urls_recent);
          // }

        }
      } catch (error) {
        // get response from error
        const data = error.response.data;
        console.log(data)
        if ( data.type === 'alias_name' ) {
          this.form_css_was_validated = 'was-validated';
          this.alias_error_msg = data.message;
          console.log(this.alias_error_msg)
        }
        console.error('Error:', error);
      }
    },
    async get_urls() {
      const response = await axios.get( get_end_point() + '/api/url/short-url');
      this.urls_recent = response.data.list_alias;
      this.is_loading_urls_recent = false;
    },
    zip_another_link() {
      this.long_url = '';
      this.long_url_disable = false;
      this.alias_name = '';
      this.short_url = '';
      this.is_show_result = false;
      this.btn_copy_text = 'Copy';
      this.qrcode_base64 = '';
      this.qrcode = ''
    },
    copy_url(url, is_show_toast = false) {
      navigator.clipboard.writeText(url);
      if (is_show_toast) {
        this.toast.header_content = "Success";
        this.toast.message = "Copied to clipboard";
        const toast_live = document.getElementById('live_toast');
        const toast_bs = Toast.getOrCreateInstance(toast_live);
        toast_bs.show();
        setTimeout(() => {
          toast_bs.hide();
        }, 1500);
      } else {
        this.btn_copy_text = 'Copied';
        setTimeout(() => {
          this.btn_copy_text = 'Copy';
        }, 1500);
      }

    },
    copy_alias_url(index) {
      const item = this.urls_recent[index];
      navigator.clipboard.writeText(item.alias_name);
      item.copied = true;
      setTimeout(() => {
        item.copied = false;
      }, 1500);
    },
    heartbeat() {
      const url = get_end_point() + '/api/heartbeat';
      setInterval(async function () {
        await axios.get(url)
      }, 10000)
    },
  }
};
</script>