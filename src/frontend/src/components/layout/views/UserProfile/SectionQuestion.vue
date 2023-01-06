<template>
  <div class="flex flex-col items-center">
    <div class="flex flex-row my-8">
      <div class="flex flex-col items-center">
        <p class="text-3xl font-semibold">12</p>
        <p class="text-xl text-gray-400">Questions</p>
      </div>
      <div class="flex flex-col items-center ml-20">
        <p class="text-3xl font-semibold">78</p>
        <p class="text-xl text-gray-400">Answers</p>
      </div>
    </div>
  </div>
  <QuestionList
    :questions="userStore.getQuestionList()"
    name="Your Questions"
  ></QuestionList>
  <QuestionList
    :questions="userStore.getBookmarkList()"
    class="mt-8"
    name="Saved Questions"
  ></QuestionList>
</template>

<script setup>
import QuestionList from "@/components/layout/views/UserProfile/QuestionList.vue";
import { useUserStore } from "@/stores/user";

const props = defineProps({
  name: String,
});

const userStore = useUserStore();
</script>

<style lang="scss" scoped></style>
