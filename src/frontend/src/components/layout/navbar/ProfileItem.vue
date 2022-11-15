<template>
  <div class="h-full w-full">
    <div class="flex flex-row gap-[20px] h-full items-center">
      <div
        class="w-[24px] h-[28px] border-2 border-solid border-b-dark-violet-100"
      ></div>
      <div
        class="w-[48px] h-[48px] border-2 border-solid border-b-dark-violet-100"
      ></div>
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
</script>

<style lang="scss" scoped></style>
