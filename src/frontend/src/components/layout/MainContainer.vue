<template>
  <div class="w-full h-fit">
    <div class="w-[1272px] mx-auto">
      <div class="grid grid-cols-12 gap-x-6">
        <div class="col-span-2">
          <div class="text-xl font-semibold mb-3">Categories</div>
          <div class="flex flex-col gap-y-2 mb-3">
            <div v-for="(category, index) in categories" v-bind:key="index">
              <router-link
                :to="{
                  name: 'questions.category',
                  params: { category: category.toLowerCase() },
                }"
                >{{ category }}</router-link
              >
            </div>
          </div>
          <div class="text-blue">See all</div>
        </div>

        <div class="col-span-7 border border-solid">Content</div>

        <div class="col-span-3 border border-solid">Side bar 2</div>
      </div>
    </div>
  </div>
</template>

<script setup>
const categories = [
  "Technology",
  "Movies",
  "Health",
  "Food",
  "Music",
  "Books",
  "Business",
  "Psychology",
  "History",
  "Cooking",
];
</script>

<style lang="scss" scoped></style>
