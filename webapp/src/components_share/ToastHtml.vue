<template>
   <div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div id="live_toast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
      <div class="toast-header">
        <strong class="me-auto">{{header_content}}</strong>
        <small>{{date_friendly}}</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body">
        {{message}}
      </div>
    </div>
  </div>
</template>
<script setup>
defineProps(['header_content', 'date_friendly', 'message'])
</script>
