import axios from "axios";
import Constants from "@/plugins/Constants.js";
import { defineStore } from "pinia";
import { ref, watch } from "vue";
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

    const response = await instance.post("/sign-in", data, config);

    if (response.status === 200) {
      accessToken.value = response.data.access_token;
      isLogin.value = true;

      await sleep(2000);
      await userStore.fetchCurrentUserInfo();
      router.push({ name: "home" });
    } else {
      router.push({ name: "login", query: { msg: "wrongCredentials" } });
    }
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
    return accessToken.value != "";
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

  return {
    accessToken,
    isLogin,
    loginUser,
    registerUser,
    isAuthenticated,
    getAuthHeader,
    getAxiosInstance,
  };
});
