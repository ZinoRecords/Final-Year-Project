<template>
  <div class="genres-container">
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
      <h2 class="section-title">Anime Genres</h2>

      <div class="view-controls">
        <div class="view-toggle">
          <span>View:</span>
          <button
            :class="{ active: viewMode === 'list' }"
            @click="viewMode = 'list'"
          >
            List
          </button>
          <button
            :class="{ active: viewMode === 'grid' }"
            @click="viewMode = 'grid'"
          >
            Grid
          </button>
        </div>
      </div>

      <div v-if="loading" class="loading-container">
        <div class="loading-spinner"></div>
        <p>Loading genres...</p>
      </div>

      <div v-else-if="error" class="error-container">
        <p>{{ error }}</p>
        <button @click="fetchGenres" class="retry-button">Try Again</button>
      </div>

      <section v-else-if="viewMode === 'grid'" class="genres-grid-section">
        <div class="genres-grid">
          <div
            v-for="genre in sortedGenres"
            :key="genre.id"
            class="genre-card"
            @click="selectGenre(genre)"
          >
            <div class="genre-name">{{ genre.name }}</div>
            <div class="genre-count" v-if="genre.count">
              {{ genre.count }}+ anime
            </div>
          </div>
        </div>
      </section>

      <template v-else>
        <section class="anime-section" v-if="featuredAnimes.length > 0">
          <div class="section-header">
            <h3 class="section-heading">Featured Anime</h3>
            <span class="count-badge">{{ featuredAnimes.length }}</span>
          </div>
          <div class="slider-container">
            <button
              class="slider-btn prev-btn"
              @click="scrollSlider('featured', -1)"
            >
              ◀
            </button>
            <div class="anime-slider" ref="featured">
              <div
                class="anime-card"
                v-for="anime in featuredAnimes"
                :key="anime.id"
                @click="getAnimeOverview(anime.id)"
              >
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
                  <h4 class="anime-title">{{ anime.title }}</h4>
                  <div class="anime-meta">
                    <span>{{ anime.year }}</span>
                    <span class="separator"></span>
                    <span>{{ anime.episodes }} eps</span>
                  </div>
                  <div class="anime-genres">
                    <span
                      class="genre-tag"
                      v-for="(genre, index) in anime.genres.slice(0, 2)"
                      :key="index"
                    >
                      {{ genre }}
                    </span>
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
            <button
              class="slider-btn next-btn"
              @click="scrollSlider('featured', 1)"
            >
              ▶
            </button>
          </div>
        </section>

        <section
          v-for="genre in displayedGenres"
          :key="genre.id"
          class="anime-section"
        >
          <div class="section-header">
            <h3 class="section-heading">{{ genre.name }}</h3>
            <div class="section-actions">
              <span
                class="count-badge"
                v-if="getAnimesByGenre(genre.id).length"
              >
                {{ getAnimesByGenre(genre.id).length }}
              </span>
              <button class="view-all-btn" @click="selectGenre(genre.id)">
                View All
              </button>
            </div>
          </div>
          <div class="slider-container">
            <button
              class="slider-btn prev-btn"
              @click="scrollSlider(`genre-${genre.id}`, -1)"
            >
              ◀
            </button>
            <div class="anime-slider" :ref="`genre-${genre.id}`">
              <div
                class="anime-card"
                v-for="anime in getAnimesByGenre(genre.id)"
                :key="anime.id"
                @click="getAnimeOverview(anime.id)"
              >
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
                  <h4 class="anime-title">{{ anime.title }}</h4>
                  <div class="anime-meta">
                    <span>{{ anime.year }}</span>
                    <span class="separator"></span>
                    <span>{{ anime.episodes }} eps</span>
                  </div>
                  <div class="anime-genres">
                    <span
                      class="genre-tag"
                      v-for="(genre, index) in anime.genres.slice(0, 2)"
                      :key="index"
                    >
                      {{ genre }}
                    </span>
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
            <button
              class="slider-btn next-btn"
              @click="scrollSlider(`genre-${genre.id}`, 1)"
            >
              ▶
            </button>
          </div>
        </section>
      </template>

      <div v-if="selectedGenre" class="selected-genre-overlay">
        <div class="selected-genre-content">
          <div class="selected-genre-header">
            <h3>{{ selectedGenre.name }} Anime</h3>
            <button class="close-btn" @click="selectedGenre = null">×</button>
          </div>

          <div v-if="loadingGenreAnime" class="loading-container">
            <div class="loading-spinner"></div>
            <p>Loading anime...</p>
          </div>

          <div v-else-if="genreAnimeError" class="error-container">
            <p>{{ genreAnimeError }}</p>
            <button
              @click="fetchAnimeByGenre(selectedGenre.id)"
              class="retry-button"
            >
              Try Again
            </button>
          </div>

          <div v-else class="genre-anime-grid">
            <div
              v-for="anime in selectedGenreAnime"
              :key="anime.id"
              class="anime-card"
              @click="getAnimeOverview(anime.id)"
            >
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
                <h4 class="anime-title">{{ anime.title }}</h4>
                <div class="anime-meta">
                  <span>{{ anime.year }}</span>
                  <span class="separator"></span>
                  <span>{{ anime.episodes }} eps</span>
                </div>
                <div class="anime-genres">
                  <span
                    class="genre-tag"
                    v-for="(genre, index) in anime.genres.slice(0, 2)"
                    :key="index"
                  >
                    {{ genre }}
                  </span>
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
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "Genres",
  data() {
    return {
      searchTerm: "",
      viewMode: "list",
      loading: true,
      error: null,

      genres: [],
      animesByGenre: {},
      featuredAnimes: [],

      selectedGenre: null,
      selectedGenreAnime: [],
      loadingGenreAnime: false,
      genreAnimeError: null,

      genresPerPage: 4,
      placeholderImg:
        "https://placehold.co/320x200/9333ea/ffffff?text=No+Image",
    };
  },

  computed: {
    sortedGenres() {
      return [...this.genres].sort((a, b) => a.name.localeCompare(b.name));
    },

    displayedGenres() {
      // Return a subset of genres for the list view
      return this.genres.slice(0, this.genresPerPage);
    },
  },

  methods: {
    performSearch() {
      const query = this.searchTerm.trim();
      if (query) {
        this.$emit("search", query);
      }
    },

    getAnimesByGenre(genreId) {
      return this.animesByGenre[genreId] || [];
    },

    scrollSlider(refName, direction) {
      let slider = this.$refs[refName];
      if (Array.isArray(slider)) slider = slider[0];

      if (slider) {
        slider.scrollBy({
          left: direction * (slider.clientWidth * 0.8),
          behavior: "smooth",
        });
      }
    },

    handleImgError(event) {
      event.target.onerror = null;
      event.target.src = this.placeholderImg;
    },

    getAnimeOverview(animeId) {
      this.$emit("getAnimeOverview", animeId);
    },

    formatMembers(members) {
      if (members >= 1000000) {
        return (members / 1000000).toFixed(1) + "M";
      } else if (members >= 1000) {
        return (members / 1000).toFixed(1) + "K";
      }
      return members;
    },

    selectGenre(genreID) {
      console.log(`emitted genreID: ${genreID}`);
      this.$emit("getGenrePage", genreID);
    },

    async fetchGenres() {
      this.loading = true;
      this.error = null;

      try {
        const response = await fetch("https://api.jikan.moe/v4/genres/anime");

        if (!response.ok) {
          throw new Error(`Failed to fetch genres: ${response.status}`);
        }

        const data = await response.json();

        this.genres = (data.data || []).map((genre) => ({
          id: genre.mal_id,
          name: genre.name,
          count: genre.count,
        }));

        await this.fetchFeaturedAnimes();

        for (const genre of this.displayedGenres) {
          await this.delay(700);
          await this.fetchGenreAnimes(genre);
        }
      } catch (err) {
        console.error("Error fetching genres:", err);
        this.error = "Failed to load genres. Please try again later.";
      } finally {
        this.loading = false;
      }
    },

    async fetchGenreAnimes(genre) {
      try {
        const response = await fetch(
          `https://api.jikan.moe/v4/anime?genres=${genre.id}&limit=10&order_by=popularity`
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch anime for genre ${genre.name}`);
        }

        const data = await response.json();

        this.animesByGenre[genre.id] = (data.data || []).map((anime) => ({
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
        }));
      } catch (err) {
        console.error(`Failed to load anime for ${genre.name}:`, err);
      }
    },

    async fetchFeaturedAnimes() {
      try {
        const response = await fetch(
          "https://api.jikan.moe/v4/top/anime?limit=10"
        );

        if (!response.ok) {
          throw new Error("Failed to fetch featured anime");
        }

        const data = await response.json();

        this.featuredAnimes = (data.data || []).map((anime) => ({
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
        }));
      } catch (err) {
        console.error("Failed to load featured anime:", err);
      }
    },

    async fetchAnimeByGenre(genreId) {
      this.loadingGenreAnime = true;
      this.genreAnimeError = null;
      this.selectedGenreAnime = [];

      try {
        const response = await fetch(
          `https://api.jikan.moe/v4/anime?genres=${genreId}&limit=24&order_by=popularity`
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch anime for this genre`);
        }

        const data = await response.json();

        this.selectedGenreAnime = (data.data || []).map((anime) => ({
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
        }));
      } catch (err) {
        console.error("Error fetching anime for genre:", err);
        this.genreAnimeError = "Failed to load anime. Please try again later.";
      } finally {
        this.loadingGenreAnime = false;
      }
    },

    delay(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
  },

  async mounted() {
    await this.fetchGenres();
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
  background-color: #ffffff;
  color: #333;
}

.genres-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
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

.section-heading {
  color: #9333ea;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.view-controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 2rem;
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
.error-container {
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

.genres-grid-section {
  margin-bottom: 3rem;
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.genre-card {
  background-color: white;
  border: 1px solid #f3e8ff;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.genre-card:hover {
  background-color: #f3e8ff;
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(147, 51, 234, 0.15);
}

.genre-name {
  color: #9333ea;
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

.genre-count {
  color: #db2777;
  font-size: 0.8rem;
  font-weight: 500;
}

.anime-section {
  margin-bottom: 3rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.count-badge {
  background-color: #db2777;
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
}

.view-all-btn {
  color: #9333ea;
  background: none;
  border: none;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.3s;
  padding: 0.25rem 0.5rem;
}

.view-all-btn:hover {
  color: #db2777;
  text-decoration: underline;
}

.slider-container {
  position: relative;
  padding: 0 2rem;
}

.anime-slider {
  display: flex;
  overflow-x: auto;
  gap: 1rem;
  padding: 0.5rem 0;
  scroll-behavior: smooth;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.anime-slider::-webkit-scrollbar {
  display: none;
}

.anime-card {
  flex-shrink: 0;
  width: 200px;
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
  display: flex;
  align-items: center;
  font-size: 0.875rem;
  color: #666;
}

.anime-meta .separator {
  display: inline-block;
  width: 4px;
  height: 4px;
  background-color: #db2777;
  border-radius: 50%;
  margin: 0 0.5rem;
}

.anime-genres {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
  margin-top: 0.5rem;
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

.slider-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: #9333ea;
  color: white;
  border: none;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.3s;
  z-index: 2;
}

.slider-btn:hover {
  opacity: 1;
}

.prev-btn {
  left: 0;
}

.next-btn {
  right: 0;
}

.selected-genre-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.75);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  overflow-y: auto;
}

.selected-genre-content {
  background-color: white;
  border-radius: 8px;
  width: 100%;
  max-width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 1.5rem;
}

.selected-genre-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f3e8ff;
}

.selected-genre-header h3 {
  color: #9333ea;
  font-size: 1.5rem;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 1.5rem;
  cursor: pointer;
  transition: color 0.3s;
}

.close-btn:hover {
  color: #db2777;
}

.genre-anime-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
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

  .view-controls {
    justify-content: center;
  }

  .genres-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .anime-card {
    width: 160px;
  }

  .anime-image {
    height: 220px;
  }

  .genre-anime-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .selected-genre-content {
    padding: 1rem;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .genres-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }

  .genre-anime-grid {
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  }
}
</style>
