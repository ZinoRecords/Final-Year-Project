<template>
  <div>
    <nav class="nav-gradient">
      <a href="#" class="logo">AnimeWorld</a>
      <div class="search-container">
        <input
          type="search"
          placeholder="Search anime..."
          class="search-input"
        />
        <button class="search-button">Search</button>
      </div>
    </nav>

    <!-- <div class="nav-menu">
      <a href="#" v-for="item in menuItems" :key="item">{{ item }}</a>
    </div> -->

    <main class="container">
      <div class="header-container">
        <h1 class="page-title">My Favorite Anime</h1>
        <button class="fetch-button" @click="fetchAnimes">Fetch Anime</button>
        <div style="position: relative">
          <button class="filter-button" @click="toggleDropdown">
            Sort by
            <svg
              width="12"
              height="12"
              viewBox="0 0 12 12"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M2.5 4L6 7.5L9.5 4"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>
          <div class="dropdown-content" :class="{ show: isDropdownVisible }">
            <button @click="sortAnime('title')">Sort by Title</button>
            <button @click="sortAnime('rating-high')">
              Rating: High to Low
            </button>
            <button @click="sortAnime('rating-low')">
              Rating: Low to High
            </button>
          </div>
        </div>
      </div>
      <div class="grid">
        <div
          v-for="anime in sortedAnimeList"
          :key="anime.id"
          class="anime-card"
        >
          <div class="image-container">
            <img
              v-if="anime.image"
              :src="anime.image"
              :alt="anime.title"
              class="anime-image"
            />
            <div v-else class="no-image">No image found</div>
          </div>
          <h2 class="anime-title">{{ anime.title }}</h2>
          <div class="rating">
            <span class="star">★</span>
            <span>{{ anime.rating.toFixed(1) }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      menuItems: [
        "Popular",
        "New Releases",
        "Genres",
        "My List",
        "Community",
        "News",
      ],
      animeList: [
        { id: 1, title: "Attack on Titan", rating: 9.0, image: "" },
        { id: 2, title: "Death Note", rating: 8.6, image: "" },
        {
          id: 3,
          title: "Fullmetal Alchemist: Brotherhood",
          rating: 9.1,
          image: "",
        },
        { id: 4, title: "One Punch Man", rating: 8.7, image: "" },
        { id: 5, title: "My Hero Academia", rating: 8.4, image: "" },
        { id: 6, title: "Demon Slayer", rating: 8.9, image: "" },
      ],
      isDropdownVisible: false,
      sortCriteria: null,
      sortOrder: "asc",
      apiTest: "",
    };
  },
  computed: {
    sortedAnimeList() {
      const sorted = [...this.animeList];
      if (this.sortCriteria === "title") {
        sorted.sort((a, b) => a.title.localeCompare(b.title));
      } else if (this.sortCriteria === "rating") {
        sorted.sort((a, b) =>
          this.sortOrder === "asc" ? a.rating - b.rating : b.rating - a.rating
        );
      }
      return sorted;
    },
  },
  methods: {
    toggleDropdown() {
      this.isDropdownVisible = !this.isDropdownVisible;
    },
    sortAnime(criteria) {
      if (criteria === "title") {
        this.sortCriteria = "title";
      } else if (criteria === "rating-high") {
        this.sortCriteria = "rating";
        this.sortOrder = "desc";
      } else if (criteria === "rating-low") {
        this.sortCriteria = "rating";
        this.sortOrder = "asc";
      }
      this.isDropdownVisible = false;
    },
    async fetchAnimes() {
      try {
        const response = await fetch("https://api.jikan.moe/v4/anime?limit=20"); // Fetch only 20 anime
        const data = await response.json();
        this.apiTest = data.data.map((anime) => ({
          id: anime.mal_id,
          title: anime.title,
          rating: anime.score || "N/A",
          image: anime.images.jpg.image_url || "",
        })); // Store fetched anime list
        console.log(this.apiTest);
      } catch (err) {
        console.error(err);
      }
    },
  },
  mounted() {
    document.addEventListener("click", (event) => {
      if (
        !event.target.closest(".filter-button") &&
        !event.target.closest(".dropdown-content")
      ) {
        this.isDropdownVisible = false;
      }
    });
  },
};
</script>

<style src="./MyListPage.css" scoped></style>
