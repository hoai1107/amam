<script setup>
import { ref } from "vue";
import ButtonItem from "@/components/ButtonItem.vue";
import SortMenu from "@/components/SortMenu.vue";
const name = ref("Hello World");
</script>

<template>
  <p>{{ name }}</p>
  <ButtonItem type="primary" state="normal"></ButtonItem>
  <SortMenu></SortMenu>
</template>
