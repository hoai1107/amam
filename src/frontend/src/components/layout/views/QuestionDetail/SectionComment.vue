<template>
  <div>
    <!-- Comment Input Form -->
    <div>
      <div class="text-xl font-semibold">Comments ({{ totalComments }})</div>
      <CommentForm />
      <div class="flex flex-col gap-6">
        <CommentItem
          v-for="comment in content"
          :comment="comment"
          v-bind:key="comment._id"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import CommentForm from "@/components/layout/views/QuestionDetail/CommentForm.vue";
import CommentItem from "@/components/layout/views/QuestionDetail/CommentItem.vue";

const props = defineProps(["content"]);

const totalComments = computed(() => {
  var total = props.content.length;
  for (var index in props.content) {
    var comment = props.content[index];
    total += comment.list_child_comment.length;
  }
  return total;
});
</script>

<style lang="scss" scoped></style>
