<template>
  <div class="text-xl font-semibold mb-3">All Questions</div>
  <div class="flex flex-col gap-y-6"></div>
</template>

<script setup>
import QuestionCard from "@/components/layout/QuestionCard.vue";
import Constansts from "@/plugins/Constants.js";
import { ref } from "vue";

import axios from "axios";
const instance = axios.create({
  baseURL: Constansts.BACKEND_URL + "posts",
});

const questions = ref([]);
const questionsResponse = await instance.get("/all");
console.log(questionsResponse.data);
</script>

<style lang="scss" scoped></style>
