<template>
  <div class="w-full h-full">
    <div class="flex flex-row-reverse gap-4">
      <router-link :to="{ name: 'login' }">
        <ButtonItem text="Login" type="primary" />
      </router-link>
      <router-link :to="{ name: 'signup' }">
        <ButtonItem text="Sign up" type="secondary" />
      </router-link>
    </div>
  </div>
</template>

<script setup>
import ButtonItem from "@/components/ui/ButtonItem.vue";
</script>

<style lang="scss" scoped></style>
