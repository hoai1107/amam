<template>
  <div class="flex flex-row items-center">
    <h1 class="text-xl font-semibold pr-4 mr-auto">
      {{ content.title }}
    </h1>
    <div>
      <button @click="toggleOptions">
        <SvgIcon size="32" type="mdi" :path="mdiDotsVertical"></SvgIcon>
      </button>
      <div
        v-show="showOptions"
        class="text-base mt-2 border-2 border-solid rounded px-2 py-2 absolute bg-white z-10 shadow-sm -translate-x-28"
      >
        <ul class="flex flex-col gap-1">
          <router-link :to="{ name: 'home' }">
            <li
              class="rounded flex flex-row gap-2 items-center justify-start px-4 hover:bg-blueSky-light-800"
            >
              <SvgIcon size="24" type="mdi" :path="mdiPencilOutline"></SvgIcon>
              <p>Edit</p>
            </li>
          </router-link>
          <li
            class="rounded flex flex-row gap-2 items-center text-red px-4 hover:bg-blueSky-light-800 cursor-pointer"
          >
            <SvgIcon size="24" type="mdi" :path="mdiDeleteOutline"></SvgIcon>
            <p>Delete</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <PostMetaData
    :username="content.user_name"
    :avatar="content.avatar"
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
        <button
          :class="authStore.isAuthenticated() ? '' : 'pointer-events-none'"
          @click="changeSentiment(userSentiment, Sentiment.LIKE)"
        >
          <SvgIcon
            class="transition-none"
            :class="[userSentiment === Sentiment.LIKE ? 'text-blue' : '']"
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
        <button
          :class="authStore.isAuthenticated() ? '' : 'pointer-events-none'"
          @click="changeSentiment(userSentiment, Sentiment.DISLIKE)"
        >
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

    <SvgIcon
      v-if="authStore.isAuthenticated()"
      class="transition-none cursor-pointer ml-auto"
      :class="isBookmark ? 'text-blue' : ''"
      size="24"
      type="mdi"
      :path="isBookmark ? mdiBookmark : mdiBookmarkOutline"
      @click="changeBookmark"
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
  mdiPencilOutline,
  mdiDeleteOutline,
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
const isBookmark = ref(false);
const showOptions = ref(false);

console.log(props.content);

const instance = authStore.getAxiosInstance();

if (authStore.isAuthenticated()) {
  userSentiment.value = userStore.checkPostVoted(props.content.id);
  isBookmark.value = userStore.checkPostBookmark(props.content.id);
}

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

  var requestURL = `users/`;
  if (newSentiment === Sentiment.LIKE) {
    requestURL += "upvote";
  } else {
    requestURL += "downvote";
  }
  requestURL += `/${props.content.id}`;

  instance.put(requestURL).then(async () => {
    await userStore.fetchCurrentUserInfo();
  });
}

function changeBookmark() {
  isBookmark.value = !isBookmark.value;
  instance.put(`/users/bookmark/${props.content.id}`).then(async () => {
    await userStore.fetchCurrentUserInfo();
  });
}

function toggleOptions() {
  showOptions.value = !showOptions.value;
}
</script>

<style lang="scss" scoped></style>
