<script setup>
import { ref } from "vue";

const name = ref("Hello world");
</script>

<template>
  <h1>Hello {{ name }}</h1>
</template>
