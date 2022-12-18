<template>
  <div class="w-full bg-[#FFFCE8] h-fit px-[84px] py-4 mb-6 flex">
    <div
      class="w-[1272px] h-full grid grid-cols-12 gap-x-6 items-center m-auto"
    >
      <div class="col-span-2 border-black">
        <router-link :to="{ name: 'home' }">
          <img
            class="object-center object-none"
            src="@/assets/img/logo-sm.png"
            alt="logo"
          />
        </router-link>
      </div>
      <div class="col-span-7">
        <SearchBar />
      </div>
      <div class="col-span-3 h-full">
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
