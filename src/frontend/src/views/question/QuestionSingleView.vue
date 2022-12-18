<template>
  <MainContainer>
    <Suspense>
      <QuestionDetail />
    </Suspense>
  </MainContainer>
</template>

<script setup>
import MainContainer from "@/components/layout/MainContainer.vue";
import QuestionDetail from "@/components/layout/views/QuestionDetail/QuestionDetail.vue";

const props = defineProps({
  id: String,
});
</script>

<style lang="scss" scoped></style>
