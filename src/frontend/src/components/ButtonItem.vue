<script setup>
const props = defineProps(
  {
    type: String,
    state: String
  }
)
</script>

<template>
  <button class="button" :class="[type, state]">Hello</button>
</template>
<style lang="scss" scoped>
@import "@/assets/styles/base.scss";

.button {
  border-radius: 8px;
  transition: all .5s;
  padding: 12px 24px;
  @extend .base-600;
}
/* BUTTON TYPE */
.primary {
  background-color: var(--blueSky-primary);
  border: 2px solid black;
}
.secondary {
  background-color: var(--white);
  border: 2px solid black;
}

/* BUTTON STATE */
.button:hover {
  box-shadow: 4px 4px #000000;
  transform: translate(-4px,-4px);
}
.primary.disabled {
  color: var(--blueSky-dark-100);
  border-color: var(--blueSky-dark-100);
  background-color: var(--blueSky-light-800);
}

.primary.disabled:hover {
  box-shadow: 0px 0px #000000;
  transform: translate(0px,0px);
}

.secondary.disabled {
  color: var(--blueSky-dark-100);
  border-color: var(--blueSky-dark-100);
}

.secondary.disabled:hover {
  box-shadow: 0px 0px #000000;
  transform: translate(0px,0px);
}
</style>

