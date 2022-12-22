<template>
  <MainContainer>
    <Suspense>
      <QuestionContent endpoint="all" />
    </Suspense>
  </MainContainer>
</template>

<script setup>
import MainContainer from "@/components/layout/MainContainer.vue";
import QuestionContent from "@/components/layout/QuestionContent.vue";
</script>

<style lang="scss" scoped></style>
