<template>
  <Authentication v-if="!loggedIn" @login-successful="onLogin" />
  <div v-else>
    <nav>
      <ul>
        <li><a @click="currentView = 'TopAnime'">Top Anime</a></li>
        <li @click="currentView = 'NewReleases'"><a>New Releases</a></li>
        <li @click="currentView = 'Genre'"><a>Genres</a></li>
        <li @click="currentView = 'MyList'"><a>My List</a></li>
        <li @click="currentView = 'HomePage'"><a>Home</a></li>
        <li><a @click="logoutUser" class="logout-btn">Logout</a></li>
      </ul>
    </nav>

    <HomePage v-if="currentView === 'HomePage'" />
    <MyListPage v-if="currentView === 'MyList'" />
    <TopAnime
      v-if="currentView === 'TopAnime'"
      @getAnimeOverview="openAnimeDetails"
    />
    <GenrePage
      v-if="currentView === 'Genre'"
      @getAnimeOverview="openAnimeDetails"
      @getGenrePage="openGenreDetails"
    />
    <NewReleases
      v-if="currentView === 'NewReleases'"
      @getAnimeOverview="openAnimeDetails"
    />
    <AnimeOverview
      v-if="currentView === 'AnimeOverview'"
      :animeID="selectedAnime"
      @goBack="currentView = previousPage"
    />
    <GenreDisplay
      v-if="currentView === 'GenreDisplay'"
      :genreId="selectedGenre"
      @goBack="currentView = previousPage"
    />
  </div>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import Authentication from "./components/Authentication.vue";
import HomePage from "./components/HomePage.vue";
import MyListPage from "./components/MyListPage.vue";
import TopAnime from "./components/TopAnime.vue";
import GenrePage from "./components/Genres.vue";
import AnimeOverview from "./components/AnimeOverview.vue";
import NewReleases from "./components/NewReleases.vue";
import GenreDisplay from "./components/GenreDisplay.vue";

const loggedIn = ref(sessionStorage.getItem("isAuth") === "true");
const selectedAnime = ref(
  parseInt(sessionStorage.getItem("selectedAnime")) || null
);
const selectedGenre = ref(
  parseInt(sessionStorage.getItem("selectedGenre")) || null
);

const previousPage = ref(null);

let defaultView = sessionStorage.getItem("currentPage") || "HomePage";
const currentView = ref(defaultView);

watchEffect(() => {
  sessionStorage.setItem("currentPage", currentView.value);
});

function onLogin() {
  loggedIn.value = true;
  sessionStorage.setItem("isAuth", "true");
}

function getCSRFToken() {
  const tokenParts = `; ${document.cookie}`.split(`; csrftoken=`);
  return tokenParts.length === 2 ? tokenParts.pop().split(";").shift() : "";
}

function openAnimeDetails(animeId) {
  previousPage.value = currentView.value;
  selectedAnime.value = animeId;
  currentView.value = "AnimeOverview";
  sessionStorage.setItem("selectedAnime", animeId);
}

function openGenreDetails(genreId) {
  previousPage.value = currentView.value;
  selectedGenre.value = genreId;
  currentView.value = "GenreDisplay";
  sessionStorage.setItem("selectedGenre", genreId);
}

async function logoutUser() {
  try {
    const res = await fetch("http://localhost:8000/app/logout/", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
    });

    if (res.ok) {
      sessionStorage.removeItem("isAuth");
      sessionStorage.removeItem("currentPage");
      loggedIn.value = false;
      currentView.value = "HomePage";
    } else {
      console.warn("Logout didn't work as expected.");
    }
  } catch (err) {
    console.error("Something broke during logout:", err);
  }
}
</script>

<style src="./components/HomePageStyle.css" scoped></style>
