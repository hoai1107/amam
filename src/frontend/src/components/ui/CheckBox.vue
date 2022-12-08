<script setup>
import SvgIcon from "@jamescoyle/vue-icon";
import { mdiCheckBold } from "@mdi/js";
const props = defineProps({
  text: String,
});
</script>

<template>
    <div class="flex flex-row items-center">
      <div class="tick-box flex flex-row items-center justify-center">
        <input
          type="checkbox"
          id="remembered"
          class="input-checkbox items-center"
          v-model="remembered"
        />
        <span class="flex tick-icon">
          <svg-icon type="mdi" :path="mdiCheckBold" size="10"></svg-icon>
        </span>
      </div>
      <label for="remembered">{{text}}</label>
    </div>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.tick-box input[type="checkbox"]:checked ~ .tick-icon {
  opacity: 1;
}

.input-checkbox {
  cursor: pointer;
  opacity: 0;
  z-index: 1;
}
.tick-icon {
  position: absolute;
  opacity: 0;
}

.tick-box {
  width: 14px;
  height: 14px;

  background: #ffffff;
  border: 2px solid #000000;
  border-radius: 2px;
  margin-right: 8px;
}
</style>
