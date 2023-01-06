<template>
  <div>
    <div class="flex flex-col gap-3 py-3">
      <div class="flex flex-row gap-3 h-12">
        <Avatar :image-src="userStore.user.avatar" class="w-fit" />
        <input
          class="border-2 border-solid w-full px-6 rounded"
          type="text"
          placeholder="Add an answer..."
          v-model="comment"
        />
      </div>
      <div class="flex flex-row-reverse w-full">
        <div @click="$emit('submit-comment', comment)">
          <ButtonItem type="primary" state="normal" text="Submit" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Avatar from "@/components/ui/Avatar.vue";
import ButtonItem from "@/components/ui/ButtonItem.vue";
import { ref } from "vue";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
const comment = ref();
</script>

<style lang="scss" scoped></style>
