<template>
  <div class="h-screen flex flex-row items-center">
    <div
      class="max-w-default mx-auto my-auto grid grid-cols-12 gap-x-6 flex flex-row"
    >
      <div class="col-span-7">
        <h1 class="text-3xl font-semibold mb-8">
          Let’s Connect Through The Questions!
        </h1>
        <img src="../assets/img/img-login.png" alt="people-chatting-img" />
      </div>
      <div class="col-span-4 col-start-9 flex flex-col items-center">
        <img src="../assets/img/logo-lg.png" class="mb-6" alt="AMAM logo" />
        <p class="text-3xl mb-4">Sign up</p>
        <p class="text-base mb-9">
          Already had an account?
          <a href="#" class="text-blue hover:text-blue-dark">Login</a>
        </p>
        <SignUpForm></SignUpForm>
        <p class="mt-6">
          or
          <a href="#" class="text-blue hover:text-blue-dark"
            >continue as guest</a
          >
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import SignUpForm from "@/components/SignUpForm.vue";
</script>

<style lang="scss" scoped></style>
