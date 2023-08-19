<script setup>
import AdminTopMenu from "@/admin/components/AdminTopMenu.vue";
</script>

<template>
  <main>
    <AdminTopMenu />
  </main>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
