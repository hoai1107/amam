<template>
  <div>
    <p class="px-3 text-left text-xl font-semibold">{{ props.name }}</p>

    <p
      v-for="(question, index) in questions"
      :key="question._id"
      class="text-sm p-3 border-gray-100 border-solid hover:text-blueSky-dark-300 cursor-pointer"
      :class="[index + 1 != 1 ? 'border-t-2' : '']"
      @click="onClick(question._id)"
    >
      {{ question.title }}
    </p>

    <p class="text-right text-sm text-blue cursor-pointer">See all</p>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";

const props = defineProps({
  name: String,
  questions: Array,
});
const router = useRouter();

console.log(props.questions);

function onClick(postId) {
  router.push({ name: "questions.single", params: { id: postId } });
}
</script>

<style lang="scss" scoped></style>
