<template>
  <div>Single Question</div>
  <div>Question Id: {{ props.id }}</div>
</template>

<script setup>
const props = defineProps({
  id: String,
});
</script>

<style lang="scss" scoped></style>
