<template>
  <div>Question Search</div>
  <div>Search keyword: {{ props.keyword }}</div>
</template>

<script setup>
const props = defineProps({
  keyword: String,
});
</script>

<style lang="scss" scoped></style>
