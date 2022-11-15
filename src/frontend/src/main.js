import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import "@/assets/styles/reset.css";
import "@/assets/styles/base.scss";
import "@/assets/styles/styles.scss";
import router from "@/router";

const app = createApp(App);

app.use(router);
app.use(createPinia());
app.mount("#app");
