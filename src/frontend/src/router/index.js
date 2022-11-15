import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";

const baseRoutes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    alias: ["/index", "/home"],
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
  },
];

const questionsRoutes = [
  {
    path: "/questions",
    name: "questions",
    component: () => import("@/views/question/QuestionAllView.vue"),
    props: (route) => ({ ...route.query }),
  },
  {
    path: "/questions/:id",
    name: "questions.single",
    component: () => import("@/views/question/QuestionSingleView.vue"),
    props: (route) => ({ id: route.params.id }),
  },
  {
    path: "/questions/categories/:category",
    name: "questions.category",
    component: () => import("@/views/question/QuestionCategoryView.vue"),
    props: (route) => ({ category: route.params.category }),
  },
  {
    path: "/questions/search",
    name: "questions.search",
    component: () => import("@/views/question/QuestionSearchView.vue"),
    props: (route) => ({ ...route.query }),
  },
  {
    path: "/questions/create",
    name: "questions.create",
    component: () => import("@/views/question/QuestionCreateView.vue"),
  },
];

const userRoutes = [
  {
    path: "/user/:id",
    name: "user",
    component: () => import("@/views/user/UserProfileView.vue"),
    props: (route) => ({ id: route.params.id }),
  },
  {
    path: "/user/edit/:id",
    name: "user.edit",
    component: () => import("@/views/user/UserEditProfileView.vue"),
    props: (route) => ({ id: route.params.id }),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: [...baseRoutes, ...questionsRoutes, ...userRoutes],
});

export default router;
