import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";

const baseRoutes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    alias: ["/index", "/home"],
    props: (route) => ({ ...route.query }),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginView.vue"),
  },
  {
    path: "/sign-up",
    name: "signup",
    component: () => import("@/views/SignUpView.vue"),
  },
  {
    path: "/test",
    name: "test",
    component: () => import("@/views/TestView.vue"),
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
    path: "/questions/categories/all",
    name: "questions.category.all",
    component: () => import("@/views/question/QuestionCategoryView.vue"),
  },
  {
    path: "/questions/categories/:category",
    name: "questions.category",
    redirect: (to) => {
      return { name: "questions", query: { category: to.params.category } };
    },
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
    component: () => import("@/views/user/UserProfileEditView.vue"),
    props: (route) => ({ id: route.params.id }),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: [...baseRoutes, ...questionsRoutes, ...userRoutes],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  },
});

export default router;
