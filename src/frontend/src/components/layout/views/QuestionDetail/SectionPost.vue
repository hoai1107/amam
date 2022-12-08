<template>
  <div class="flex flex-row items-center ">
    <h1 class="text-xl font-semibold pr-4 mr-auto">Where should I store my CSV files for Memgraph?</h1>
    <SvgIcon size="32" type="mdi" :path="mdiDotsVertical"></SvgIcon>
  </div>
  <PostMetaData :hours-from-last-edit="2" :views="15"></PostMetaData>
  <div class="flex gap-2 mb-4 mt-4">
    <Tag></Tag>
    <Tag></Tag>
  </div>
  <p class="text-base">
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Veritatis perferendis et totam cupiditate magni! Aliquid consequuntur expedita reiciendis quidem ab! Sed delectus alias repudiandae excepturi? Molestias quasi reiciendis laboriosam qui commodi facilis quidem ab id vel iusto corporis autem ullam non velit quisquam pariatur, quae unde explicabo odio ipsum modi.
  </p>
  <div class="flex flex-row mt-4 mb-6">
      <div class="flex flex-row gap-8">
        <div class="flex flex-row">
          <div class="mr-2 text-base">5</div>
          <SvgIcon size="24" type="mdi" :path="mdiArrowUpBoldOutline"></SvgIcon>
        </div>
        <div class="flex flex-row">
          <div class="mr-2 text-base">5</div>
          <SvgIcon size="24" type="mdi" :path="mdiArrowDownBoldOutline"></SvgIcon>
        </div>
      </div>

      <!-- bookmark icon, bien mat doi voi anonymous, khi click se chuyen qua icon mdiBookmark co color blue (xem design system) -->
      <SvgIcon
        size="24"
        type="mdi"
        :path="mdiBookmarkOutline"
        class="ml-auto"
      ></SvgIcon>
    </div>
</template>

<script setup>
import Tag from '@/components/ui/Tag.vue';
import PostMetaData from './PostMetaData.vue';
import {
  mdiArrowUpBoldOutline,
  mdiArrowDownBoldOutline,
  mdiCommentOutline,
  mdiEyeOutline,
  mdiBookmarkOutline,
  mdiBookmark,
  mdiDotsVertical
} from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";
</script>

<style lang="scss" scoped></style>
