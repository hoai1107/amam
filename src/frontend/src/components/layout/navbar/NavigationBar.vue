<template>
  <div class="w-full bg-[#FFFCE8] h-[80px] px-[84px]">
    <div class="h-full py-4 grid grid-cols-12 gap-x-8">
      <div class="col-span-2 border-2 border-solid border-black">
        <!-- <img class="" src="@/assets/test.jpg" alt="AMAM" /> -->
        <div></div>
      </div>
      <div class="col-span-7">
        <SearchBar />
      </div>
      <div class="col-span-3">
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
