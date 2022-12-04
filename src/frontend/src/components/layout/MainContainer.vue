<template>
  <NavigationBar></NavigationBar>
  <div class="w-full h-fit mb-6">
    <div class="w-[1272px] mx-auto">
      <div class="grid grid-cols-12 gap-x-6">
        <div class="col-span-2">
          <SidebarCategory></SidebarCategory>
        </div>

        <div class="col-span-7">
          <slot>
            <div class="text-xl font-semibold mb-3">All Questions</div>
            <div class="flex flex-col gap-y-6">
              <QuestionCard />
              <QuestionCard />
              <QuestionCard />
              <QuestionCard />
            </div>
          </slot>
          <Pagination :current-page="10" :total-pages="10" />
        </div>

        <div class="col-span-3">
          <SidebarHistory></SidebarHistory>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import QuestionCard from "@/components/layout/QuestionCard.vue";
import SidebarCategory from "@/components/layout/sidebar/SidebarCategory.vue";
import SidebarHistory from "@/components/layout/sidebar/SidebarHistory.vue";
import Pagination from "@/components/layout/pagination/Pagination.vue";
import NavigationBar from "@/components/layout/navbar/NavigationBar.vue";
</script>

<style lang="scss" scoped></style>
