<template>
  <div>User Profile</div>
  <div>ID: {{ props.id }}</div>
</template>

<script setup>
const props = defineProps({
  id: String,
});
</script>

<style lang="scss" scoped></style>
