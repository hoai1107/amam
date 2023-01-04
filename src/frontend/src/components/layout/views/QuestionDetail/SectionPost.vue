<template>
  <div class="flex flex-row items-center">
    <h1 class="text-xl font-semibold pr-4 mr-auto">
      {{ content.title }}
    </h1>
    <SvgIcon size="32" type="mdi" :path="mdiDotsVertical"></SvgIcon>
  </div>
  <PostMetaData
    :time-interval="timeInterval"
    :views="content.view"
  ></PostMetaData>
  <div class="flex gap-2 mb-4 mt-4">
    <div v-for="(tag, index) in content.tags" :key="index">
      <Tag :name="tag" />
    </div>
  </div>
  <p class="text-base">
    {{ content.content }}
  </p>
  <div class="flex flex-row mt-4 mb-6">
    <div class="flex flex-row gap-8">
      <div class="flex flex-row">
        <div class="mr-2 text-base">{{ content.upvote }}</div>
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
      <div class="flex flex-row">
        <div class="mr-2 text-base">
          <span v-show="content.downvote > 0">-</span>{{ content.downvote }}
        </div>
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
    </div>

    <!-- bookmark icon, bien mat doi voi anonymous, khi click se chuyen qua icon mdiBookmark co color blue (xem design system) -->
    <SvgIcon
      size="24"
      type="mdi"
      :path="mdiBookmarkOutline"
      class="ml-auto"
    ></SvgIcon>
  </div>
</template>

<script setup>
import Tag from "@/components/ui/Tag.vue";
import PostMetaData from "./PostMetaData.vue";
import { DateTime } from "luxon";
import {
  mdiArrowDownBold,
  mdiArrowUpBold,
  mdiArrowUpBoldOutline,
  mdiArrowDownBoldOutline,
  mdiCommentOutline,
  mdiEyeOutline,
  mdiBookmarkOutline,
  mdiBookmark,
  mdiDotsVertical,
} from "@mdi/js";
import SvgIcon from "@jamescoyle/vue-icon";
import { computed, toRefs, ref } from "vue";
import { useAuthStore } from "@/stores/auth.js";
import { useUserStore } from "@/stores/user.js";

const Sentiment = {
  DISLIKE: -1,
  NEUTRAL: 0,
  LIKE: 1,
};

const props = defineProps(["content"]);
const post = toRefs(props);
const authStore = useAuthStore();
const userStore = useUserStore();
const userSentiment = ref(Sentiment.NEUTRAL);

const instance = authStore.getAxiosInstance();

if (authStore.isAuthenticated()) {
  userSentiment.value = userStore.checkPostVoted(props.content._id);
}

console.log(props.content);

const timeInterval = computed(() => {
  const dateNow = DateTime.now();
  const dateCreated = DateTime.fromSQL(props.content.time_created);

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

function changeSentiment(oldSentiment, newSentiment) {
  // Set Ref value
  if (oldSentiment === newSentiment) {
    userSentiment.value = Sentiment.NEUTRAL;
  } else {
    userSentiment.value = newSentiment;
  }

  if (oldSentiment === Sentiment.LIKE) {
    post.content.value.upvote--;
  }

  if (oldSentiment === Sentiment.DISLIKE) {
    post.content.value.downvote--;
  }

  if (oldSentiment === Sentiment.NEUTRAL || oldSentiment !== newSentiment) {
    if (newSentiment === Sentiment.LIKE) {
      post.content.value.upvote++;
    } else {
      post.content.value.downvote++;
    }
  }

  var requestURL = "users/";
  if (newSentiment === Sentiment.LIKE) {
    requestURL += "upvote";
  } else {
    requestURL += "downvote";
  }

  instance
    .put(requestURL, null, {
      params: {
        postId: props.content._id,
      },
    })
    .then(async () => {
      await userStore.fetchCurrentUserInfo();
    });
}
</script>

<style lang="scss" scoped></style>
