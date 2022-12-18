<template>
  <SectionPost :content="content" />
  <SectionComment :content="content" />
</template>

<script setup>
import SectionComment from "./SectionComment.vue";
import SectionPost from "./SectionPost.vue";
import Constansts from "@/plugins/Constants.js";
import axios from "axios";
import { useRoute } from "vue-router";
import { ref } from "vue";

const route = useRoute();
const content = ref();

const response = await axios.get(
  Constansts.BACKEND_URL + `posts/${route.params.id}`
);
content.value = response.data;

console.log(response);
</script>

<style lang="scss" scoped></style>
