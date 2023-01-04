<template>
  <form @submit.prevent="submitQuestion">
    <div class="container">
      <div class="py-6">
        <p>Title</p>
        <p class="text-sm text-blueSky-dark-500">
          Be specific about what you want to ask (maximum 100 characters)
        </p>
        <input
          type="text"
          class="input-form"
          v-model="title"
          placeholder="Write something..."
        />
      </div>
      <div class="pb-6">
        <p>Can you tell us more detail about what you want to ask?</p>
        <textarea
          class="input-form"
          v-model="content"
          placeholder="Write something..."
          rows="5"
        ></textarea>
      </div>
      <p class="mb-2">Tags</p>
      <p class="text-sm text-blueSky-dark-500 mb-2">
        Select up to 5 tags to describe what your question is about
      </p>
      <div class="grid grid-rows-6 grid-flow-col gap-y-2 pb-9">
        <!-- TODO: Implement this with CheckBox component -->
        <div v-for="(category, index) in categoriesNames" v-bind:key="index">
          <div class="flex flex-row items-center">
            <div class="tick-box flex flex-row items-center justify-center">
              <input
                type="checkbox"
                class="input-checkbox items-center"
                :id="category"
                :value="category"
                v-model="categories"
              />
              <span class="flex tick-icon">
                <svg-icon type="mdi" :path="mdiCheckBold" size="10"></svg-icon>
              </span>
            </div>
            <label :for="category">{{ category }}</label>
          </div>
        </div>
      </div>
      <ButtonItem
        style="mt-10; height: 48px; width: 105px"
        type="primary"
        state="normal"
        text="Submit"
      ></ButtonItem>
    </div>
  </form>
</template>

<script setup>
import Constants from "@/plugins/Constants";
import ButtonItem from "@/components/ui/ButtonItem.vue";
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiCheckBold } from "@mdi/js";
import axios from "axios";

import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const categoriesNames = Constants.CATEGORIES;

const title = ref();
const content = ref();
const categories = ref([]);
const authStore = useAuthStore();
const router = useRouter();

function submitQuestion() {
  const instance = axios.create({
    baseURL: Constants.BACKEND_URL + "posts",
  });

  let config = authStore.getAuthHeader();

  instance
    .post(
      "/create",
      {
        title: title.value,
        content: content.value,
        tags: categories.value,
      },
      config
    )
    .then(() => {
      router.push({ name: "home" });
    });
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.container {
  box-sizing: border-box;
  @extend .base-400;
}
.input-form {
  width: 1056px;

  padding: 12px 24px;
  gap: 8px;
  background: #ffffff;
  border: 2px solid #000000;
  border-radius: 8px;

  -moz-appearance: none; /* Firefox */
  -webkit-appearance: none; /* Safari and Chrome */
  appearance: none;
}

.tick-box input[type="checkbox"]:checked ~ .tick-icon {
  opacity: 1;
}

.input-checkbox {
  cursor: pointer;
  opacity: 0;
  z-index: 1;
}
.tick-icon {
  position: absolute;
  opacity: 0;
}

.tick-box {
  width: 14px;
  height: 14px;

  background: #ffffff;
  border: 2px solid #000000;
  border-radius: 2px;
  margin-right: 8px;
}
</style>
