<template>
  <div
    class="aspect-square cursor-pointer flex grow-0 items-center content-center"
  >
    <img
      v-if="props.imageSrc"
      class="avatar-container"
      :src="props.imageSrc"
      alt="avatar"
    />
    <img
      v-else
      class="avatar-container"
      src="@/assets/img/user.webp"
      alt="avatar"
    />
  </div>
</template>

<script setup>
const props = defineProps(["imageSrc"]);
</script>

<style lang="scss" scoped>
.avatar-container {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  border: 2px solid black;
  border-radius: theme("borderRadius.DEFAULT");
}
</style>
