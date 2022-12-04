<template>
  <div class="h-12 mb-3 flex flex-row gap-3">
    <!--Avatar---->
    <div
      class="aspect-square h-full cursor-pointer flex grow-0 items-center content-center"
    >
      <img
        class="avatar-container"
        src="@/assets/img/user.webp "
        alt="avatar"
      />
    </div>

    <!--Meta Data-->
    <div class="flex flex-col">
      <!--Post's Username-->
      <div class="text-base font-semibold">Hoai Tu</div>

      <!--Time, View-->
      <div class="flex flex-row gap-3 text-gray-400">
        <div>{{ props.hoursFromLastEdit }} hours ago</div>
        <div>{{ props.views }} views</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  hoursFromLastEdit: Number,
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
