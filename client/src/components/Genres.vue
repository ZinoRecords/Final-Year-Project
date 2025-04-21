<template>
  <div>
    <div class="container">
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

        <!-- Featured -->
        <section class="anime-section">
          <h3 class="section-heading">Featured Anime</h3>
          <div class="slider-container">
            <button
              class="slider-btn prev-btn"
              @click="scrollSlider('featured', -1)"
            >
              ◀
            </button>
            <div class="anime-slider featured" ref="featured">
              <div
                class="anime-card"
                v-for="anime in featuredAnimes"
                :key="anime.id"
              >
                <div class="anime-image">
                  <img
                    :src="anime.image"
                    :alt="anime.title"
                    @error="handleImgError($event)"
                  />
                  <div class="anime-type">{{ anime.type }}</div>
                  <div v-if="anime.newEpisode" class="new-episode">
                    New Episode
                  </div>
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
                  <div class="anime-rating">{{ anime.rating }}/10</div>
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

        <!-- Genre Sections -->
        <section
          v-for="genre in genres"
          :key="genre.name"
          class="anime-section"
        >
          <div class="section-header">
            <h3 class="section-heading">{{ genre.name }}</h3>
            <a :href="`/genre/${genre.name.toLowerCase()}`" class="view-all"
              >View All</a
            >
          </div>
          <div class="slider-container">
            <button
              class="slider-btn prev-btn"
              @click="scrollSlider(genre.name.toLowerCase(), -1)"
            >
              ◀
            </button>
            <div class="anime-slider" :ref="genre.name.toLowerCase()">
              <div
                class="anime-card"
                v-for="anime in getAnimesByGenre(genre.name)"
                :key="anime.id"
              >
                <div class="anime-image">
                  <img
                    :src="anime.image"
                    :alt="anime.title"
                    @error="handleImgError($event)"
                  />
                  <div class="anime-type">{{ anime.type }}</div>
                  <div v-if="anime.newEpisode" class="new-episode">
                    New Episode
                  </div>
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
                  <div class="anime-rating">{{ anime.rating }}/10</div>
                </div>
              </div>
            </div>
            <button
              class="slider-btn next-btn"
              @click="scrollSlider(genre.name.toLowerCase(), 1)"
            >
              ▶
            </button>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: "",
      viewMode: "list",
      genres: [
        { name: "Action", id: 1 },
        { name: "Romance", id: 22 },
        { name: "Fantasy", id: 10 },
        { name: "Sci-Fi", id: 24 },
      ],
      placeholderImg:
        "https://placehold.co/320x200/8a2be2/ffffff?text=No+Image",
      genreData: {},
      featuredAnimes: [],
    };
  },
  methods: {
    performSearch() {
      const term = this.searchTerm.trim().toLowerCase();
      if (term) alert(`Searching for: ${term}`);
    },
    getAnimesByGenre(genreName) {
      return this.genreData[genreName] || [];
    },
    scrollSlider(refName, direction) {
      let slider = this.$refs[refName];

      // If the ref is an array (e.g., multiple v-for refs), get the first one
      if (Array.isArray(slider)) {
        slider = slider[0];
      }

      if (slider) {
        const scrollAmount = direction * (slider.clientWidth * 0.8);
        slider.scrollBy({ left: scrollAmount, behavior: "smooth" });
      }
    },

    handleImgError(event) {
      event.target.onerror = null;
      event.target.src = this.placeholderImg;
    },
    async fetchGenreAnimes(genre) {
      try {
        const response = await fetch(
          `https://api.jikan.moe/v4/anime?genres=${genre.id}&limit=10&order_by=popularity`
        );
        const data = await response.json();
        this.genreData[genre.name] = data.data.map((anime) => ({
          id: anime.mal_id,
          title: anime.title,
          image: anime.images.jpg.image_url,
          type: anime.type,
          episodes: anime.episodes || "N/A",
          year: anime.aired?.from
            ? new Date(anime.aired.from).getFullYear()
            : "N/A",
          genres: anime.genres.map((g) => g.name),
          rating: anime.score || "N/A",
          newEpisode: false,
        }));
      } catch (error) {
        console.error(`Error fetching anime for genre ${genre.name}:`, error);
      }
    },
    async fetchFeaturedAnimes() {
      try {
        const response = await fetch(
          `https://api.jikan.moe/v4/top/anime?limit=10`
        );
        const data = await response.json();
        this.featuredAnimes = data.data.map((anime) => ({
          id: anime.mal_id,
          title: anime.title,
          image: anime.images.jpg.image_url,
          type: anime.type,
          episodes: anime.episodes || "N/A",
          year: anime.aired?.from
            ? new Date(anime.aired.from).getFullYear()
            : "N/A",
          genres: anime.genres.map((g) => g.name),
          rating: anime.score || "N/A",
          newEpisode: false,
        }));
      } catch (error) {
        console.error("Error fetching featured animes:", error);
      }
    },
  },
  async mounted() {
    await this.fetchFeaturedAnimes();
    for (const genre of this.genres) {
      await delay(700);
      await this.fetchGenreAnimes(genre);
    }
  },
};
function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
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

/* Navbar */
.navbar {
  background-color: #8a2be2;
  padding: 1rem 0;
  color: white;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  padding: 0 1rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #ffb6c1;
}

.nav-links a.active {
  font-weight: 600;
}

.logout {
  color: #ffb6c1;
  text-decoration: none;
  font-weight: 500;
}

/* Main Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

/* Header */
.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

h1 {
  color: #8a2be2;
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
  background-color: #ec4899;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 1rem;
}

.search-container button:hover {
  background-color: #d53f8c;
}

/* Section Titles */
.section-title {
  color: #8a2be2;
  font-size: 2rem;
  text-align: center;
  margin-bottom: 2rem;
}

.section-heading {
  color: #8a2be2;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

/* View Controls */
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
  border: 1px solid #8a2be2;
  color: #8a2be2;
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
  background-color: #8a2be2;
  color: white;
}

/* Anime Sections */
.anime-section {
  margin-bottom: 3rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.view-all {
  color: #ec4899;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.view-all:hover {
  color: #8a2be2;
}

/* Slider */
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
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.anime-slider::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.anime-card {
  flex-shrink: 0;
  width: 220px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  background-color: white;
}

.anime-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.2);
}

.featured .anime-card {
  width: 280px;
}

.anime-image {
  position: relative;
  height: 140px;
  background-color: #f0f0f0;
}

.featured .anime-image {
  height: 180px;
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
  background-color: #ec4899;
  color: white;
  font-size: 0.75rem;
  font-weight: bold;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.new-episode {
  position: absolute;
  bottom: 8px;
  left: 8px;
  background-color: #8a2be2;
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
  color: #8a2be2;
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
  background-color: #ec4899;
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
  color: #8a2be2;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.anime-rating {
  color: #ec4899;
  font-weight: bold;
  margin-top: 0.5rem;
}

.slider-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: #8a2be2;
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

/* Responsive */
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

  .anime-card {
    width: 180px;
  }

  .featured .anime-card {
    width: 220px;
  }
}
</style>
