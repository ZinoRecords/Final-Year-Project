<template>
  <div class="new-releases-container">
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
      <h2 class="section-title">New Releases</h2>

      <div class="season-selector">
        <div class="season-controls">
          <span>Season:</span>
          <select v-model="selectedYear" @change="fetchSeasonAnime">
            <option v-for="year in availableYears" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
          <select v-model="selectedSeason" @change="fetchSeasonAnime">
            <option v-for="season in seasons" :key="season" :value="season">
              {{ season.charAt(0).toUpperCase() + season.slice(1) }}
            </option>
          </select>
        </div>

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
        <p>Loading anime...</p>
      </div>

      <div v-else-if="error" class="error-container">
        <p>{{ error }}</p>
        <button @click="fetchSeasonAnime" class="retry-button">
          Try Again
        </button>
      </div>

      <div v-else-if="viewMode === 'grid'" class="anime-grid">
        <div
          v-for="anime in seasonAnime"
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
              <span>{{ anime.episodes }} eps</span>
              <span v-if="anime.startDate" class="separator"></span>
              <span v-if="anime.startDate">{{
                formatDate(anime.startDate)
              }}</span>
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

      <div v-else class="anime-categories">
        <section v-if="getTVAnime.length" class="anime-section">
          <div class="section-header">
            <h3 class="section-heading">TV Shows</h3>
            <span class="count-badge">{{ getTVAnime.length }}</span>
          </div>
          <div class="slider-container">
            <button
              class="slider-btn prev-btn"
              @click="scrollSlider('tv-slider', -1)"
            >
              ◀
            </button>
            <div class="anime-slider" ref="tv-slider">
              <div
                v-for="anime in getTVAnime"
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
                    <span>{{ anime.episodes }} eps</span>
                    <span v-if="anime.startDate" class="separator"></span>
                    <span v-if="anime.startDate">{{
                      formatDate(anime.startDate)
                    }}</span>
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
              @click="scrollSlider('tv-slider', 1)"
            >
              ▶
            </button>
          </div>
        </section>

        <section v-if="getMovieAnime.length" class="anime-section">
          <div class="section-header">
            <h3 class="section-heading">Movies</h3>
            <span class="count-badge">{{ getMovieAnime.length }}</span>
          </div>
          <div class="slider-container">
            <button
              class="slider-btn prev-btn"
              @click="scrollSlider('movie-slider', -1)"
            >
              ◀
            </button>
            <div class="anime-slider" ref="movie-slider">
              <div
                v-for="anime in getMovieAnime"
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
                </div>
                <div class="anime-details">
                  <h4 class="anime-title">{{ anime.title }}</h4>
                  <div class="anime-meta">
                    <span v-if="anime.startDate">{{
                      formatDate(anime.startDate)
                    }}</span>
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
              @click="scrollSlider('movie-slider', 1)"
            >
              ▶
            </button>
          </div>
        </section>

        <section v-if="getOVAAnime.length" class="anime-section">
          <div class="section-header">
            <h3 class="section-heading">OVAs</h3>
            <span class="count-badge">{{ getOVAAnime.length }}</span>
          </div>
          <div class="slider-container">
            <button
              class="slider-btn prev-btn"
              @click="scrollSlider('ova-slider', -1)"
            >
              ◀
            </button>
            <div class="anime-slider" ref="ova-slider">
              <div
                v-for="anime in getOVAAnime"
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
                </div>
                <div class="anime-details">
                  <h4 class="anime-title">{{ anime.title }}</h4>
                  <div class="anime-meta">
                    <span>{{ anime.episodes }} eps</span>
                    <span v-if="anime.startDate" class="separator"></span>
                    <span v-if="anime.startDate">{{
                      formatDate(anime.startDate)
                    }}</span>
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
              @click="scrollSlider('ova-slider', 1)"
            >
              ▶
            </button>
          </div>
        </section>

        <section v-if="getOtherAnime.length" class="anime-section">
          <div class="section-header">
            <h3 class="section-heading">Other</h3>
            <span class="count-badge">{{ getOtherAnime.length }}</span>
          </div>
          <div class="slider-container">
            <button
              class="slider-btn prev-btn"
              @click="scrollSlider('other-slider', -1)"
            >
              ◀
            </button>
            <div class="anime-slider" ref="other-slider">
              <div
                v-for="anime in getOtherAnime"
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
                </div>
                <div class="anime-details">
                  <h4 class="anime-title">{{ anime.title }}</h4>
                  <div class="anime-meta">
                    <span>{{ anime.episodes }} eps</span>
                    <span v-if="anime.startDate" class="separator"></span>
                    <span v-if="anime.startDate">{{
                      formatDate(anime.startDate)
                    }}</span>
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
              @click="scrollSlider('other-slider', 1)"
            >
              ▶
            </button>
          </div>
        </section>
      </div>

      <div
        v-if="!loading && !error && seasonAnime.length === 0"
        class="no-results"
      >
        <p>No anime found for this season. Try selecting a different season.</p>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "NewReleases",
  data() {
    return {
      searchTerm: "",
      viewMode: "list",
      loading: true,
      error: null,

      currentYear: new Date().getFullYear(),
      currentSeason: this.getCurrentSeason(),
      selectedYear: new Date().getFullYear(),
      selectedSeason: this.getCurrentSeason(),
      seasons: ["winter", "spring", "summer", "fall"],

      seasonAnime: [],
      placeholderImg:
        "https://placehold.co/320x200/9333ea/ffffff?text=No+Image",
    };
  },

  computed: {
    availableYears() {
      const years = [];
      for (let year = 2000; year <= this.currentYear + 1; year++) {
        years.push(year);
      }
      return years.reverse();
    },

    getTVAnime() {
      return this.seasonAnime.filter((anime) => anime.type === "TV");
    },

    getMovieAnime() {
      return this.seasonAnime.filter((anime) => anime.type === "Movie");
    },

    getOVAAnime() {
      return this.seasonAnime.filter(
        (anime) => anime.type === "OVA" || anime.type === "ONA"
      );
    },

    getOtherAnime() {
      return this.seasonAnime.filter(
        (anime) => !["TV", "Movie", "OVA", "ONA"].includes(anime.type)
      );
    },
  },

  methods: {
    getCurrentSeason() {
      const month = new Date().getMonth();
      if (month >= 0 && month <= 2) return "winter";
      if (month >= 3 && month <= 5) return "spring";
      if (month >= 6 && month <= 8) return "summer";
      return "fall";
    },

    performSearch() {
      const query = this.searchTerm.trim();
      if (query) {
        this.$emit("search", query);
      }
    },

    async fetchSeasonAnime() {
      this.loading = true;
      this.error = null;
      this.seasonAnime = [];

      try {
        await this.delay(300);

        const url = `https://api.jikan.moe/v4/seasons/${this.selectedYear}/${this.selectedSeason}`;
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`Failed to fetch data: ${response.status}`);
        }

        const data = await response.json();

        this.seasonAnime = (data.data || []).map((anime) => ({
          id: anime.mal_id,
          title: anime.title,
          image: anime.images.jpg.image_url,
          type: anime.type || "Unknown",
          episodes: anime.episodes || "?",
          startDate: anime.aired?.from || null,
          genres: anime.genres?.map((g) => g.name) || [],
          rating: anime.score || null,
          members: anime.members || null,
          airing: anime.airing || false,
        }));

        this.seasonAnime.sort((a, b) => (b.members || 0) - (a.members || 0));
      } catch (err) {
        console.error("Error fetching season anime:", err);
        this.error = "Failed to load anime. Please try again later.";
      } finally {
        this.loading = false;
      }
    },

    scrollSlider(refName, direction) {
      const slider = this.$refs[refName];
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

    formatDate(dateString) {
      if (!dateString) return "TBA";
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
    },

    formatMembers(members) {
      if (members >= 1000000) {
        return (members / 1000000).toFixed(1) + "M";
      } else if (members >= 1000) {
        return (members / 1000).toFixed(1) + "K";
      }
      return members;
    },

    delay(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
  },

  async mounted() {
    await this.fetchSeasonAnime();
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

.new-releases-container {
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

.season-selector {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.season-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.season-controls span {
  font-weight: 500;
}

.season-controls select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  font-size: 1rem;
  cursor: pointer;
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
  margin-bottom: 3rem;
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

.count-badge {
  background-color: #db2777;
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 999px;
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

@media (max-width: 768px) {
  .main-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-container {
    width: 100%;
    margin-top: 1rem;
  }

  .season-selector {
    flex-direction: column;
    align-items: flex-start;
  }

  .view-toggle {
    margin-top: 0.5rem;
  }

  .anime-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }

  .anime-card {
    width: 160px;
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
