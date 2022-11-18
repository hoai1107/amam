<template>
  <div class="h-full w-full">
    <div class="flex flex-row gap-[20px] h-full items-center">
      <!--Noti icon-->
      <div class="flex items-center">
        <SvgIcon size="32" type="mdi" :path="mdiBellOutline"></SvgIcon>
      </div>

      <!--Avatar-->
      <div
        class="img-container w-auto h-full flex grow-0 items-center content-center"
      >
        <img src="@/assets/img/user.webp " alt="avatar" />
      </div>

      <!--Button-->
      <div class="h-full">
        <ButtonItem type="primary" state="normal" text="Create a question" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
import { mdiBellOutline } from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";
</script>

<style lang="scss" scoped>
.img-container {
  font-size: 0;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  border: 2px solid black;
  border-radius: theme("borderRadius.DEFAULT");
}
</style>
