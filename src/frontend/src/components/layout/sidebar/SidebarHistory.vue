<template>
  <div class="text-xl font-semibold mb-3">History</div>
  <div class="grid grid-cols-1 divide-y divide-gray-100 divide-solid mb-3">
    <div
      v-for="post in historyPosts"
      v-bind:key="post.id"
      class="py-4 first:pt-0 last:pb-0"
    >
      <router-link
        :to="{ name: 'questions.single', params: { id: post.id } }"
        class="inline-block w-full hover:text-blueSky-dark-300"
        >{{ post.title }}</router-link
      >
    </div>
  </div>
  <div class="text-blue">See all</div>
</template>

<script setup>
const historyPosts = [
  { id: 1, title: "How does AWS work?" },
  { id: 2, title: "Is Java better than C++?" },
  { id: 3, title: "How much time to learn a programming language?" },
];
</script>

<style lang="scss" scoped></style>
