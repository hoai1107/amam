<script setup>
import ButtonItem from "@/components/ButtonItem.vue";
</script>

<template>
  <div class="container">
    <div class="input-container">
      <p>Name</p>
      <input class="input-form" v-model="name" />
    </div>
    <div class="input-container">
      <p>Email</p>
      <input type="email" class="input-form" v-model="email" />
    </div>
    <div class="input-container">
      <p>Password</p>
      <input type="password" class="input-form" v-model="password" />
    </div>
    <ButtonItem
      style="margin-top: 10px"
      type="primary"
      state="normal"
    ></ButtonItem>
  </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.container {
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  @extend .base-400;
}

.input-container {
  display: flex;
  flex-direction: column;
  align-content: stretch;
  margin-bottom: 12px;
}

.input-form {
  padding: 12px 24px;
  gap: 8px;
  background: #ffffff;
  border: 2px solid #000000;
  border-radius: 8px;

  -moz-appearance: none; /* Firefox */
  -webkit-appearance: none; /* Safari and Chrome */
  appearance: none;
}

.button-container {
  padding-top: 12px;
}
</style>
