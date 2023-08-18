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
        <div class="col-2">
        </div>
        <div class="col">
          <ToolBox/>
        </div>
        <div class="col-2"></div>
      </div>
    </div>
    <Footer/>
  </main>
</template>
