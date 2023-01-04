import axios from "axios";
import Constants from "@/plugins/Constants.js";
import { defineStore } from "pinia";
import { ref } from "vue";
import router from "@/router";
import { useUserStore } from "./user";

const instance = axios.create({
  baseURL: Constants.BACKEND_URL + "authentication",
});

export const useAuthStore = defineStore("auth", () => {
  const userStore = useUserStore();
  const accessToken = ref("");
  const isLogin = ref(false);

  async function loginUser(email, password) {
    let data = {
      username: email,
      password: password,
    };

    let config = {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    };

    try {
      const response = await instance.post("/sign-in", data, config);

      if (response.status === 200) {
        accessToken.value = response.data.access_token;
        sessionStorage.setItem("accessToken", response.data.access_token);
        isLogin.value = true;
        await sleep(5000);
        await userStore.fetchCurrentUserInfo();
        return true;
      }
    } catch (error) {
      console.log(error);
      return false;
    }
  }

  function logoutUser() {
    accessToken.value = "";
    userStore.clearUserData();
    sessionStorage.removeItem("accessToken");
  }

  async function registerUser(name, email, password) {
    const response = await instance.post("/sign-up", {
      user_name: name,
      email: email,
      password: password,
    });

    return response;
  }

  function isAuthenticated() {
    return accessToken.value != "" && accessToken.value != null;
  }

  function getAxiosInstance() {
    return axios.create({
      baseURL: Constants.BACKEND_URL,
      headers: {
        Authorization: `Bearer ${accessToken.value}`,
      },
    });
  }

  function getAuthHeader() {
    return {
      headers: {
        Authorization: `Bearer ${accessToken.value}`,
      },
    };
  }

  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  async function getTokenFromStorage() {
    try {
      accessToken.value = sessionStorage.getItem("accessToken");
      await userStore.fetchCurrentUserInfo();
    } catch (error) {
      console.log(error);
    }
  }

  return {
    accessToken,
    isLogin,
    loginUser,
    registerUser,
    isAuthenticated,
    getAuthHeader,
    getAxiosInstance,
    logoutUser,
    getTokenFromStorage,
  };
});
