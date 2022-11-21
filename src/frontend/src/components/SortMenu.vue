<script setup>
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiChevronDown } from "@mdi/js";
</script>

<template>
  <div class="dropdown-container">
    <select
      class="dropdown-form rounded border-2 border-solid border-black"
      key=""
      v-model="selected"
      label="Sort by"
    >
      <option selected disabled value="undefined">Sort by</option>
      <option>Most vote</option>
      <option>Most answer</option>
      <option>Most view</option>
    </select>
    <div class="dropdown-icon">
      <svg-icon type="mdi" :path="mdiChevronDown"></svg-icon>
    </div>
  </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.dropdown-container {
  box-sizing: border-box;

  display: flex;
  flex-direction: row;
  align-items: flex-start;
  position: relative;

  flex: none;
  order: 2;
  align-self: stretch;
  flex-grow: 0;

  @extend .base-400;
}

.dropdown-form {
  padding: 12px 24px;
  width: 200px;

  background: theme("colors.white");

  -moz-appearance: none; /* Firefox */
  -webkit-appearance: none; /* Safari and Chrome */
  appearance: none;
}

.dropdown-icon {
  margin-left: -48px;
  padding-top: 14px;
  pointer-events: none;
}
</style>
