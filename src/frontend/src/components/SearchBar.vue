<script setup>
import SvgIcon from '@jamescoyle/vue-icon'
import { mdiMagnify } from '@mdi/js';
</script>

<template>
    <div class="container">
        <input class="search-bar" v-model="message" placeholder="Search a question" />
        <div class="dropdown-icon">
            <svg-icon type="mdi" :path="mdiMagnify"></svg-icon>
        </div>
    </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.container {
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

.search-bar {
  width: 732px;
  height: 48px;

  padding: 0px 24px;

  background: #FFFFFF;
  border: 2px solid #000000;
  border-radius: 8px;
  box-shadow: 4px 4px #000000;

  -moz-appearance:none; /* Firefox */
  -webkit-appearance:none; /* Safari and Chrome */
  appearance:none;
}

.dropdown-icon {
  position: relative;
  padding: 12px 0px;
  margin-left: -48px;
}
</style>
