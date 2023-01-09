<template>
  <div>
    <div class="text-xl font-semibold mb-3">{{ result_heading }}</div>
    <div class="w-fit border-2 border-solid rounded px-6 py-3 mb-6">
      <select v-model="orderBy">
        <option
          v-for="option in orderOptions"
          :value="option.value"
          :key="option.value"
        >
          {{ option.text }}
        </option>
      </select>
    </div>
    <div class="flex flex-col gap-y-6">
      <div v-if="questions.data && questions.data.length === 0">
        Opps! Nothing here ¯\_(ツ)_/¯
      </div>
      <div v-else v-for="question in questions.data" :key="question._id">
        <router-link
          :to="{ name: 'questions.single', params: { id: question._id } }"
        >
          <QuestionCard :question="question" />
        </router-link>
      </div>
    </div>
    <Pagination
      :total-pages="Math.max(totalPages, 1)"
      :current-page="Math.max(page, 1)"
      :route-name="route.name"
    />
  </div>
</template>

<script setup>
import QuestionCard from "@/components/layout/QuestionCard.vue";
import Constants from "@/plugins/Constants.js";
import Pagination from "@/components/layout/pagination/Pagination.vue";
import { useRoute } from "vue-router";
import { ref, computed, watchEffect } from "vue";
import voca from "voca";

import axios from "axios";
const instance = axios.create({
  baseURL: Constants.BACKEND_URL + "posts",
});

const props = defineProps({
  endpoint: String,
});

const route = useRoute();
const questions = ref([]);

const orderOptions = ref([
  { text: "Newest", value: "default" },
  { text: "Most Comment", value: "comment" },
  { text: "Most View", value: "view" },
  { text: "Most Voted", value: "vote" },
]);
const orderBy = ref("default");

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
      if (route.query.category) {
        var category = voca
          .split(route.query.category, " ")
          .map((item) => voca.capitalize(item));
        result = category.join(" ");
      }
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
      order_by_option: orderBy.value,
    },
  });
  questions.value = questionsResponse.data;
});
</script>

<style lang="scss" scoped>
select:focus {
  outline: none;
}
</style>
