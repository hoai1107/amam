<script setup>
const props = defineProps({
  type: String,
  state: String,
  text: String,
});
</script>

<template>
  <button
    class="hover:shadow-sm border-2 border-solid rounded text-base font-semibold"
    :class="[type, state]"
    @click="$emit('buttonClick')"
  >
    {{ props.text }}
  </button>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

button {
  transition: all 0.3s;
  padding: 12px 24px;
  text-align: center;
}
/* BUTTON TYPE */
.primary {
  background-color: theme("colors.blueSky.DEFAULT");
  border-color: black;
}
.secondary {
  background-color: theme("colors.white");
  border-color: black;
}

/* BUTTON STATE */
button:hover {
  transform: translate(-2px, -2px);
}
.primary.disabled {
  color: theme("colors.blueSky.dark.100");
  border-color: theme("colors.blueSky.dark.100");
  background-color: theme("colors.blueSky.light.800");
}

.primary.disabled:hover {
  box-shadow: 0px 0px #000000;
  transform: translate(0px, 0px);
  cursor: default;
}

.secondary.disabled {
  color: theme("colors.blueSky.dark.100");
  border-color: theme("colors.blueSky.dark.100");
}

.secondary.disabled:hover {
  box-shadow: 0px 0px #000000;
  transform: translate(0px, 0px);
  cursor: default;
}
</style>
