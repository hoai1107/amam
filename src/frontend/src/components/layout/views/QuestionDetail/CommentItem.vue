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
            <button @click="changeSentiment(userSentiment, Sentiment.LIKE)">
              <SvgIcon
                class="transition-none"
                :class="userSentiment === Sentiment.LIKE ? 'text-blue' : ''"
                size="24"
                type="mdi"
                :path="
                  userSentiment === Sentiment.LIKE
                    ? mdiArrowUpBold
                    : mdiArrowUpBoldOutline
                "
              ></SvgIcon>
            </button>
          </div>

          <!-- Dislike -->
          <div class="flex flex-row gap-2">
            <p>2</p>
            <button @click="changeSentiment(userSentiment, Sentiment.DISLIKE)">
              <SvgIcon
                class="transition-none"
                :class="userSentiment === Sentiment.DISLIKE ? 'text-blue' : ''"
                size="24"
                type="mdi"
                :path="
                  userSentiment === Sentiment.DISLIKE
                    ? mdiArrowDownBold
                    : mdiArrowDownBoldOutline
                "
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
  mdiArrowDownBold,
  mdiArrowUpBold,
  mdiDotsHorizontal,
} from "@mdi/js";
import { ref } from "vue";

const Sentiment = {
  DISLIKE: -1,
  NEUTRAL: 0,
  LIKE: 1,
};

const showReply = ref(false);
const userSentiment = ref(Sentiment.NEUTRAL);

function toggleReply() {
  showReply.value = !showReply.value;
}

function changeSentiment(oldSentiment, newSentiment) {
  if (oldSentiment == Sentiment.NEUTRAL) {
    userSentiment.value = newSentiment;
  } else {
    if (oldSentiment === newSentiment) {
      userSentiment.value = Sentiment.NEUTRAL;
    } else {
      userSentiment.value = newSentiment;
    }
  }
}
</script>

<style lang="scss" scoped></style>
