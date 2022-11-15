<template>
  <div>Question in Category</div>
  <div>Category: {{ props.category }}</div>
</template>

<script setup>
const props = defineProps({
  category: String,
});
</script>

<style lang="scss" scoped></style>
