import axios from "axios";
import Constants from "@/plugins/Constants.js";
import { defineStore } from "pinia";
import { ref } from "vue";
import router from "@/router";

const instance = axios.create({
  baseURL: Constants.BACKEND_URL,
});

export const useAuthStore = defineStore("auth", () => {
  const user = ref({});

  async function loginUser(email, password) {
    // const response = await instance.post("/sign-in", {
    //   email: email,
    //   password: password,
    // });

    // // Do something with the response here.
    // console.log(response.data);
    console.log(email);
    console.log(password);
  }

  async function registerUser(name, email, password) {
    console.log(email);
    console.log(password);
    console.log(name);

    // Fake response model
    return {
      code: 200,
      message: "Login successfully",
    };
  }

  function isAuthenticated() {
    return !(
      user.value &&
      Object.keys(user.value).length === 0 &&
      Object.getPrototypeOf(user.value) === Object.prototype
    );
  }

  return { user, loginUser, registerUser, isAuthenticated };
});
