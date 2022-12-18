<template>
  <NavigationBar></NavigationBar>
  <div class="w-full h-fit mb-6">
    <div class="w-[1272px] mx-auto">
      <div class="grid grid-cols-12 gap-x-6">
        <div class="col-span-6">
          <div class="flex flex-row">
            <div class="flex flex-col items-center w-1/3">
              <Avatar></Avatar>
              <div class="flex flex-row mt-2">
                <SvgIcon
                  size="24"
                  type="mdi"
                  style="color: blue;"
                  :path="mdiCameraOutline"
                ></SvgIcon>
                <p class="text-blue ml-2">change</p>
              </div>
            </div>
            <div class="flex flex-col ml-2">
              <p class="text-2xl font-semibold">Floyd Miles</p>
              <p class="text-gray-400 mt-1">camlansuc@gmail.com</p>
              <div class="flex flex-row text-blue gap-x-8 mt-2">
                <p>0 following</p>
                <p>0 follower</p>
              </div>
            </div>
          </div>
          <div class="mt-3">
            <p>About me</p>
            <textarea
              class="input-form"
              v-model="question"
              placeholder="Write something..."
              rows="5"
            ></textarea>
            <div class="flex flex-row justify-between mt-2">
              <div class="flex flex-col">
                <p>Location</p>
                <input
                  class="input-form"
                  v-model="name"
                  placeholder="e.g Vietnam"
                />
              </div>
              <div class="flex flex-col">
                <p>Title</p>
                <input
                  class="input-form"
                  v-model="name"
                  placeholder="e.g Student"
                />
              </div>
            </div>
            <ButtonItem
              style="margin-top: 1rem; height: 52px; width: 150px"
              type="primary"
              state="normal"
              text="Save Profile"
            ></ButtonItem>
          </div>
        </div>
        <div class="col-span-6">
          <div class="flex flex-col items-center">
            <div class="flex flex-row my-8">
              <div class="flex flex-col items-center">
                <p class="text-3xl font-semibold">12</p>
                <p class="text-xl text-gray-400">Questions</p>
              </div>
              <div class="flex flex-col items-center ml-20">
                <p class="text-3xl font-semibold">78</p>
                <p class="text-xl text-gray-400">Answers</p>
              </div>
            </div>
          </div>
          <div>
            <p class="text-left text-xl font-semibold">Your Questions</p>
            <p class="text-right text-sm text-blue">See all</p>
          </div>
          <div>
            <p class="text-left text-xl font-semibold">Saved Questions</p>
            <p class="text-right text-sm text-blue">See all</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  id: String,
});
import Avatar from "@/components/ui/Avatar.vue";
import NavigationBar from "@/components/layout/navbar/NavigationBar.vue";
import QuestionCard from "@/components/layout/QuestionCard.vue";
import ButtonItem from "@/components/ui/ButtonItem.vue";

import { mdiCameraOutline } from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";
</script>

<style lang="scss" scoped>
.input-form {
  width: 100%;

  padding: 12px 24px;
  gap: 8px;
  background: #ffffff;
  border: 2px solid #000000;
  border-radius: 8px;

  -moz-appearance: none; /* Firefox */
  -webkit-appearance: none; /* Safari and Chrome */
  appearance: none;
}
</style>
