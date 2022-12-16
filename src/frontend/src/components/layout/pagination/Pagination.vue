<template>
  <div class="pt-3 flex flex-row gap-x-3 w-fit mx-auto mt-3 items-center">
    <div>
      <SvgIcon
        class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
        size="24"
        type="mdi"
        :path="mdiChevronDoubleLeft"
      ></SvgIcon>
    </div>
    <div>
      <SvgIcon
        class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
        size="24"
        type="mdi"
        :path="mdiChevronLeft"
      ></SvgIcon>
    </div>
    <div class="px-3 h-[40px]">
      <div class="flex flex-row gap-3">
        <router-link
          v-for="page in pages(props.currentPage, props.totalPages)"
          class="rounded py-2 px-4 hover:bg-blueSky-light-800 cursor-pointer"
          v-bind:key="page"
          :class="{ selected: page === currentPage }"
          :to="{ name: routeName, query: { page_index: page } }"
        >
          {{ page }}
        </router-link>
      </div>
    </div>
    <div>
      <SvgIcon
        class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
        size="24"
        type="mdi"
        :path="mdiChevronRight"
      ></SvgIcon>
    </div>
    <div>
      <SvgIcon
        class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
        size="24"
        type="mdi"
        :path="mdiChevronDoubleRight"
      ></SvgIcon>
    </div>
  </div>
</template>

<script setup>
import {
  mdiChevronLeft,
  mdiChevronRight,
  mdiChevronDoubleLeft,
  mdiChevronDoubleRight,
} from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";

const props = defineProps({
  currentPage: Number,
  totalPages: Number,
  routeName: String,
});

const pages = (currentPage, totalPages) => {
  const range = [];
  for (
    let i = Math.max(1, currentPage - 2);
    i <= Math.min(totalPages, currentPage + 2);
    ++i
  ) {
    range.push(i);
  }
  return range;
};
</script>

<style lang="scss" scoped>
.selected {
  background-color: theme("colors.blueSky.DEFAULT");
  border: 1px solid;
}
</style>
