<script setup>
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiMagnify } from "@mdi/js";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const searchText = ref("");

function searchQuestion() {
  router.push({
    name: "questions.search",
    query: {
      query_title: searchText.value,
    },
  });
}
</script>

<template>
  <div
    class="container relative flex flex-row items-start text-base font-normal"
  >
    <input
      class="search-bar w-full shadow-sm bg-white rounded border-2 border-black"
      v-model="searchText"
      @keyup.enter="searchQuestion"
      placeholder="Search a question"
    />
    <button type="submit" @click="searchQuestion">
      <div class="dropdown-icon">
        <svg-icon type="mdi" :path="mdiMagnify"></svg-icon>
      </div>
    </button>
  </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.search-bar {
  padding: 10px 48px 10px 24px;

  -moz-appearance: none; /* Firefox */
  -webkit-appearance: none; /* Safari and Chrome */
  appearance: none;
}

input:focus {
  outline: none;
}

.dropdown-icon {
  position: relative;
  padding: 14px 0px;
  margin-left: -48px;
}
</style>
