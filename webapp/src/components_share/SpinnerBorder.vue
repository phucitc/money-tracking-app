<template>
  <div :class="this.is_loading ? 'w-100 text-center text-primary' : 'd-none'">
    <div class="spinner-border" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SpinnerBorder',
  props: ['is_loading'],
}
</script>