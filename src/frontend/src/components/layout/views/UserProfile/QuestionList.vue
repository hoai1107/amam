<template>
  <div>
    <p class="px-3 text-left text-xl font-semibold">{{ props.name }}</p>

    <p
      v-for="(question, index) in currentQuestionList"
      :key="question._id"
      class="text-sm p-3 border-gray-100 border-solid hover:text-blueSky-dark-300 cursor-pointer"
      :class="[index + 1 != 1 ? 'border-t-2' : '']"
      @click="onClick(question._id)"
    >
      {{ question.title }}
    </p>

    <div class="w-full">
      <div class="flex flex-row gap-12 w-fit mx-auto">
        <SvgIcon
          class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
          :class="[page === 0 ? 'pointer-events-none text-gray-400' : '']"
          size="24"
          type="mdi"
          :path="mdiChevronLeft"
          @click="page--"
        ></SvgIcon>
        <SvgIcon
          class="cursor-pointer hover:text-blueSky-dark-300 transition-none"
          :class="[
            page === maxPage - 1 ? 'pointer-events-none text-gray-400' : '',
          ]"
          size="24"
          type="mdi"
          :path="mdiChevronRight"
          @click="page++"
        ></SvgIcon>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { mdiChevronLeft, mdiChevronRight } from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";
import { ref, watchEffect } from "vue";

const props = defineProps({
  name: String,
  questions: Array,
});

const ITEMS_PER_PAGE = 5;
const maxPage = Math.ceil(props.questions.length / 5);

const router = useRouter();
const page = ref(0);
const currentQuestionList = ref();

watchEffect(() => {
  currentQuestionList.value = props.questions.slice(
    ITEMS_PER_PAGE * page.value,
    ITEMS_PER_PAGE * (page.value + 1)
  );
});

function onClick(postId) {
  router.push({ name: "questions.single", params: { id: postId } });
}
</script>

<style lang="scss" scoped></style>
