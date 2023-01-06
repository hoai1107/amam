<template>
  <div class="flex flex-row gap-3">
    <!-- Avatar -->
    <div class="h-12 aspect-square">
      <Avatar :image-src="comment.user_avatar" />
    </div>

    <!-- Content -->
    <div class="flex flex-col gap-2 w-full">
      <div class="flex flex-row gap-6">
        <!-- Username -->
        <div class="text-base font-semibold">{{ comment.user_name }}</div>
        <!-- Timestamp -->
        <div class="text-base text-gray-400">{{ timeInterval }}</div>
      </div>

      <!-- Content -->
      <div class="text-base">
        {{ comment.content }}
      </div>

      <!-- Buttons -->
      <div class="flex flex-row justify-between">
        <div class="flex flex-row gap-8">
          <!-- Like -->
          <div class="flex flex-row gap-2">
            <p>{{ comment.upvote }}</p>
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
            <p>{{ comment.downvote }}</p>
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
            <button
              v-if="authStore.isAuthenticated()"
              @click="toggleReply"
              v-show="canReply"
            >
              Reply
            </button>
          </div>
        </div>
        <button>
          <SvgIcon size="24" type="mdi" :path="mdiDotsHorizontal"></SvgIcon>
        </button>
      </div>

      <!-- Reply -->
      <div class="flex flex-col mt-2 gap-2">
        <CommentItem
          v-for="reply in comment.list_child_comment"
          :comment="reply"
          :can-reply="false"
          v-bind:key="reply._id"
        />
      </div>

      <!-- Reply form -->
      <div class="flex flex-row gap-3" v-show="showReply">
        <input
          class="border-2 border-solid w-full px-6 rounded"
          type="text"
          placeholder="Add an answer..."
          v-model="reply"
        />
        <div>
          <ButtonItem
            class="w-fit"
            type="primary"
            state="normal"
            text="Submit"
            @click="$emit('submit-reply', reply, comment._id)"
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
import { ref, toRefs, computed } from "vue";
import { useAuthStore } from "@/stores/auth.js";
import { useUserStore } from "@/stores/user.js";
import { DateTime } from "luxon";
import Constants from "@/plugins/Constants.js";
import axios from "axios";

const Sentiment = {
  DISLIKE: -1,
  NEUTRAL: 0,
  LIKE: 1,
};

const props = defineProps({
  comment: Object,
  canReply: Boolean,
});
const content = toRefs(props);
const authStore = useAuthStore();
const userStore = useUserStore();
const reply = ref();
const showReply = ref(false);
const userSentiment = ref(Sentiment.NEUTRAL);

console.log(props.comment);

if (authStore.isAuthenticated()) {
  userSentiment.value = userStore.checkCommentVoted(props.comment._id);
}

const timeInterval = computed(() => {
  const dateNow = DateTime.now();
  const dateCreated = DateTime.fromSQL(props.comment.time_created);

  const diff = dateNow
    .diff(dateCreated, ["years", "months", "days", "hours", "minutes"])
    .toObject();

  for (const measurement in diff) {
    const val = Math.floor(diff[measurement]);

    if (val !== 0) {
      return `${val} ${measurement} ago`;
    }
  }

  return "Just a second ago";
});

const config = authStore.getAuthHeader();
const instance = axios.create({
  baseURL: Constants.BACKEND_URL,
  ...config,
});

function toggleReply() {
  showReply.value = !showReply.value;
}

function changeSentiment(oldSentiment, newSentiment) {
  // Set Ref value
  if (oldSentiment === newSentiment) {
    userSentiment.value = Sentiment.NEUTRAL;
  } else {
    userSentiment.value = newSentiment;
  }

  if (oldSentiment === Sentiment.LIKE) {
    content.comment.value.upvote--;
  }

  if (oldSentiment === Sentiment.DISLIKE) {
    content.comment.value.downvote--;
  }

  if (oldSentiment === Sentiment.NEUTRAL || oldSentiment !== newSentiment) {
    if (newSentiment === Sentiment.LIKE) {
      content.comment.value.upvote++;
    } else {
      content.comment.value.downvote++;
    }
  }

  var requestURL = `users/comment/${props.comment._id}/`;
  if (newSentiment === Sentiment.LIKE) {
    requestURL += "upvote";
  } else {
    requestURL += "downvote";
  }

  instance.put(requestURL).then(async () => {
    await userStore.fetchCurrentUserInfo();
  });
}
</script>

<style lang="scss" scoped></style>
