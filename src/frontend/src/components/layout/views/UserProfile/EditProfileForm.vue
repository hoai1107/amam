<template>
  <div class="mt-3">
    <p>About me</p>
    <textarea
      class="input-form"
      v-model="aboutMe"
      placeholder="Write something..."
      rows="5"
    ></textarea>
    <div class="flex flex-row justify-between mt-2">
      <div class="flex flex-col w-1/2">
        <p>Location</p>
        <input
          class="input-form"
          v-model="location"
          placeholder="e.g Vietnam"
        />
      </div>
      <div class="flex flex-col w-1/2 ml-4">
        <p>Title</p>
        <input class="input-form" v-model="title" placeholder="e.g Student" />
      </div>
    </div>
    <ButtonItem
      @click="updateProfile"
      style="margin-top: 1rem; height: 52px; width: 150px"
      type="primary"
      state="normal"
      text="Save Profile"
    ></ButtonItem>
  </div>
</template>

<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useUserStore } from "@/stores/user";

const authStore = useAuthStore();
const userStore = useUserStore();

const aboutMe = ref(userStore.user.about_me);
const location = ref(userStore.user.location);
const title = ref(userStore.user.title);

console.log(userStore.user);

function updateProfile() {
  userStore.updateUserProfile({
    about_me: aboutMe.value,
    location: location.value,
    title: title.value,
  });
}
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
