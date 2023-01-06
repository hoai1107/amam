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
    <p class="warning text-red" v-show="errorMessage !== ''">
      {{ errorMessage }}
    </p>
    <ButtonItem
      class="mt-3"
      type="primary"
      state="normal"
      text="Sign up"
      @click="signUp"
    ></ButtonItem>
    <PulseLoader
      :loading="isSignup"
      class="mt-4 mx-auto"
      color="#467980"
      size="15px"
    />
  </div>
</template>

<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";
import PulseLoader from "vue-spinner/src/PulseLoader.vue";

const authStore = useAuthStore();
const router = useRouter();
const name = ref();
const email = ref();
const password = ref();
const errorMessage = ref("");
const isSignup = ref(false);

async function signUp() {
  isSignup.value = true;
  const response = await authStore.registerUser(
    name.value,
    email.value,
    password.value
  );

  console.log(response);
  if (response.status === 200) {
    router.push({ name: "login", query: { msg: "afterSignup" } });
  } else {
    errorMessage.value = "Sign up failed.";
    isSignup.value = false;
  }
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
