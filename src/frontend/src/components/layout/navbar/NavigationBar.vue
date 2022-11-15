<template>
  <div class="max-w-[1440px] bg-[#FFFCE8] h-[80px] px-[84px]">
    <div class="h-full py-4 grid grid-cols-12 gap-x-8">
      <div class="col-span-2 border-2 border-solid border-black">Logo</div>
      <div class="col-span-7 border-2 border-solid border-black">
        <SearchBar />
      </div>
      <div class="col-span-3 border-2 border-solid border-black">
        <ProfileItem />
      </div>
    </div>
  </div>
</template>

<script setup>
import SearchBar from "@/components/layout/navbar/SearchBar.vue";
import ProfileItem from "@/components/layout/navbar/ProfileItem.vue";
</script>

<style lang="scss" scoped></style>
