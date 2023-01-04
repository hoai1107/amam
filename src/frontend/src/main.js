import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import "@/assets/styles/reset.css";
import "@/assets/styles/base.scss";
import "@/assets/styles/styles.scss";

import router from "@/router";


const app = createApp(App);
const clickOutside = {
  beforeMount: (el, binding) => {
    el.clickOutsideEvent = (event) => {
      // here I check that click was outside the el and his children
      if (!(el == event.target || el.contains(event.target))) {
        // and if it did, call method provided in attribute value
        binding.value();
      }
    };
    document.addEventListener("click", el.clickOutsideEvent);
  },
  unmounted: (el) => {
    document.removeEventListener("click", el.clickOutsideEvent);
  },
};

app.use(router);
app.use(createPinia());
app.directive("click-outside", clickOutside);

import { useAuthStore } from "./stores/auth";

const authStore = useAuthStore();
await authStore.getTokenFromStorage();

app.mount("#app");
