<template>
  <div>
    <div class="text-xl font-semibold mb-3">{{ result_heading }}</div>
    <div class="flex flex-col gap-y-6">
      <div v-for="question in questions.data" :key="question._id">
        <router-link
          :to="{ name: 'questions.single', params: { id: question._id } }"
        >
          <QuestionCard :question="question" />
        </router-link>
      </div>
    </div>
    <Pagination
      :total-pages="totalPages"
      :current-page="page"
      :route-name="route.name"
    />
  </div>
</template>

<script setup>
import QuestionCard from "@/components/layout/QuestionCard.vue";
import Constansts from "@/plugins/Constants.js";
import Pagination from "@/components/layout/pagination/Pagination.vue";
import { useRoute } from "vue-router";
import { ref, computed, watchEffect } from "vue";

import axios from "axios";
const instance = axios.create({
  baseURL: Constansts.BACKEND_URL + "posts",
});

const props = defineProps({
  endpoint: String,
});

const route = useRoute();
const questions = ref([]);

console.log(route.params);

const page = computed(() => {
  return route.query.page_index ? Number(route.query.page_index) : 1;
});

const totalPages = computed(() => {
  return questions.value.total % 7 === 0
    ? questions.value.total / 7
    : Math.floor(questions.value.total / 7) + 1;
});

const result_heading = computed(() => {
  const name = route.name;
  var result = "";

  switch (name) {
    case "home":
      result = "All Questions";
      break;
    case "questions.search":
      result = `Results for "${route.query.query_title}"`;
      break;
    default:
      result = "Hi";
      break;
  }

  return result;
});

watchEffect(async () => {
  const questionsResponse = await instance.get(props.endpoint, {
    params: {
      ...route.query,
      ...route.params,
      page_index: page.value,
    },
  });
  questions.value = questionsResponse.data;
});
</script>

<style lang="scss" scoped></style>
