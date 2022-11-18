<template>
  <div class="w-full bg-[#FFFCE8] h-fit px-[84px] py-0.5">
    <div class="h-full grid grid-cols-12 gap-x-8 items-center">
      <div class="col-span-2 border-black">
        <img
          class="w-full object-center object-none"
          src="@/assets/img/logo-sm.png"
          alt="logo"
        />
        <div></div>
      </div>
      <div class="col-span-7">
        <SearchBar />
      </div>
      <div class="col-span-3 h-12">
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
