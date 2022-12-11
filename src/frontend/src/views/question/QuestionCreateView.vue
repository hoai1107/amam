<template>
  <NavigationBar></NavigationBar>
  <div class="w-full h-fit mb-6">
    <div class="w-[1272px] mx-auto">
      <div class="grid grid-cols-12 gap-x-6">
        <div class="col-span-2">
          <SidebarCategory></SidebarCategory>
        </div>

        <div class="col-span-10">
          <div class="text-xl font-semibold mb-3">Ask a question</div>
          <QuestionForm></QuestionForm>
          <p>Tags</p>
          <p class="text-sm text-blueSky-dark-500">
            Select up to 5 tags to describe what your question is about
          </p>

          <div class="grid grid-rows-6 grid-flow-col gap-y-2 pb-9">
            <div v-for="(category, index) in categories" v-bind:key="index">
              <CheckBox :text="category"></CheckBox>
            </div>
          </div>
          <ButtonItem
            style="mt-10; height: 48px; width: 105px"
            type="primary"
            state="normal"
            text="Submit"
          ></ButtonItem>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import SidebarCategory from "@/components/layout/sidebar/SidebarCategory.vue";
import NavigationBar from "@/components/layout/navbar/NavigationBar.vue";
import QuestionForm from "@/components/QuestionForm.vue";
import CheckBox from "@/components/ui/CheckBox.vue";
import ButtonItem from "@/components/ui/ButtonItem.vue";
const categories = [
  "Books",
  "Business",
  "Cooking",
  "Design",
  "Economics",
  "Education",
  "Fashion & Style",
  "Finance",
  "Fine Art",
  "Food",
  "Health",
  "History",
  "Journalism",
  "Literature",
  "Marketing",
  "Mathematics",
  "Movies",
  "Music",
  "Philosophy",
  "Politics",
  "Psychology",
  "Science",
  "Sports",
  "Technology",
  "Travel",
  "Writing",
  "Others",
];
</script>

<style lang="scss" scoped></style>
