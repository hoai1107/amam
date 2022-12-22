<template>
  <NavigationBar></NavigationBar>
  <div class="w-full h-fit mb-6">
    <div class="w-[1272px] mx-auto">
      <div class="grid grid-cols-12 gap-x-6">
        <div class="col-span-2">
          <SidebarCategory></SidebarCategory>
        </div>

        <div class="col-span-10">
          <div class="text-xl font-semibold mb-3">Ask a question</div>
          <QuestionForm></QuestionForm>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import SidebarCategory from "@/components/layout/sidebar/SidebarCategory.vue";
import NavigationBar from "@/components/layout/navbar/NavigationBar.vue";
import QuestionForm from "./QuestionForm.vue";
</script>

<style lang="scss" scoped></style>
