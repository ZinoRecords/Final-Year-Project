<template>
  <div class="genre-detail-container">
    <header class="main-header">
      <h1>AnimeWorld</h1>
      <div class="search-container">
        <input
          v-model="searchTerm"
          @keypress.enter="performSearch"
          placeholder="Search anime..."
        />
        <button @click="performSearch">🔍</button>
      </div>
    </header>

    <main>
      <div class="genre-header">
        <h2 class="section-title">{{ genreName }} Anime</h2>
        <button class="back-button" @click="goBack">← Back to Genres</button>
      </div>

      <div class="filter-controls">
        <div class="filter-dropdown">
          <button class="filter-button" @click="toggleFilterDropdown">
            Sort by: {{ getSortLabel() }}
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
          <div
            class="dropdown-content"
            :class="{ show: isFilterDropdownVisible }"
          >
            <button @click="setSortOption('popularity', 'asc')">
              Most Popular
            </button>
            <button @click="setSortOption('popularity', 'desc')">
              Least Popular
            </button>
            <button @click="setSortOption('rating', 'desc')">
              Highest Rating
            </button>
            <button @click="setSortOption('rating', 'asc')">
              Lowest Rating
            </button>
            <button @click="setSortOption('title', 'asc')">Title (A-Z)</button>
            <button @click="setSortOption('title', 'desc')">Title (Z-A)</button>
          </div>
        </div>

        <div class="view-toggle">
          <span>View:</span>
          <button
            :class="{ active: viewMode === 'list' }"
            @click="setView('list')"
          >
            List
          </button>
          <button
            :class="{ active: viewMode === 'grid' }"
            @click="setView('grid')"
          >
            Grid
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading anime...</p>
      </div>

      <div v-else-if="error" class="error-container">
        <p>{{ error }}</p>
        <button @click="fetchAnimeByGenre" class="retry-button">
          Try Again
        </button>
      </div>

      <div v-else-if="animeList.length === 0" class="no-results">
        <p>No anime found for this genre.</p>
      </div>

      <div
        v-else
        :class="[
          'anime-container',
          viewMode === 'grid' ? 'anime-grid' : 'anime-list',
        ]"
      >
        <div
          v-for="anime in animeList"
          :key="anime.id"
          class="anime-card"
          @click="getAnimeOverview(anime.id)"
        >
          <div
            class="favorite-btn"
            @click.stop="toggleFavorite(anime)"
            :title="
              favorites.has(anime.id)
                ? 'Remove from favorites'
                : 'Add to favorites'
            "
          >
            <span :class="{ favorited: favorites.has(anime.id) }">★</span>
          </div>

          <div class="anime-image">
            <img
              :src="anime.image"
              :alt="anime.title"
              @error="handleImgError($event)"
            />
            <div class="anime-type">{{ anime.type }}</div>
            <div v-if="anime.airing" class="airing-badge">Airing</div>
          </div>
          <div class="anime-details">
            <h3 class="anime-title" :title="anime.title">{{ anime.title }}</h3>

            <div v-if="viewMode === 'list'" class="anime-meta">
              <span>{{ anime.episodes }} Episodes</span>
              <span class="separator"></span>
              <span>Released: {{ anime.year }}</span>
            </div>

            <div v-if="viewMode === 'list'" class="anime-genres">
              <span
                class="genre-tag"
                v-for="(genre, index) in anime.genres.slice(0, 4)"
                :key="index"
              >
                {{ genre }}
              </span>
            </div>

            <div v-if="viewMode === 'list'" class="anime-description">
              {{ anime.synopsis || "No description available." }}
            </div>

            <div class="anime-stats">
              <div class="anime-rating" v-if="anime.rating">
                <span class="star-icon">★</span> {{ anime.rating }}
              </div>
              <div class="anime-members" v-if="anime.members">
                <span class="members-icon">👥</span>
                {{ formatMembers(anime.members) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && !error && totalPages > 1" class="pagination">
        <button
          class="pagination-btn"
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          Previous
        </button>

        <div class="page-numbers">
          <button
            v-for="page in displayedPages"
            :key="page"
            :class="['page-number', { active: currentPage === page }]"
            @click="changePage(page)"
          >
            {{ page }}
          </button>
        </div>

        <button
          class="pagination-btn"
          :disabled="currentPage === totalPages"
          @click="changePage(currentPage + 1)"
        >
          Next
        </button>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "GenreDetail",
  props: {
    genreId: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      searchTerm: "",
      viewMode: "grid",
      loading: true,
      error: null,
      animeList: [],
      favorites: new Set(),
      isFilterDropdownVisible: false,
      sortBy: "rating",
      sortOrder: "desc",
      currentPage: 1,
      itemsPerPage: 25,
      totalAnime: 0,
      totalPages: 1,
      placeholderImg:
        "https://placehold.co/320x200/9333ea/ffffff?text=No+Image",
      genreName: "Loading...",
    };
  },
  computed: {
    displayedPages() {
      const pages = [];
      const maxVisiblePages = 5;

      if (this.totalPages <= maxVisiblePages) {
        for (let i = 1; i <= this.totalPages; i++) {
          pages.push(i);
        }
      } else {
        pages.push(1);
        let startPage = Math.max(2, this.currentPage - 1);
        let endPage = Math.min(this.totalPages - 1, this.currentPage + 1);

        if (this.currentPage <= 2) {
          endPage = 4;
        } else if (this.currentPage >= this.totalPages - 1) {
          startPage = this.totalPages - 3;
        }

        if (startPage > 2) pages.push("...");
        for (let i = startPage; i <= endPage; i++) {
          pages.push(i);
        }
        if (endPage < this.totalPages - 1) pages.push("...");
        pages.push(this.totalPages);
      }

      return pages;
    },
  },
  methods: {
    setView(mode) {
      this.viewMode = mode;
    },

    toggleFilterDropdown() {
      this.isFilterDropdownVisible = !this.isFilterDropdownVisible;
    },

    setSortOption(sortBy, sortOrder) {
      if (this.sortBy !== sortBy || this.sortOrder !== sortOrder) {
        this.currentPage = 1;
        this.sortBy = sortBy;
        this.sortOrder = sortOrder;

        if (sortBy === "rating" && sortOrder === "asc") {
          this.totalPages = 20;
        }

        this.fetchAnimeByGenre();
      }
      this.isFilterDropdownVisible = false;
    },

    getSortLabel() {
      if (this.sortBy === "popularity") {
        return this.sortOrder === "desc" ? "Most Popular" : "Least Popular";
      } else if (this.sortBy === "rating") {
        return this.sortOrder === "desc" ? "Highest Rating" : "Lowest Rating";
      } else if (this.sortBy === "title") {
        return this.sortOrder === "asc" ? "Title (A-Z)" : "Title (Z-A)";
      }
      return "Most Popular";
    },

    goBack() {
      this.$emit("back");
    },

    performSearch() {
      if (this.searchTerm.trim()) {
        this.currentPage = 1;
        this.fetchAnimeByGenre();
      }
    },

    getCSRFToken() {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; csrftoken=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
      return "";
    },

    getAnimeOverview(animeId) {
      this.$emit("getAnimeOverview", animeId);
    },

    handleImgError(event) {
      event.target.onerror = null;
      event.target.src = this.placeholderImg;
    },

    formatMembers(members) {
      if (!members) return "";
      if (members >= 1000000) return (members / 1000000).toFixed(1) + "M";
      if (members >= 1000) return (members / 1000).toFixed(1) + "K";
      return members;
    },

    changePage(page) {
      if (page === "...") return;
      if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
        this.currentPage = page;

        window.scrollTo({ top: 0, behavior: "smooth" });
        this.fetchAnimeByGenre();
      }
    },

    async fetchGenreInfo() {
      try {
        const response = await fetch("https://api.jikan.moe/v4/genres/anime");
        if (!response.ok)
          throw new Error(`Failed to fetch genre info: ${response.status}`);
        const data = await response.json();
        const genre = data.data.find((g) => g.mal_id === this.genreId);
        this.genreName = genre ? genre.name : `Genre ${this.genreId}`;
      } catch (err) {
        console.error("Error fetching genre info:", err);
        this.genreName = `Genre ${this.genreId}`;
      }
    },

    async fetchAnimeByGenre() {
      this.loading = true;
      this.error = null;

      try {
        if (
          this.sortBy === "rating" &&
          this.sortOrder === "asc" &&
          this.currentPage > 20
        ) {
          this.error = "Only the lowest 500 rated anime are available.";
          return;
        }

        let orderBy = "popularity";
        if (this.sortBy === "rating") orderBy = "score";
        if (this.sortBy === "title") orderBy = "title";

        const sort = this.sortOrder === "desc" ? "desc" : "asc";
        let searchParam = this.searchTerm.trim()
          ? `&q=${encodeURIComponent(this.searchTerm.trim())}`
          : "";

        let url = `https://api.jikan.moe/v4/anime?genres=${this.genreId}&page=${this.currentPage}&limit=${this.itemsPerPage}&order_by=${orderBy}&sort=${sort}${searchParam}`;

        if (this.sortBy === "rating" && this.sortOrder === "asc") {
          const apiPage = 21 - this.currentPage;
          url = `https://api.jikan.moe/v4/anime?genres=${this.genreId}&page=${apiPage}&limit=${this.itemsPerPage}&order_by=score&sort=desc${searchParam}`;
        }

        const response = await fetch(url);
        if (!response.ok)
          throw new Error(`Failed to fetch anime: ${response.status}`);
        const data = await response.json();

        this.animeList = (data.data || []).map((anime) => ({
          id: anime.mal_id,
          title: anime.title,
          image: anime.images.jpg.image_url,
          type: anime.type || "Unknown",
          episodes: anime.episodes || "?",
          year: anime.aired?.from
            ? new Date(anime.aired.from).getFullYear()
            : "N/A",
          genres: anime.genres.map((g) => g.name),
          rating: anime.score || null,
          members: anime.members || null,
          airing: anime.airing || false,
          synopsis: anime.synopsis,
        }));

        this.totalAnime = data.pagination?.items?.total || 0;
        this.totalPages = data.pagination?.last_visible_page || 1;
      } catch (err) {
        console.error("Error fetching anime for genre:", err);
        this.error = "Failed to load anime. Please try again later.";
      } finally {
        this.loading = false;
      }
    },

    async toggleFavorite(anime) {
      console.log(`Anime:`, anime);
      if (this.favorites.has(anime.id)) {
        this.favorites.delete(anime.id);
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
              body: JSON.stringify({ name: anime.title }),
            }
          );
          const data = await response.json();
          console.log(data.message || data.error);
        } catch (error) {
          console.error("Request failed:", error);
        }
      } else {
        this.favorites.add(anime.id);
        try {
          const response = await fetch(
            "http://localhost:8000/app/favorites/add/",
            {
              method: "POST",
              credentials: "include",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": this.getCSRFToken(),
              },
              body: JSON.stringify({
                name: anime.title,
                description: anime.synopsis,
                imageURL: anime.image,
                releaseDate: anime.year?.toString(),
                genre: anime.genres,
                rating: anime.rating,
                characters: anime.characters || [],
                id: anime.id,
              }),
            }
          );
          const data = await response.json();
          console.log(data.message || data.error);
        } catch (error) {
          console.error("Request failed:", error);
        }
      }
    },

    async getFavorites() {
      try {
        const response = await fetch("http://localhost:8000/app/favorites/", {
          credentials: "include",
        });
        const data = await response.json();
        this.favorites = new Set(data.map((anime) => anime.id));
      } catch (error) {
        console.error("Failed to fetch favorites:", error);
      }
    },

    closeDropdowns(event) {
      if (!event.target.closest(".filter-dropdown")) {
        this.isFilterDropdownVisible = false;
      }
    },
  },
  async mounted() {
    await this.fetchGenreInfo();
    await this.fetchAnimeByGenre();
    this.getFavorites();
    document.addEventListener("click", this.closeDropdowns);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdowns);
  },
  watch: {
    genreId: {
      handler: async function () {
        this.currentPage = 1;
        await this.fetchGenreInfo();
        await this.fetchAnimeByGenre();
      },
    },
    sortBy() {
      this.searchTerm = "";
    },
    sortOrder() {
      this.searchTerm = "";
    },
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

.genre-detail-container {
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
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 1rem;
}

.search-container button:hover {
  background-color: #be185d;
}

.genre-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.section-title {
  color: #9333ea;
  font-size: 2rem;
  margin-bottom: 0;
}

.back-button {
  background-color: transparent;
  color: #9333ea;
  border: 1px solid #9333ea;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.back-button:hover {
  background-color: #9333ea;
  color: white;
}

.filter-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
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
  left: 0;
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

.view-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.view-toggle span {
  font-size: 1rem;
}

.view-toggle button {
  background-color: transparent;
  border: 1px solid #9333ea;
  color: #9333ea;
  padding: 0.3rem 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.view-toggle button:first-of-type {
  border-radius: 4px 0 0 4px;
}

.view-toggle button:last-of-type {
  border-radius: 0 4px 4px 0;
}

.view-toggle button.active {
  background-color: #9333ea;
  color: white;
}

.loading-container,
.error-container,
.no-results {
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

.anime-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.anime-list .anime-card {
  display: flex;
  margin-bottom: 1.5rem;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
}

.anime-list .anime-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2);
}

.anime-list .anime-image {
  width: 25%;
  min-height: 200px;
  position: relative;
  background-color: #f0f0f0;
}

.anime-list .anime-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.anime-list .anime-details {
  padding: 1.5rem;
  width: 75%;
}

.anime-list .anime-title {
  color: #9333ea;
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
}

.anime-list .anime-meta {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.anime-list .anime-meta .separator {
  display: inline-block;
  width: 4px;
  height: 4px;
  background-color: #db2777;
  border-radius: 50%;
  margin: 0 0.8rem;
}

.anime-list .anime-genres {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.anime-list .anime-description {
  color: #555;
  line-height: 1.5;
  margin-top: 0.8rem;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.anime-grid .anime-card {
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  background-color: white;
  cursor: pointer;
  position: relative;
}

.anime-grid .anime-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(147, 51, 234, 0.2);
}

.anime-grid .anime-image {
  position: relative;
  height: 280px;
  background-color: #f0f0f0;
}

.anime-grid .anime-image img {
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

.airing-badge {
  position: absolute;
  bottom: 8px;
  left: 8px;
  background-color: #9333ea;
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
}

.anime-grid .anime-details {
  padding: 1rem;
}

.anime-grid .anime-title {
  font-weight: bold;
  color: #9333ea;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.genre-tag {
  font-size: 0.75rem;
  background-color: #f3e8ff;
  color: #9333ea;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.anime-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
}

.anime-rating,
.anime-members {
  font-size: 0.875rem;
  color: #db2777;
  font-weight: 500;
}

.star-icon,
.members-icon {
  font-size: 0.875rem;
  margin-right: 0.25rem;
}

.favorite-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 6px;
  font-size: 1.2rem;
  cursor: pointer;
  z-index: 10;
  user-select: none;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.favorite-btn span {
  color: gray;
  transition: color 0.3s ease;
}

.favorite-btn span.favorited {
  color: gold;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.pagination-btn {
  background-color: white;
  border: 1px solid #9333ea;
  color: #9333ea;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #9333ea;
  color: white;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.page-number {
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-number:hover:not(.active) {
  border-color: #9333ea;
  color: #9333ea;
}

.page-number.active {
  background-color: #9333ea;
  color: white;
  border-color: #9333ea;
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

  .genre-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .filter-controls {
    flex-direction: column;
    align-items: flex-start;
  }

  .anime-list .anime-card {
    flex-direction: column;
  }

  .anime-list .anime-image {
    width: 100%;
    height: 200px;
  }

  .anime-list .anime-details {
    width: 100%;
  }

  .anime-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }

  .anime-grid .anime-image {
    height: 220px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .anime-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}
</style>
