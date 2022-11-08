<script setup>
import { ref } from "vue";
import ButtonItem from "@/components/ButtonItem.vue";

const name = ref("Hello World");
</script>

<template>
  <p class="text-blue-600 text-xl">{{ name }}</p>
  <ButtonItem type="primary" state="normal"></ButtonItem>
</template>
