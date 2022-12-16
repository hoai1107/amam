<template>
  <div
    class="bg-yellow py-1 px-2 border border-solid border-black rounded-sm inline text-xs"
  >
    {{ props.name }}
  </div>
</template>

<script setup>
const props = defineProps(["name"]);
</script>

<style lang="scss" scoped></style>
