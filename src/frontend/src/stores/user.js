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
    console.log(response);
  }
  return { user, fetchCurrentUserInfo };
});
