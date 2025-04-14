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

      <div v-if="isLoading" class="loading">Loading your favorites...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="animeList.length === 0" class="no-favorites">
        No favorite anime added yet.
      </div>

      <div v-else class="grid">
        <div
          v-for="anime in sortedAnimeList"
          :key="anime.id"
          class="anime-card"
        >
          <div class="image-container">
            <img
              v-if="anime.imageURL"
              :src="anime.imageURL"
              :alt="anime.name"
              class="anime-image"
            />
            <div v-else class="no-image">No image found</div>
          </div>
          <h2 class="anime-title">{{ anime.name }}</h2>
          <div class="rating">
            <span class="star">★</span>
            <span>{{ anime.rating }}</span>
          </div>
          <button @click="removeFromFavorites(anime.id)" class="remove-button">
            Remove from Favorites
          </button>
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
      animeList: [],
      favoriteAnimes: [],
      isLoading: false,
      error: null,
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
    async getFavorites() {
      const response = await fetch("http://localhost:8000/app/favorites/", {
        credentials: "include",
      });
      const data = await response.json();
      return data;
    },
    async addToFavorites(animeId) {
      const response = await fetch(
        `http://localhost:8000/app/favorites/add/${animeId}/`,
        {
          method: "POST",
          credentials: "include",
        }
      );
      const data = await response.json();
      return data;
    },
    async fetchFavorites() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await fetch("http://localhost:8000/app/favorites/", {
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error("Failed to fetch favorites");
        }
        const data = await response.json();
        this.animeList = data; // Update animeList with favorite animes
      } catch (err) {
        console.error("Error fetching favorites:", err);
        this.error = "Failed to load favorite animes";
      } finally {
        this.isLoading = false;
      }
    },

    async removeFromFavorites(animeId) {
      try {
        const response = await fetch(
          `http://localhost:8000/app/favorites/remove/${animeId}/`,
          {
            method: "DELETE",
            credentials: "include",
          }
        );
        if (response.ok) {
          // Remove the anime from the list
          this.animeList = this.animeList.filter(
            (anime) => anime.id !== animeId
          );
        }
      } catch (err) {
        console.error("Error removing from favorites:", err);
      }
    },
  },
  mounted() {
    this.fetchFavorites();
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

<style scoped>
.loading,
.error,
.no-favorites {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.error {
  color: red;
}

.remove-button {
  background-color: #ff4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 0.5rem;
}

.remove-button:hover {
  background-color: #cc0000;
}
</style>
