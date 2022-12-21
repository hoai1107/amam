<template>
  <div class="container flex flex-col text-base">
    <div class="input-container">
      <p>Name</p>
      <input class="input-form" v-model="name" />
    </div>
    <div class="input-container">
      <p>Email</p>
      <input type="email" class="input-form" v-model="email" />
    </div>
    <div class="input-container">
      <p>Password</p>
      <input type="password" class="input-form" v-model="password" />
    </div>
    <ButtonItem
      class="mt-3"
      type="primary"
      state="normal"
      text="Sign up"
      @click="signUp"
    ></ButtonItem>
  </div>
</template>

<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();
const name = ref();
const email = ref();
const password = ref();

async function signUp() {
  await authStore.registerUser(name.value, email.value, password.value);
}
</script>

<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.container {
  // display: flex;
  // flex-direction: column;
  // box-sizing: border-box;
  // @extend .base-400;
  gap: 12px;
}

.input-container {
  display: flex;
  flex-direction: column;
  align-content: stretch;
  // margin-bottom: 12px;
}

.input-form {
  width: 100%;
  padding: 12px 24px;
  margin-top: 4px;
  // gap: 8px;
  background: #ffffff;
  border: 2px solid #000000;
  border-radius: 8px;

  -moz-appearance: none; /* Firefox */
  -webkit-appearance: none; /* Safari and Chrome */
  appearance: none;
}
</style>
