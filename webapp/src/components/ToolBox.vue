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
               placeholder="Example: https://your-domain.com/your-url-too-long" aria-label="Enter a long link" required="">
        <div class="invalid-feedback">
          The Long URL field is required.
        </div>
      </div>

      <div v-if="!this.is_show_result" class="m-0">
        <div class="row">
          <div class="col-md-6 col-sm-12 mt-3">
            <label for="basic-url" class="form-label"><strong>Domain</strong></label>
            <input type="text" class="form-control" placeholder="zipit.link" aria-label="Enter a long link" readonly disabled
                   aria-describedby="button-addon2">
          </div>
          <div class="col-1 p-0 d-none">
            <label for="basic-url" class="form-label">&nbsp;</label>
            <input type="text" class="form-control text-center" placeholder="/" readonly disabled
                   aria-describedby="button-addon2">
          </div>
          <div class="col-md-6 col-sm-12 mt-3">
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
              <input type="text" class="form-control" name="short_url" id="short_url" v-model="this.short_url" placeholder="https://zipit.link/your-link"
                     aria-label="Enter a long link" readonly disabled
                     aria-describedby="button-addon2">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="this.copy_url()">{{ this.btn_copy_text }}</button>
            </div>

            <div v-for="(item, index) in this.list_alias">
              <div class="input-group mb-3">
                <input type="text" class="form-control" name="short_url" id="alias" v-model="item.alias_name" placeholder="https://zipit.link/your-link"
                       aria-label="Enter a long link" readonly disabled
                       aria-describedby="button-addon2">
                <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="this.copy_alias_url(index)">{{ item.copied ? "Copied" : "Copy" }}</button>
              </div>
            </div>
            <div class="text-center d-none d-sm-block">
              <button class="btn btn-secondary btn-large mx-2" data-bs-toggle="offcanvas" data-bs-target="#offcanvas-urls-recent" aria-controls="staticBackdrop">My URLs</button>
              <button class="btn btn-primary btn-large"  @click="this.zip_another_link">{{  this.btn_zip_another_text }}</button>
            </div>
            <div class="mb-4"></div>
          </div>
          <div class="col-md-4 col-sm-12">
            <div class="text-center">
              <div class="qrcode-box overflow-hidden">
                <img :src="this.qrcode_base64" alt="QR Code" class="img-fluid">
                <a :href="this.qrcode" class="link-success link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover btn-download-qrcode">Download</a>
              </div>

            </div>
          </div>
          <div class="col-md-8 col-xs-12 mt-3 d-md-none d-lg-none d-xl-none d-xxl-none">
              <div class="text-center">
                <button class="btn btn-primary btn-large">My URLs</button>
                <button class="btn btn-primary btn-large" @click="this.zip_another_link">{{  this.btn_zip_another_text }}</button>
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
      <div class="card mb-2" v-for="(item, index) in this.urls_recent">
        <div class="card-body">
          <h5 class="card-title">Card title</h5>
          <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>
          <p class="card-text">
            Some quick example text to build on the card title and make up the bulk of the card's
            content.
          </p>
          <a href="#" class="card-link">Card link</a>
          <a href="#" class="card-link">Another link</a>
        </div>
      </div>
    </div>
  </div>

  </div>
</template>
<script>
import axios from "axios";
import {convert_space_to_dash, get_border_spinner} from "@/ultils/helper";
import { Tooltip } from 'bootstrap';
export default {
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
      urls_recent: [],
    }
  },
  setup() {
  },
  mounted() {
    this.tooltip = new Tooltip(this.$refs.alias_name_info, {
      title: "Special characters are not allowed.",
      placement: 'top',
    });

    if (localStorage.urls_recent) {
      this.urls_recent = JSON.parse(localStorage.urls_recent);
      console.log(this.urls_recent)
    }
  },
  methods: {
    submit_form() {},
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

        let short_link = response.data.short_link;
        if ( short_link !== '' ) {
          this.short_url = short_link;
          this.is_show_result = true;
          this.long_url_disable = true;
          this.qrcode_base64 = response.data.qrcode_base64;
          this.qrcode = response.data.qrcode;
          this.list_alias = response.data.list_alias;

          let urls_recent = {}
          if (localStorage.urls_recent) {
            urls_recent = JSON.parse(localStorage.urls_recent);
          }
          let public_id = response.data.public_id;
          // // Check if public_id is exist in urls_recent
          if (urls_recent[public_id] === undefined) {
            let url_recent = {
              long_url: this.long_url,
              short_url: this.short_url,
              qrcode_base64: this.qrcode_base64,
            }
            urls_recent[public_id] = url_recent
            this.urls_recent.push(url_recent)
            localStorage.urls_recent = JSON.stringify(urls_recent);
          }

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
    copy_url() {
      navigator.clipboard.writeText(this.short_url);
      this.btn_copy_text = 'Copied';
      setTimeout(() => {
        this.btn_copy_text = 'Copy';
      }, 1500);
    },
    copy_alias_url(index) {
      const item = this.list_alias[index];
      navigator.clipboard.writeText(item.alias_name);
      item.copied = true;
      setTimeout(() => {
        item.copied = false;
      }, 1500);
    }
  }
};
</script>