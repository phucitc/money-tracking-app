<template>
<div class="modal fade user-dashboard" id="modal_url" ref="modal_url" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-lg">
    <div class="modal-content">
      <div class="modal-header border-0">
        <h4 class="modal-title" id="exampleModalLabel"><strong>Edit Link</strong></h4>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
          <form class="row g-3 needs-validation" novalidate  @submit.prevent="prevent_submit_form">
          <div class="col-md-12 mb-3">
            <label for="long_url" class="form-label">Title</label>
            <input type="text" class="form-control"
                   id="long_url"
                   v-model="this.url_alias.title"
                   required />
            <div class="valid-feedback">
              Looks good!
            </div>
          </div>
          <div class="col-md-6">
            <label for="domain" class="form-label">Domain</label>
            <select class="form-select" id="domain" required disabled
              v-model="this.url_alias.domain_id">
              <option v-for="option in this.domains" :value="option.id">{{ option.domain_name }}</option>
            </select>
            <div class="invalid-feedback">
              Please select your domain.
            </div>
          </div>
          <div class="col-md-6">
            <label for="long_url" class="form-label">Back-half</label>
            <input type="text" class="form-control"
                   id="short_url"
                   v-model="this.url_alias.public_id"
                   required />
          </div>

        </form>
      </div>
      <div class="modal-footer border-0">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" >Save changes</button>
      </div>
    </div>
  </div>
</div>
</template>
<script>
import {prevent_submit_form} from "@/ultils/helper";

export default {
  name: 'ModalURL',
  methods: {prevent_submit_form},
  props: ['url_alias'],
  data() {
    return {
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
    }
  }

}
</script>