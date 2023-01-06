<template>
  <div
    class="questionCard cursor-pointer border-2 border-solid border-black hover:shadow-md rounded bg-blueSky-light-800 py-4 px-6"
  >
    <p class="text-lg font-semibold text-blueSky-dark-800">
      {{ question.title }}
    </p>
    <div class="flex gap-2 mt-2 mb-4">
      <div v-for="(tag, index) in question.tags" :key="index">
        <Tag :name="capitalize(tag)" />
      </div>
    </div>
    <p class="text-base mb-4 truncate">
      {{ question.content }}
    </p>
    <div class="flex flex-row">
      <div class="flex flex-row gap-8">
        <div class="flex flex-row">
          <div class="mr-2 text-base">
            {{ question.upvote + question.downvote }}
          </div>
          <SvgIcon size="24" type="mdi" :path="mdiArrowUpBoldOutline"></SvgIcon>
        </div>
        <div class="flex flex-row">
          <div class="mr-2 text-base">{{ question.num_comments }}</div>
          <SvgIcon size="24" type="mdi" :path="mdiCommentOutline"></SvgIcon>
        </div>
        <div class="flex flex-row">
          <div class="mr-2 text-base">{{ question.view }}</div>
          <SvgIcon size="24" type="mdi" :path="mdiEyeOutline"></SvgIcon>
        </div>
      </div>

      <!-- bookmark icon, bien mat doi voi anonymous, khi click se chuyen qua icon mdiBookmark co color blue (xem design system) -->
      <SvgIcon
        size="24"
        type="mdi"
        :path="
          userStore.checkPostBookmark(question._id)
            ? mdiBookmark
            : mdiBookmarkOutline
        "
        class="ml-auto"
      ></SvgIcon>
    </div>
  </div>
</template>

<script setup>
import Tag from "../ui/Tag.vue";
import {
  mdiArrowUpBoldOutline,
  mdiCommentOutline,
  mdiEyeOutline,
  mdiBookmarkOutline,
  mdiBookmark,
} from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";
import { useUserStore } from "@/stores/user.js";

const props = defineProps(["question"]);
const userStore = useUserStore();

console.log(props.question);

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
</script>

<style lang="scss" scoped>
.questionCard {
  transition: all 0.3s;
}
.questionCard:hover {
  transform: translate(-4px, -4px);
}
</style>
