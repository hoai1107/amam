<template>
  <div class="pt-3 flex flex-row gap-x-3 w-fit mx-auto mt-3 items-center">
    <div>
      <SvgIcon
        v-show="currentPage !== 1"
        class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
        size="24"
        type="mdi"
        :path="mdiChevronDoubleLeft"
        @click="router.push({ name: routeName, query: { page_index: 1 } })"
      ></SvgIcon>
    </div>
    <div>
      <SvgIcon
        v-show="currentPage !== 1"
        class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
        size="24"
        type="mdi"
        :path="mdiChevronLeft"
        @click="
          router.push({
            name: routeName,
            query: { page_index: currentPage - 1 },
          })
        "
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
        v-show="currentPage !== totalPages"
        class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
        size="24"
        type="mdi"
        :path="mdiChevronRight"
        @click="
          router.push({
            name: routeName,
            query: { page_index: currentPage + 1 },
          })
        "
      ></SvgIcon>
    </div>
    <div>
      <SvgIcon
        v-show="currentPage !== totalPages"
        class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
        size="24"
        type="mdi"
        :path="mdiChevronDoubleRight"
        @click="
          router.push({ name: routeName, query: { page_index: totalPages } })
        "
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
import { useRouter } from "vue-router";

const router = useRouter();

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
  pointer-events: none;
}
</style>
