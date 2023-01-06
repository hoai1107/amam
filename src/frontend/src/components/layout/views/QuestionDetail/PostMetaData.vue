<template>
  <div class="h-12 mt-2 flex flex-row gap-3">
    <!--Avatar---->
    <div
      class="aspect-square h-full cursor-pointer flex grow-0 items-center content-center"
    >
      <img v-if="avatar" class="avatar-container" :src="avatar" alt="avatar" />
      <img
        v-else
        class="avatar-container"
        src="@/assets/img/user.webp "
        alt="avatar"
      />
    </div>

    <!--Meta Data-->
    <div class="flex flex-col">
      <!--Post's Username-->
      <div class="text-base font-semibold">{{ username }}</div>

      <!--Time, View-->
      <div class="flex flex-row gap-3 text-gray-400">
        <div>{{ props.timeInterval }}</div>
        <div>{{ props.views }} views</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  username: String,
  avatar: String,
  timeInterval: String,
  views: Number,
});
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
