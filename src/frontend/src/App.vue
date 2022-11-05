<script setup>
import { ref } from "vue";
import ButtonItem from "@/components/ButtonItem.vue";

const name = ref("Hello World");
</script>

<template>
  <p>{{ name }}</p>
  <ButtonItem></ButtonItem>
</template>
