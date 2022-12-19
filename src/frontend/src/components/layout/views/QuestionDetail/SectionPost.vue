<template>
  <div class="flex flex-row items-center">
    <h1 class="text-xl font-semibold pr-4 mr-auto">
      {{ content.title }}
    </h1>
    <SvgIcon size="32" type="mdi" :path="mdiDotsVertical"></SvgIcon>
  </div>
  <!--TODO: Calculate how from last edit-->
  <PostMetaData
    :time-interval="calculateTimeInterval()"
    :views="content.view"
  ></PostMetaData>
  <div class="flex gap-2 mb-4 mt-4">
    <div v-for="(tag, index) in content.tags" :key="index">
      <Tag :name="tag" />
    </div>
  </div>
  <p class="text-base">
    {{ content.content }}
  </p>
  <div class="flex flex-row mt-4 mb-6">
    <div class="flex flex-row gap-8">
      <div class="flex flex-row">
        <div class="mr-2 text-base">{{ content.up_vote }}</div>
        <SvgIcon size="24" type="mdi" :path="mdiArrowUpBoldOutline"></SvgIcon>
      </div>
      <div class="flex flex-row">
        <div class="mr-2 text-base">{{ content.down_vote }}</div>
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
import Tag from "@/components/ui/Tag.vue";
import PostMetaData from "./PostMetaData.vue";
import { DateTime } from "luxon";
import {
  mdiArrowUpBoldOutline,
  mdiArrowDownBoldOutline,
  mdiCommentOutline,
  mdiEyeOutline,
  mdiBookmarkOutline,
  mdiBookmark,
  mdiDotsVertical,
} from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";

const props = defineProps(["content"]);

function calculateTimeInterval() {
  const dateNow = DateTime.now();
  const dateCreated = DateTime.fromISO(props.content.time_created);

  const diff = dateNow
    .diff(dateCreated, ["years", "months", "days", "hours", "minutes"])
    .toObject();

  for (const measurement in diff) {
    const val = Math.floor(diff[measurement]);

    if (val !== 0) {
      return `${val} ${measurement} ago`;
    }
  }

  return "Just a second ago";
}
</script>

<style lang="scss" scoped></style>
