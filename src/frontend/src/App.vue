<script setup>
import { ref } from "vue";
import ButtonItem from "@/components/ButtonItem.vue";
import SortMenu from "@/components/SortMenu.vue";
import SearchBar from "@/components/SearchBar.vue";
import SignUpForm from "@/components/SignUpForm.vue";
import CommentForm from "@/components/CommentForm.vue";
import CommentItem from "@/components/CommentItem.vue";
import QuestionForm from "@/components/QuestionForm.vue";
import LoginForm from "@/components/LoginForm.vue";
const name = ref("Hello World");
</script>

<template>
  <p>{{ name }}</p>
  <ButtonItem type="primary" state="normal"></ButtonItem>
  <SortMenu></SortMenu>
  <SearchBar></SearchBar>
  <SignUpForm></SignUpForm>
  <CommentForm></CommentForm>
  <CommentItem></CommentItem>
  <QuestionForm></QuestionForm>
  <LoginForm></LoginForm>
</template>

<script setup></script>

<style lang="scss" scoped></style>
