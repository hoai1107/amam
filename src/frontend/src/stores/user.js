import { defineStore } from "pinia";
import { useAuthStore } from "./auth";
import axios from "axios";
import Constants from "@/plugins/Constants.js";
import { ref } from "vue";

const instance = axios.create({
  baseURL: Constants.BACKEND_URL + "users",
});

export const useUserStore = defineStore("user", () => {
  const auth = useAuthStore();
  const user = ref();

  async function fetchCurrentUserInfo() {
    const config = {
      headers: {
        Authorization: `Bearer ${auth.accessToken}`,
      },
    };

    const response = await instance.get("/", config);
    console.log(response);
    user.value = response.data;
  }
  return { user, fetchCurrentUserInfo };
});
