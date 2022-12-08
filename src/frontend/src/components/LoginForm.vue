<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
import CheckBox from "@/components/ui/CheckBox.vue"
const props = defineProps({
  wrong: { type: Boolean, default: true },
});
</script>

<template>
  <div class="container flex flex-col">
    <div class="input-container flex flex-col content-stretch">
      <p>Email</p>
      <input type="email" class="input-form" v-model="email" />
    </div>
    <div class="input-container flex flex-col content-stretch">
      <p>Password</p>
      <input type="password" class="input-form" v-model="password" />
    </div>
    <CheckBox text="Remember me"></CheckBox>
    <p class="warning" v-if="false">Wrong account or password</p>
    <p class="warning" v-if="false">Your email hasn't verified yet!</p>
    <p class="warning" style="color: var(--blue)" v-if="false">
      Please verify email before logging in
    </p>
    <ButtonItem
      style="margin-top: 10px"
      type="primary"
      state="normal"
      text="Login"
    ></ButtonItem>
  </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.container {
  @extend .base-400;
}

.input-container {
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

.warning {
  font-size: 14px;
  color: var(--red);
}
</style>
