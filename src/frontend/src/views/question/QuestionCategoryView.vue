<template>
  <NavigationBar></NavigationBar>
  <div class="w-full h-fit mb-6">
    <div class="w-[1272px] mx-auto">
      <div class="grid grid-cols-12 gap-x-6">
        <div class="col-span-12">
          <div class="text-center text-xl font-semibold mb-3">
            All categories
          </div>
          <div class="grid grid-cols-4 grid-flow-row gap-y-2 gap-x-2 pb-9">
            <ButtonItem
              v-for="(category, index) in categories"
              v-bind:key="index"
              :text="category"
              style="height: 120px"
              :class="[
                Math.floor(index / 4) % 2 === 0
                  ? 'bg-blueSky-light-800 hover:bg-blueSky'
                  : 'bg-yellow-light-800 hover:bg-yellow',
              ]"
              state="normal"
              @click="
                router.push({
                  name: 'questions.category',
                  params: { category: category },
                })
              "
            ></ButtonItem>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Constants from "@/plugins/Constants.js";
import NavigationBar from "@/components/layout/navbar/NavigationBar.vue";
import ButtonItem from "@/components/ui/ButtonItem.vue";
import { useRouter } from "vue-router";

const categories = Constants.CATEGORIES;
const router = useRouter();
</script>

<style lang="scss" scoped></style>
