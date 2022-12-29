<template>
  <div>
    <p class="px-3 text-left text-xl font-semibold">{{ props.name }}</p>
    <p
      class="text-sm p-3 border-gray-100 border-solid hover:text-blueSky-dark-300 cursor-pointer"
      :class="[index != 1 ? 'border-t-2' : '']"
      v-for="index in 3"
      :key="index"
    >
      {{ questions[index - 1] }}
    </p>
    <p class="text-right text-sm text-blue cursor-pointer">See all</p>
  </div>
</template>

<script setup>
const props = defineProps({
  name: String,
});

const questions = [
  "Where should I store my CSV files for Memgraph?",
  "TabView PageTabViewStyle scroll information not working after tab disappears from screen SwiftUI iOS 16",
  "Switch Statement not working but does for other statement in java",
];
</script>

<style lang="scss" scoped></style>
