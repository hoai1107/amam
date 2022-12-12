<template>
  <div class="flex flex-row gap-3">
    <!-- Avatar -->
    <div class="h-12">
      <Avatar />
    </div>

    <!-- Content -->
    <div class="flex flex-col gap-2">
      <div class="flex flex-row gap-6">
        <!-- Username -->
        <div class="text-base font-semibold">Hoai Tu</div>
        <!-- Timestamp -->
        <div class="text-base text-gray-400">2 hours ago</div>
      </div>

      <!-- Content -->
      <div class="text-base">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit ut aliquam,
        purus sit amet luctus venenatis
      </div>

      <!-- Buttons -->
      <div class="flex flex-row justify-between">
        <div class="flex flex-row gap-8">
          <!-- Like -->
          <div class="flex flex-row gap-2">
            <p>10</p>
            <button>
              <SvgIcon
                size="24"
                type="mdi"
                :path="mdiArrowUpBoldOutline"
              ></SvgIcon>
            </button>
          </div>

          <!-- Dislike -->
          <div class="flex flex-row gap-2">
            <p>2</p>
            <button>
              <SvgIcon
                size="24"
                type="mdi"
                :path="mdiArrowDownBoldOutline"
              ></SvgIcon>
            </button>
          </div>

          <div>
            <button @click="toggleReply">Reply</button>
          </div>
        </div>
        <button>
          <SvgIcon size="24" type="mdi" :path="mdiDotsHorizontal"></SvgIcon>
        </button>
      </div>

      <!-- Reply form -->
      <div class="flex flex-row gap-3" v-show="showReply">
        <input
          class="border-2 border-solid w-full px-6 rounded"
          type="text"
          placeholder="Add an answer..."
        />
        <div>
          <ButtonItem
            class="w-fit"
            type="primary"
            state="normal"
            text="Submit"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import Avatar from "@/components/ui/Avatar.vue";
import ButtonItem from "@/components/ui/ButtonItem.vue";
import SvgIcon from "@jamescoyle/vue-icon";
import {
  mdiArrowUpBoldOutline,
  mdiArrowDownBoldOutline,
  mdiDotsHorizontal,
} from "@mdi/js";
import { ref } from "vue";

const showReply = ref(false);

function toggleReply() {
  showReply.value = !showReply.value;
}
</script>

<style lang="scss" scoped></style>
