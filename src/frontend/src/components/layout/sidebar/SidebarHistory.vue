<template>
  <div class="text-xl font-semibold mb-3">History</div>
  <div v-if="authStore.isAuthenticated()">
    <div class="grid grid-cols-1 divide-y divide-gray-100 divide-solid mb-3">
      <div
        v-for="post in posts"
        v-bind:key="post._id"
        class="py-4 first:pt-0 last:pb-0"
      >
        <router-link
          :to="{ name: 'questions.single', params: { id: post._id } }"
          class="inline-block w-full hover:text-blueSky-dark-300"
          >{{ post.title }}</router-link
        >
      </div>
    </div>
    <!-- <div class="text-blue">See all</div> -->
  </div>
  <div v-else>
    Please <a href="/login" class="text-blueSky-dark-300">login</a> or
    <a href="/sign-up" class="text-blueSky-dark-300">register</a> to see your
    history.
  </div>
</template>

<script setup>
import { useUserStore } from "@/stores/user.js";
import { useAuthStore } from "@/stores/auth.js";
import { watchEffect, ref } from "vue";

const userStore = useUserStore();
const authStore = useAuthStore();
const posts = ref();

watchEffect(() => {
  if (authStore.isAuthenticated()) {
    var tempArr = userStore.user.history_posts.slice();
    posts.value = tempArr.reverse().slice(0, 10);
  }
});
</script>

<style lang="scss" scoped></style>
