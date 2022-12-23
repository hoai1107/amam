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
  const user = useUserStore();
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
      await user.fetchCurrentUserInfo();
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

  return {
    accessToken,
    isLogin,
    loginUser,
    registerUser,
    isAuthenticated,
  };
});
