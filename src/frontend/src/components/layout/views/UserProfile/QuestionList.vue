<template>
  <div>
    <p class="px-3 text-left text-xl font-semibold">{{ props.name }}</p>
    <p
      class="text-sm p-3 border-gray-100 border-solid hover:text-blueSky-dark-300 cursor-pointer"
      v-for="(question, index) in questions"
      :class="[index + 1 != 1 ? 'border-t-2' : '']"
      :key="index"
    >
      {{ question }}
    </p>
    <p class="text-right text-sm text-blue cursor-pointer">See all</p>
  </div>
</template>

<script setup>
const props = defineProps({
  name: String,
  questions: Array,
});
</script>

<style lang="scss" scoped></style>
