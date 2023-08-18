<template>
    <footer class="d-flex flex-wrap justify-content-between align-items-center fixed-bottom">
      <p class="text-center text-body-secondary w-100">© {{ this.current_year }} ZIPIT Team</p>
    </footer>
</template>

<script>
export default {
  data() {
    return {
      current_year: new Date().getFullYear()
    }
  }
}
</script>