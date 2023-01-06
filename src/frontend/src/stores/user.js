import { defineStore } from "pinia";
import { useAuthStore } from "./auth";
import axios from "axios";
import Constants from "@/plugins/Constants.js";
import { ref } from "vue";

// TODO: Watch for authStore to fetch token

export const useUserStore = defineStore("user", () => {
  const auth = useAuthStore();
  const user = ref();

  const instance = axios.create({
    baseURL: Constants.BACKEND_URL + "users",
    headers: {
      Accept: "application/json",
    },
  });

  instance.interceptors.request.use((config) => {
    if (auth.accessToken) {
      config.headers["Authorization"] = `Bearer ${auth.accessToken}`;
    }
    return config;
  });

  async function fetchCurrentUserInfo() {
    const response = await instance.get("");
    user.value = response.data;
  }

  function getQuestionList() {
    if (user.value) {
      return user.value.list_of_user_question;
    }

    return [];
  }

  function getBookmarkList() {
    if (user.value) {
      return user.value.bookmark;
    }

    return [];
  }

  function checkCommentVoted(id) {
    const commentVotes = user.value.list_of_comment_voted;

    for (var i = 0; i < commentVotes.length; ++i) {
      var vote = commentVotes[i];
      if (vote.id === id) {
        if (vote.upvote_downvote === "upvote") {
          return 1;
        } else {
          return -1;
        }
      }
    }
    return 0;
  }

  function checkPostVoted(id) {
    const postVotes = user.value.list_of_post_voted;

    for (var i = 0; i < postVotes.length; ++i) {
      var vote = postVotes[i];
      if (vote.id === id) {
        if (vote.upvote_downvote === "upvote") {
          return 1;
        } else {
          return -1;
        }
      }
    }
    return 0;
  }

  function checkPostBookmark(id) {
    if (!user.value) {
      return;
    }

    const postBookmark = user.value.bookmark;
    for (var i = 0; i < postBookmark.length; ++i) {
      var post = postBookmark[i];
      if (post._id === id) {
        return true;
      }
    }

    return false;
  }

  async function updateUserProfile(fields) {
    user.value = { ...user.value, ...fields };
    const instance = auth.getAxiosInstance();

    try {
      instance.put("/users/update", user.value);
    } catch (error) {
      console.log(error);
      return;
    }

    await fetchCurrentUserInfo();
  }

  function getUserId() {
    if (user.value) {
      return user.value._id;
    }

    return "";
  }

  function clearUserData() {
    user.value = "";
  }

  return {
    user,
    fetchCurrentUserInfo,
    checkCommentVoted,
    checkPostVoted,
    checkPostBookmark,
    getUserId,
    getQuestionList,
    getBookmarkList,
    updateUserProfile,
    clearUserData,
  };
});
