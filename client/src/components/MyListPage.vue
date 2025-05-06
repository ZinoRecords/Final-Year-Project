<template>
  <div class="my-list-container">
    <header class="main-header">
      <h1>AnimeWorld</h1>
      <div class="search-container">
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Search anime..."
          @keypress.enter="performSearch"
        />
        <button @click="performSearch">🔍</button>
      </div>
    </header>

    <main>
      <h2 class="section-title">My Favorite Anime</h2>

      <div class="filter-controls">
        <div class="filter-dropdown">
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

      <div v-if="isLoading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading your favorites...</p>
      </div>

      <div v-else-if="error" class="error-container">
        <p>{{ error }}</p>
        <button @click="fetchFavorites" class="retry-button">Try Again</button>
      </div>

      <div v-else-if="animeList.length === 0" class="no-favorites">
        <p>You haven't added any anime to your favorites yet.</p>
        <p>Browse anime and click the star icon to add them here!</p>
      </div>

      <div v-else class="anime-grid">
        <div
          v-for="anime in sortedAnimeList"
          :key="anime.id"
          class="anime-card"
        >
          <div class="anime-image">
            <img
              :src="anime.imageURL"
              :alt="anime.name"
              @error="handleImgError($event)"
            />
            <div class="anime-type">{{ anime.type || "TV" }}</div>
            <button
              class="remove-button"
              @click.stop="removeFromFavorites(anime)"
              title="Remove from favorites"
            >
              Remove
            </button>
          </div>
          <div class="anime-details">
            <h3 class="anime-title">{{ anime.name }}</h3>
            <div class="anime-meta" v-if="anime.releaseDate">
              <span>Released: {{ formatDate(anime.releaseDate) }}</span>
            </div>
            <div class="anime-stats">
              <div class="anime-rating" v-if="anime.rating">
                <span class="star-icon">★</span> {{ anime.rating }}
              </div>
            </div>
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
      searchTerm: "",
      animeList: [],
      isLoading: false,
      error: null,
      isDropdownVisible: false,
      sortCriteria: null,
      sortOrder: "asc",
      placeholderImg:
        "https://placehold.co/320x200/9333ea/ffffff?text=No+Image",
    };
  },
  computed: {
    sortedAnimeList() {
      if (!this.animeList.length) return [];

      const sorted = [...this.animeList];

      if (this.sortCriteria === "title") {
        sorted.sort((a, b) => a.name.localeCompare(b.name));
      } else if (this.sortCriteria === "rating-high") {
        sorted.sort((a, b) => (b.rating || 0) - (a.rating || 0));
      } else if (this.sortCriteria === "rating-low") {
        sorted.sort((a, b) => (a.rating || 0) - (b.rating || 0));
      }

      return sorted;
    },
  },
  methods: {
    performSearch() {
      const query = this.searchTerm.trim();
      if (query) {
        this.$emit("search", query);
      }
    },

    getCSRFToken() {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; csrftoken=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
      return "";
    },

    toggleDropdown() {
      this.isDropdownVisible = !this.isDropdownVisible;
    },

    sortAnime(criteria) {
      this.sortCriteria = criteria;
      this.isDropdownVisible = false;
    },

    handleImgError(event) {
      event.target.onerror = null;
      event.target.src = this.placeholderImg;
    },

    formatDate(dateString) {
      if (!dateString) return "Unknown";

      if (dateString.length === 4 || !isNaN(dateString)) {
        return dateString;
      }

      try {
        const date = new Date(dateString);
        return date.toLocaleDateString("en-US", {
          year: "numeric",
          month: "short",
          day: "numeric",
        });
      } catch (e) {
        return dateString;
      }
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
        this.animeList = data;
      } catch (err) {
        console.error("Error fetching favorites:", err);
        this.error = "Failed to load favorite animes";
      } finally {
        this.isLoading = false;
      }
    },

    async removeFromFavorites(anime) {
      try {
        const response = await fetch(
          "http://localhost:8000/app/favorites/remove/",
          {
            method: "DELETE",
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.getCSRFToken(),
            },
            body: JSON.stringify({
              name: anime.name,
            }),
          }
        );

        if (!response.ok) {
          throw new Error("Failed to remove from favorites");
        }

        const data = await response.json();
        console.log(data.message || data.error);

        this.animeList = this.animeList.filter((item) => item.id !== anime.id);
      } catch (error) {
        console.error("Request failed:", error);
        alert("Failed to remove from favorites. Please try again.");
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

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Arial", sans-serif;
  background-color: #f3e8ff;
}

.my-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  background-color: #f3e8ff;
  min-height: 100vh;
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

h1 {
  color: #9333ea;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.search-container {
  display: flex;
  max-width: 400px;
}

.search-container input {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  width: 100%;
  font-size: 1rem;
}

.search-container button {
  background-color: #db2777;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 1rem;
}

.search-container button:hover {
  background-color: #be185d;
}

.section-title {
  color: #9333ea;
  font-size: 2rem;
  text-align: center;
  margin-bottom: 2rem;
}

.filter-controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 2rem;
}

.filter-dropdown {
  position: relative;
}

.filter-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: white;
  border: 1px solid #9333ea;
  color: #9333ea;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.filter-button:hover {
  background-color: #f3e8ff;
}

.dropdown-content {
  position: absolute;
  right: 0;
  top: 100%;
  background-color: white;
  min-width: 180px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
  overflow: hidden;
  z-index: 10;
  display: none;
}

.dropdown-content.show {
  display: block;
}

.dropdown-content button {
  display: block;
  width: 100%;
  text-align: left;
  padding: 0.75rem 1rem;
  border: none;
  background: none;
  cursor: pointer;
  color: #333;
  font-size: 0.9rem;
}

.dropdown-content button:hover {
  background-color: #f3e8ff;
  color: #9333ea;
}

.loading-container,
.error-container,
.no-favorites {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(147, 51, 234, 0.2);
  border-radius: 50%;
  border-top-color: #9333ea;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #9333ea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-button:hover {
  background-color: #7e22ce;
}

.no-favorites {
  color: #666;
}

.no-favorites p:first-child {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.anime-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.anime-card {
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  background-color: white;
  cursor: pointer;
}

.anime-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2);
}

.anime-image {
  position: relative;
  height: 280px;
  background-color: #f0f0f0;
}

.anime-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.anime-type {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: #db2777;
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.remove-button {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background-color: rgba(219, 39, 119, 0.9);
  color: white;
  border: none;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.remove-button:hover {
  background-color: #be185d;
}

.anime-details {
  padding: 1rem;
}

.anime-title {
  font-weight: bold;
  color: #9333ea;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.anime-meta {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.anime-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
}

.anime-rating {
  font-size: 0.875rem;
  color: #db2777;
  font-weight: 500;
}

.star-icon {
  font-size: 0.875rem;
  margin-right: 0.25rem;
}

@media (max-width: 768px) {
  .main-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-container {
    width: 100%;
    margin-top: 1rem;
  }

  .filter-controls {
    justify-content: center;
  }

  .anime-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }

  .anime-image {
    height: 220px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .anime-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}
</style>
