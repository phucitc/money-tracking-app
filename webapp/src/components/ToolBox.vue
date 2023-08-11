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
          <div class="col d-none">
            <label for="basic-url" class="form-label"><strong>Enter a back-half you want (optional)</strong></label>
            <input type="text" class="form-control" name="short_url_alias" v-model="this.short_url_alias" placeholder="Example: my-link" aria-label="Enter a long link"
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
          <div class="col">
            <label for="basic-url" class="form-label"><strong>Your short URL</strong></label>
              <div class="input-group mb-3">
                <input type="text" class="form-control" name="short_url" v-model="this.short_url" placeholder="https://zipit.link/your-link"
                       aria-label="Enter a long link" readonly disabled
                       aria-describedby="button-addon2">
                <button class="btn btn-outline-secondary" type="button" id="button-addon2" @click="this.copy_short_url">{{ this.btn_copy_text }}</button>
              </div>
          </div>
        </div>
        <div class="row">
          <div class="col text-center">
            <button class="btn btn-primary"  @click="this.zip_another_link">{{  this.btn_zip_another_text }}</button>
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
      short_url_alias: '',
      short_url: '',
      is_show_result: false,
      btn_copy_text: 'Copy',
      btn_zip_url_text: 'Zip your URL',
      btn_zip_another_text: 'Zip another URL',
      form_css_was_validated: '',
    }
  },
  setup() {
  },
  mounted() {
  },
  methods: {
    submit_form() {},
    async generate_short_link() {
      try {
        this.long_url = this.long_url.trim();
        this.short_url_alias = this.short_url_alias.trim();
        if ( this.long_url === '' ) {
          this.form_css_was_validated = 'was-validated';
          return;
        }

        let btn_zip_url_text_ori = this.btn_zip_url_text;
        this.btn_zip_url_text = get_border_spinner();
        const response = await axios.post( import.meta.env.VITE_BE_URL + '/api/url/short-url', {
          long_url: this.long_url,
          short_url_alias: '',
        }).finally(() => {
          this.btn_zip_url_text = btn_zip_url_text_ori;
        });

        let short_link = response.data.short_link;
        if ( short_link !== '' ) {
          this.short_url = short_link;
          this.is_show_result = true;
          this.long_url_disable = true;
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    zip_another_link() {
      this.long_url = '';
      this.long_url_disable = false;
      this.short_url_alias = '';
      this.short_url = '';
      this.is_show_result = false;
      this.btn_copy_text = 'Copy';
    },
    copy_short_url() {
      navigator.clipboard.writeText(this.short_url);
      this.btn_copy_text = 'Copied';
    }
  }
};
</script>