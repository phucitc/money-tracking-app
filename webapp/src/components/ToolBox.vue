<template>
  <h3 class="text-center pt-5">Zip a long link</h3>
  <div class="toolbox">
    <div class="mb-3">
      <label for="basic-url" class="form-label">Paste a long link</label>
      <input type="text" class="form-control" placeholder="Example: https://your-domain.com/your-url-too-long" aria-label="Enter a long link"
             aria-describedby="button-addon2">
    </div>
    <div class="mb-3">
      <div class="row">
        <div class="col">
          <label for="basic-url" class="form-label">Domain</label>
          <input type="text" class="form-control" placeholder="zipit.link" aria-label="Enter a long link" readonly disabled
                 aria-describedby="button-addon2">
        </div>
        <div class="col-1">
          <label for="basic-url" class="form-label">&nbsp;</label>
          <input type="text" class="form-control text-center" placeholder="/" aria-label="Enter a long link" readonly disabled
                 aria-describedby="button-addon2">
        </div>
        <div class="col">
          <label for="basic-url" class="form-label">Enter a back-half you want (optional)</label>
          <input type="text" class="form-control" placeholder="Example: my-link" aria-label="Enter a long link"
                 aria-describedby="button-addon2">
        </div>
      </div>
    </div>
    <div class="mb-3 text-center">
      <button class="btn btn-primary">Zip It</button>
    </div>
  </div>
</template>
<script setup>
</script>