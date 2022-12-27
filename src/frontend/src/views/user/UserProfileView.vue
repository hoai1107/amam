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
const props = defineProps({
  id: String,
});

import NavigationBar from "@/components/layout/navbar/NavigationBar.vue";
import EditProfileForm from "@/components/layout/views/UserProfile/EditProfileForm.vue"
import SectionQuestion from "@/components/layout/views/UserProfile/SectionQuestion.vue"
import PostMetaData from "@/components/layout/views/UserProfile/PostMetaData.vue"
</script>

<style lang="scss" scoped>
</style>
