<template>
  <div>
    <!-- Comment Input Form -->
    <div>
      <div class="text-xl font-semibold">Comments ({{ totalComments }})</div>
      <CommentForm />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import CommentForm from "@/components/layout/views/QuestionDetail/CommentForm.vue";

const totalComments = ref(3);
</script>

<style lang="scss" scoped></style>
