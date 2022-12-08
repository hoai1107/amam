<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
</script>

<template>
  <div class="container">
    <div class="input-container">
      <p>Title</p>
      <p class="text-sm text-blueSky-dark-500">
        Be specific about what you want to ask (maximum 100 characters)
      </p>
      <input
        class="input-form"
        v-model="name"
        placeholder="Write something..."
      />
    </div>
    <div class="input-container">
      <p>Can you tell us more detail about what you want to ask?</p>
      <textarea
        class="input-form"
        v-model="question"
        placeholder="Write something..."
        rows="5"
      ></textarea>
    </div>
  </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.container {
  box-sizing: border-box;
  @extend .base-400;
}

.input-container {
  padding-bottom: 12px;
}

.input-form {
  width: 1056px;

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
