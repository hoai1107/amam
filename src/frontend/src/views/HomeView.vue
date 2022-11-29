<template>
  <QuestionCard></QuestionCard>
  <div>Home</div>
  <p>{{ name }}</p>
  <ButtonItem
    type="primary"
    state="normal"
    text="Click me!"
    @button-click="helloWorld"
  ></ButtonItem>
  <SortMenu></SortMenu>
  <SearchBar></SearchBar>
  <SignUpForm></SignUpForm>
  <CommentForm></CommentForm>
  <CommentItem></CommentItem>
  <QuestionForm></QuestionForm>
</template>

<script setup>
import { ref } from "vue";
import Tag from "../components/ui/Tag.vue";
import QuestionCard from "../components/layout/QuestionCard.vue";
import ButtonItem from "@/components/ui/ButtonItem.vue";
import SortMenu from "@/components/SortMenu.vue";
import SearchBar from "@/components/layout/navbar/SearchBar.vue";
import SignUpForm from "@/components/SignUpForm.vue";
import CommentForm from "@/components/CommentForm.vue";
import CommentItem from "@/components/CommentItem.vue";
import QuestionForm from "@/components/QuestionForm.vue";
const name = ref("Hello World");

function helloWorld() {
  console.log("Hello World");
}
</script>

<style lang="scss" scoped></style>
