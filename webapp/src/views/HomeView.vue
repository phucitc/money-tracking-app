<script setup>
import TheWelcome from '../components/TheWelcome.vue'
import NavBar from '../components/NavBar.vue'
import TopMenu from "@/components/TopMenu.vue";
import ToolBox from "@/components/ToolBox.vue";
import Footer from "@/components/Footer.vue";

</script>

<template>
  <main>
    <TopMenu/>
    <div class="container">
      <div class="row">
        <div class="col-md-2 col-sm-12">
        </div>
        <div class="col-md-8 col-sm-12">
          <ToolBox/>
        </div>
        <div class="col-md-2 col-sm-12"></div>
      </div>
    </div>
    <Footer/>
  </main>
</template>
