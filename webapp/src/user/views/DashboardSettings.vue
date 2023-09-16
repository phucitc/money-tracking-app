<template>
  <Header />
  <div class="container-fluid dashboard">
    <div class="row">
      <LeftSideBar />
      <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 py-4">
        <h2>Settings - Early Access</h2>

      </main>
    </div>
  </div>

</template>
<script setup>
import LeftSideBar from "@/user/components/LeftSideBar.vue";
import Header from "@/user/components/Header.vue";
</script>