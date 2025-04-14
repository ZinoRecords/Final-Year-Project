<template>
  <Authentication
    v-if="!isAuth"
    @login-successful="onSuccessfulLogin"
  ></Authentication>
  <div v-else>
    <nav>
      <ul>
        <li><a @click="currentPage = 'TopAnime'">Top Anime</a></li>
        <li><a href="#new-releases">New Releases</a></li>
        <li><a href="#genres">Genres</a></li>
        <li @click="currentPage = 'MyList'"><a>My List</a></li>
        <li><a href="#community">Community</a></li>
        <li><a href="#news">News</a></li>
        <li><a @click="handleLogout" class="logout-btn">Logout</a></li>
      </ul>
    </nav>
    <HomePage v-if="currentPage === 'Home'"></HomePage>
    <MyListPage v-if="currentPage === 'MyList'"></MyListPage>
    <TopAnime v-if="currentPage === 'TopAnime'"></TopAnime>
  </div>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import HelloWorld from "./components/HelloWorld.vue";
import Authentication from "./components/Authentication.vue";
import HomePage from "./components/HomePage.vue";
import LoginPage from "./components/LoginPage.vue";
import MyListPage from "./components/MyListPage.vue";
import TopAnime from "./components/TopAnime.vue";

const isAuth = ref(sessionStorage.getItem("isAuth") === "true");
const defaultPage = sessionStorage.getItem("currentPage") || "Home";
const currentPage = ref(defaultPage);

watchEffect(() => {
  sessionStorage.setItem("currentPage", currentPage.value);
});

function onSuccessfulLogin() {
  isAuth.value = true;
  sessionStorage.setItem("isAuth", "true");
}

const getCSRFToken = () => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; csrftoken=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return "";
};

async function handleLogout() {
  try {
    const response = await fetch("http://localhost:8000/app/logout/", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
    });

    if (response.ok) {
      // Clear session storage
      sessionStorage.removeItem("isAuth");
      sessionStorage.removeItem("currentPage");
      // Reset auth state
      isAuth.value = false;
      // Reset current page
      currentPage.value = "Home";
    } else {
      console.error("Logout failed");
    }
  } catch (error) {
    console.error("Logout failed:", error);
  }
}
</script>

<style src="./components/HomePageStyle.css" scoped></style>

<style scoped>
/* Add these styles to your existing CSS */
.logout-btn {
  color: #ff69b4 !important; /* Using your existing pink color */
  font-weight: bold !important;
  cursor: pointer;
}

.logout-btn:hover {
  color: #ff1493 !important; /* Darker pink on hover */
}
</style>
