<template>
  <div class="h-full w-full">
    <div class="flex flex-row gap-[20px] h-full items-center">
      <div class="w-[24px] h-[28px] border-2 border-solid flex content-center">
        <SvgIcon type="mdi" :path="mdiBellOutline"></SvgIcon>
      </div>
      <div class="w-[48px] h-[48px] border-2 border-solid"></div>
      <ButtonItem
        text="Create a question"
        width="188px"
        height="48px"
        font-size="14px"
        is-primary="true"
      />
    </div>
  </div>
</template>

<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
import { mdiBellOutline } from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";
</script>

<style lang="scss" scoped></style>
