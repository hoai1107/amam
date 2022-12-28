<template>
  <div class="flex flex-row">
    <div class="flex flex-col items-center w-1/3">
      <Avatar></Avatar>
      <div class="flex flex-row mt-2">
        <SvgIcon
          size="24"
          type="mdi"
          style="color: blue"
          :path="mdiCameraOutline"
        ></SvgIcon>
        <p class="text-blue ml-2">change</p>
      </div>
    </div>
    <div class="flex flex-col ml-4">
      <p class="text-2xl font-semibold">Floyd Miles</p>
      <p class="text-gray-400 mt-1">camlansuc@gmail.com</p>
      <div class="flex flex-row text-blue gap-x-8 mt-2">
        <p>0 following</p>
        <p>0 follower</p>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  name: String,
});

import Avatar from "@/components/ui/Avatar.vue";
import { mdiCameraOutline } from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";
</script>

<style lang="scss" scoped></style>
