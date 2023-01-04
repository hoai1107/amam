<template>
  <NavigationBar></NavigationBar>
  <div class="w-full h-fit mb-6">
    <div class="w-[1272px] mx-auto">
      <div class="grid grid-cols-12 gap-x-6">
        <div class="col-span-6">
          <PostMetaData></PostMetaData>
          <EditProfileForm></EditProfileForm>
        </div>
        <div class="col-span-6">
          <SectionQuestion></SectionQuestion>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import NavigationBar from "@/components/layout/navbar/NavigationBar.vue";
import EditProfileForm from "@/components/layout/views/UserProfile/EditProfileForm.vue";
import SectionQuestion from "@/components/layout/views/UserProfile/SectionQuestion.vue";
import PostMetaData from "@/components/layout/views/UserProfile/PostMetaData.vue";
import { useRoute } from "vue-router";
import { useUserStore } from "@/stores/user.js";
import { ref } from "vue";

const readOnly = ref(true);
const route = useRoute();
const userStore = useUserStore();

if (route.params.id === userStore.getUserId()) {
  readOnly.value = false;
}
</script>

<style lang="scss" scoped></style>
