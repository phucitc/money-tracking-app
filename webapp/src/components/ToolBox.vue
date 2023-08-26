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

      <div v-if="!this.is_show_result">
        <div class="row">
          <div class="col">
            <label for="basic-url" class="form-label"><strong>Domain</strong></label>
            <input type="text" class="form-control" placeholder="zipit.link" aria-label="Enter a long link" readonly disabled
                   aria-describedby="button-addon2">
          </div>
          <div class="col-1 p-0 d-none">
            <label for="basic-url" class="form-label">&nbsp;</label>
            <input type="text" class="form-control text-center" placeholder="/" readonly disabled
                   aria-describedby="button-addon2">
          </div>
          <div class="col">
            <label for="basic-url" class="form-label"><strong>Enter a back-half you want (optional)</strong></label>
            <input type="text" class="form-control" name="alias_name" v-model="this.alias_name" placeholder="Example: my-link" aria-label="Enter a long link"
                   aria-describedby="button-addon2">
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
          <div class="col col-md-8">
            <label class="form-label" for="short_url"><strong>Your short URL</strong></label>
            <div class="input-group mb-3">
              <input type="text" class="form-control" name="short_url" id="short_url" v-model="this.short_url" placeholder="https://zipit.link/your-link"
                     aria-label="Enter a long link" readonly disabled
                     aria-describedby="button-addon2">
              <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="this.copy_url()">{{ this.btn_copy_text }}</button>
            </div>
            <div v-if="this.list_alias.length > 0">
            <label class="form-label" for="alias"><strong>Your Aliases URL</strong></label>
            </div>
            <div v-for="(item, index) in this.list_alias">
              <div class="input-group mb-3">
                <input type="text" class="form-control" name="short_url" id="alias" v-model="item.alias_name" placeholder="https://zipit.link/your-link"
                       aria-label="Enter a long link" readonly disabled
                       aria-describedby="button-addon2">
                <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="this.copy_alias_url(index)">{{ item.copied ? "Copied" : "Copy" }}</button>
              </div>
            </div>
            <div class="input-group">
              <div class="text-center w-100">
                <button class="btn btn-primary btn-large"  @click="this.zip_another_link">{{  this.btn_zip_another_text }}</button>
              </div>
            </div>
          </div>
          <div class="col col-md-4">
            <div class="text-center">
              <div class="qrcode-box overflow-hidden">
                <img :src="this.qrcode_base64" alt="QR Code" class="img-fluid">
                <a :href="this.qrcode" class="link-success link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover btn-download-qrcode">Download</a>
              </div>

            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>
<script>
import axios from "axios";
import {get_border_spinner} from "@/ultils/helper";

export default {
  data() {
    return {
      long_url: '',
      long_url_disable: false,
      alias_name: '',
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
    }
  },
  setup() {
  },
  mounted() {
    console.log(location.host)
  },
  methods: {
    submit_form() {},
    async generate_short_link() {
      try {
        this.long_url = this.long_url.trim();
        this.alias_name = this.alias_name.trim();
        if ( this.long_url === '' ) {
          this.form_css_was_validated = 'was-validated';
          return;
        }

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
        }
      } catch (error) {
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