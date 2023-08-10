<template>
  <h1 class="text-center pt-5">Shorten a long link</h1>
  <div class="toolbox">
    <div class="mb-3">
      <label for="basic-url" class="form-label"><strong>Paste a long link</strong></label>
      <input type="text" class="form-control" name="long_url" v-model="this.long_url" placeholder="Example: https://your-domain.com/your-url-too-long" aria-label="Enter a long link"
             aria-describedby="button-addon2">
    </div>
    <div class="mb-3" v-if="!this.is_show_result">
      <div class="row">
        <div class="col">
          <label for="basic-url" class="form-label"><strong>Domain</strong></label>
          <input type="text" class="form-control" placeholder="zipit.link" aria-label="Enter a long link" readonly disabled
                 aria-describedby="button-addon2">
        </div>
        <div class="col-1">
          <label for="basic-url" class="form-label">&nbsp;</label>
          <input type="text" class="form-control text-center" placeholder="/" aria-label="Enter a long link" readonly disabled
                 aria-describedby="button-addon2">
        </div>
        <div class="col">
          <label for="basic-url" class="form-label"><strong>Enter a back-half you want (optional)</strong></label>
          <input type="text" class="form-control" name="short_url_alias" v-model="this.short_url_alias" placeholder="Example: my-link" aria-label="Enter a long link"
                 aria-describedby="button-addon2">
        </div>
      </div>
      <div class="row mt-3">
        <div class="col text-center">
          <button class="btn btn-primary btn-large" @click="this.generate_short_link">Zip your link</button>
        </div>
      </div>
    </div>

    <div class="mb-3" v-if="this.is_show_result">
      <div class="row">
        <div class="col">
          <label for="basic-url" class="form-label">Your short link</label>
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
          <button class="btn btn-primary"  @click="this.zip_another_link">Zip another link</button>
        </div>
      </div>
    </div>

  </div>
</template>
<script>
import axios from "axios";

export default {
  data() {
    return {
      long_url: '',
      short_url_alias: '',
      short_url: '',
      is_show_result: false,
      btn_copy_text: 'Copy'
    }
  },
  setup() {
  },
  mounted() {
  },
  methods: {
    async generate_short_link() {
      try {
        this.long_url = this.long_url.trim();
        this.short_url_alias = this.short_url_alias.trim();
        if ( this.long_url === '' ) {
          return;
        }

        const response = await axios.post( import.meta.env.VITE_BE_URL + '/api/url/short-url', {
          long_url: this.long_url,
          short_url_alias: '',
        });

        let short_link = response.data.short_link;
        if ( short_link !== '' ) {
          this.short_url = short_link;
          this.is_show_result = true;
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    zip_another_link() {
      this.long_url = '';
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