<template>
  <div class="flex flex-row">
    <div class="flex flex-col items-center w-1/3">
      <Avatar :image-src="avatar"></Avatar>
      <label>
        <div class="flex flex-row mt-2">
          <SvgIcon
            size="24"
            type="mdi"
            style="color: blue"
            :path="mdiCameraOutline"
          ></SvgIcon>
          <p class="text-blue ml-2">change</p>
          <input
            @change="previewAvatar"
            type="file"
            id="avatar"
            name="avatar"
            accept="image/png, image/jpeg"
          />
        </div>
      </label>
    </div>
    <div class="flex flex-col ml-4">
      <p class="text-2xl font-semibold">Floyd Miles</p>
      <p class="text-gray-400 mt-1">camlansuc@gmail.com</p>
      <div class="flex flex-row text-blue gap-x-8 mt-2">
        <p>0 following</p>
        <p>0 follower</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import Avatar from "@/components/ui/Avatar.vue";
import { mdiCameraOutline } from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";
import { ref } from "vue";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
const avatar = ref(userStore.user.avatar);

async function previewAvatar() {
  const imageFile = document.querySelector("input[type=file]").files[0];
  const reader = new FileReader();

  var rawImg;
  reader.onloadend = () => {
    rawImg = reader.result;
    avatar.value = rawImg;
    userStore.updateUserProfile({ avatar: rawImg });
  };
  reader.readAsDataURL(imageFile);
}
</script>

<style lang="scss" scoped>
input[type="file"] {
  display: none;
}
</style>
