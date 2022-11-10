<template>
  <div>All Questions</div>
  <div>Query: {{ props }}</div>
</template>

<script setup>
const props = defineProps({
  name: String,
  author: String,
});
</script>

<style lang="scss" scoped></style>
