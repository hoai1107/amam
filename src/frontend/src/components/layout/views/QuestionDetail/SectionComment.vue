<template>
  <div>
    <!-- Comment Input Form -->
    <div>
      <div class="text-xl font-semibold">Comments ({{ totalComments }})</div>
      <CommentForm @submit-comment="submitComment" />
      <div class="flex flex-col gap-6">
        <CommentItem
          v-for="comment in content"
          :comment="comment"
          :can-reply="true"
          @submit-reply="submitReply"
          v-bind:key="comment._id"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth.js";
import CommentForm from "@/components/layout/views/QuestionDetail/CommentForm.vue";
import CommentItem from "@/components/layout/views/QuestionDetail/CommentItem.vue";
import { useRoute } from "vue-router";

const props = defineProps(["content"]);
const emit = defineEmits(["fetch-data"]);
const authStore = useAuthStore();
const route = useRoute();

const postId = route.params.id;
const instance = authStore.getAxiosInstance();

const totalComments = computed(() => {
  var total = props.content.length;
  for (var index in props.content) {
    var comment = props.content[index];
    total += comment.list_child_comment.length;
  }
  return total;
});

function submitComment(content) {
  instance
    .post("users/comments/create", {
      post_id: postId,
      content: content,
    })
    .then(() => {
      emit("fetch-data");
    });
}

function submitReply(content, parentId) {
  instance
    .post(
      "users/comments/reply",
      {
        post_id: postId,
        content: content,
      },
      { params: { parentCommentID: parentId } }
    )
    .then(() => {
      emit("fetch-data");
    });
}
</script>

<style lang="scss" scoped></style>
