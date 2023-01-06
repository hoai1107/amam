<template>
  <div class="h-full w-full">
    <div class="flex flex-row justify-between h-12 items-center">
      <!--Noti icon-->
      <div class="flex items-center">
        <SvgIcon size="32" type="mdi" :path="mdiBellOutline"></SvgIcon>
      </div>

      <!--Avatar-->
      <div
        class="aspect-square h-full relative cursor-pointer"
        v-click-outside="hideMenu"
      >
        <div
          class="img-container aspect-square h-full flex grow-0 items-center content-center"
        >
          <img
            v-if="userStore.user.avatar"
            :src="userStore.user.avatar"
            alt="avatar"
            @click="toggleMenu"
          />
          <img
            v-else
            src="@/assets/img/user.webp"
            alt="avatar"
            @click="toggleMenu"
          />
        </div>

        <!--Menu-->
        <div
          v-show="showMenu"
          class="text-lg mt-2 border-2 border-solid rounded px-2 py-2 absolute bg-white z-10 shadow-sm"
        >
          <ul class="flex flex-col gap-1">
            <router-link
              :to="{ name: 'user', params: { id: userStore.getUserId() } }"
            >
              <li
                class="rounded flex flex-row gap-2 items-center justify-start px-4 hover:bg-blueSky-light-800"
              >
                <SvgIcon
                  size="24"
                  type="mdi"
                  :path="mdiAccountOutline"
                ></SvgIcon>
                <p>Profile</p>
              </li>
            </router-link>
            <li
              class="rounded flex flex-row gap-2 items-center text-red px-4 hover:bg-blueSky-light-800"
              @click="logout"
            >
              <SvgIcon size="24" type="mdi" :path="mdiLogoutVariant"></SvgIcon>
              <p>Logout</p>
            </li>
          </ul>
        </div>
      </div>

      <!--Button-->
      <div class="h-full">
        <router-link :to="{ name: 'questions.create' }">
          <ButtonItem type="primary" state="normal" text="Create a question" />
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
import { mdiBellOutline, mdiAccountOutline, mdiLogoutVariant } from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";

import { ref } from "vue";
import { useUserStore } from "@/stores/user.js";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const showMenu = ref(false);
const router = useRouter();
const userStore = useUserStore();
const authStore = useAuthStore();

function toggleMenu() {
  showMenu.value = !showMenu.value;
}

function hideMenu() {
  showMenu.value = false;
}

function logout() {
  authStore.logoutUser();
  router.push({ name: "login" });
}
</script>

<style lang="scss" scoped>
.img-container {
  font-size: 0;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  border: 2px solid black;
  border-radius: theme("borderRadius.DEFAULT");
}
</style>
