<script setup>
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiMagnify } from "@mdi/js";
</script>

<template>
  <div
    class="container relative flex flex-row items-start text-base font-normal"
  >
    <input
      class="search-bar w-full shadow-sm bg-white rounded border-2 border-black"
      v-model="message"
      placeholder="Search a question"
    />
    <div class="dropdown-icon">
      <svg-icon type="mdi" :path="mdiMagnify"></svg-icon>
    </div>
  </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.container {
  // position: relative;

  // flex: none;
  // order: 2;
  // align-self: stretch;
  // flex-grow: 0;
}

.search-bar {
  padding: 12px 48px 12px 24px;

  -moz-appearance: none; /* Firefox */
  -webkit-appearance: none; /* Safari and Chrome */
  appearance: none;
}

input:focus {
  outline: none;
}

.dropdown-icon {
  position: relative;
  padding: 14px 0px;
  margin-left: -48px;
}
</style>
