<template>
  <div>
    <PulseLoader :loading="isFetching" color="#467980" size="20px" />
  </div>
  <div v-if="!isFetching">
    <SectionPost :content="post_section" />
    <SectionComment :content="comment_section" @fetch-data="fetchData" />
  </div>
</template>

<script setup>
import SectionComment from "./SectionComment.vue";
import SectionPost from "./SectionPost.vue";
import Constansts from "@/plugins/Constants.js";
import axios from "axios";
import { useRoute } from "vue-router";
import { ref } from "vue";
import PulseLoader from "vue-spinner/src/PulseLoader.vue";

const route = useRoute();
const content = ref();
const isFetching = ref(true);
const post_section = ref();
const comment_section = ref();

async function fetchData() {
  isFetching.value = true;
  axios
    .get(Constansts.BACKEND_URL + `posts/${route.params.id}`)
    .then((response) => {
      content.value = response.data;
      post_section.value = content.value["Post Section"];
      comment_section.value = content.value["Comment Section"];
    })
    .then(() => {
      isFetching.value = false;
    });
}

fetchData();
</script>

<style lang="scss" scoped></style>
