import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./components/HomePage.vue";
import MyListPage from "./components/MyListPage.vue";
import Authentication from "./components/Authentication.vue";

const routes = [
  {
    path: "/",
    component: Authentication, // Shows login page if not authenticated
    meta: { requiresAuth: false },
  },
  {
    path: "/home",
    component: HomePage, // Main homepage after login
    meta: { requiresAuth: true },
  },
  {
    path: "/mylist",
    component: MyListPage, // My List page
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to protect authenticated routes
router.beforeEach((to, from, next) => {
  const isAuth = localStorage.getItem("isAuth"); // Retrieve authentication status
  if (to.meta.requiresAuth && !isAuth) {
    next("/"); // Redirect to login if not authenticated
  } else {
    next(); // Allow navigation
  }
});

export default router;
