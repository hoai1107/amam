<template>
  <NavigationBar></NavigationBar>
  <div class="w-full h-fit mb-6">
    <div class="w-[1272px] mx-auto">
      <div class="grid grid-cols-12 gap-x-6">
        <div class="col-span-12">
          <div class="text-center text-xl font-semibold mb-3">All categories</div>
          <div class="grid grid-cols-4 grid-flow-row gap-y-2 gap-x-2 pb-9">
            <ButtonItem
            v-for="(category, index) in categories" v-bind:key="index"
            :text="category"
            style="height: 120px"
            :class= "[Math.floor(index/4) % 2 === 0 ? 'bg-blueSky-light-800 hover:bg-blueSky' : 'bg-yellow-light-800 hover:bg-yellow']"
            state="normal"
            ></ButtonItem>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  category: String,
});
import SidebarCategory from "@/components/layout/sidebar/SidebarCategory.vue";
import NavigationBar from "@/components/layout/navbar/NavigationBar.vue";
import QuestionForm from "@/components/layout/views/QuestionCreate/QuestionForm.vue";
import CheckBox from "@/components/ui/CheckBox.vue";
import ButtonItem from "@/components/ui/ButtonItem.vue";
const categories = [
  "All",
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
