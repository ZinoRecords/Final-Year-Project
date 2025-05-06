<template>
  <div class="top-anime-container">
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
      <h2 class="section-title">Highest Rated Anime</h2>

      <div class="view-controls">
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
        <button @click="fetchAnime" class="retry-button">Try Again</button>
      </div>

      <div
        v-else
        :class="[
          'anime-container',
          viewMode === 'grid' ? 'anime-grid' : 'anime-list',
        ]"
      >
        <div
          v-for="anime in filteredAnime"
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
              :alt="anime.name"
              @error="handleImgError($event)"
            />
            <div class="anime-type">{{ anime.type || "TV" }}</div>
          </div>
          <div class="anime-details">
            <h3 class="anime-title" :title="anime.name">{{ anime.name }}</h3>

            <div v-if="viewMode === 'list'" class="anime-meta">
              <span>{{ anime.episodes }} Episodes</span>
              <span class="separator"></span>
              <span>Released: {{ anime.releaseYear }}</span>
            </div>

            <div v-if="viewMode === 'list'" class="anime-description">
              {{ anime.description }}
            </div>

            <div class="anime-stats">
              <div class="anime-rating">
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
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: "",
      viewMode: "list",
      animeData: [],
      favorites: new Set(),
      loading: true,
      error: null,
      placeholderImg:
        "https://placehold.co/320x200/9333ea/ffffff?text=No+Image",
    };
  },
  computed: {
    filteredAnime() {
      const search = this.searchTerm.toLowerCase().trim();
      if (!search) return this.animeData;
      return this.animeData.filter(
        (anime) =>
          anime.name.toLowerCase().includes(search) ||
          anime.description.toLowerCase().includes(search)
      );
    },
  },
  methods: {
    setView(mode) {
      this.viewMode = mode;
    },

    getCSRFToken() {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; csrftoken=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
      return "";
    },

    getAnimeOverview(animeID) {
      this.$emit("getAnimeOverview", animeID);
    },

    handleImgError(event) {
      event.target.onerror = null;
      event.target.src = this.placeholderImg;
    },

    formatMembers(members) {
      if (!members) return "";
      if (members >= 1000000) {
        return (members / 1000000).toFixed(1) + "M";
      } else if (members >= 1000) {
        return (members / 1000).toFixed(1) + "K";
      }
      return members;
    },

    async fetchAnime() {
      this.loading = true;
      this.error = null;

      try {
        const response = await fetch(
          "https://api.jikan.moe/v4/top/anime?limit=25"
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch anime: ${response.status}`);
        }

        const { data } = await response.json();

        this.animeData = data.map((item, index) => ({
          id: item.mal_id || index,
          name: item.title,
          episodes: item.episodes || "N/A",
          rating: item.score || "N/A",
          releaseYear: item.year || "Unknown",
          description: item.synopsis || "No description available.",
          image:
            item.images.webp?.image_url || item.images.jpg?.image_url || "",
          genres: item.genres?.map((genre) => genre.name) || [],
          type: item.type || "TV",
          members: item.members || null,
        }));
      } catch (error) {
        console.error("Failed to fetch anime from Jikan:", error);
        this.error = "Failed to load anime. Please try again later.";
      } finally {
        this.loading = false;
      }
    },

    async toggleFavorite(anime) {
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
              body: JSON.stringify({
                name: anime.name,
              }),
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
                name: anime.name,
                description: anime.description,
                imageURL: anime.image,
                releaseDate: anime.releaseYear,
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
  },
  mounted() {
    this.fetchAnime();
    this.getFavorites();
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

.top-anime-container {
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

.anime-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.anime-list .anime-card {
  display: flex;
  margin-bottom: 1.5rem;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
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

.anime-list .anime-description {
  color: #555;
  line-height: 1.5;
  margin-top: 0.8rem;
  margin-bottom: 1rem;
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

@media (max-width: 768px) {
  .main-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-container {
    width: 100%;
    margin-top: 1rem;
  }

  .anime-list .anime-card {
    flex-direction: column;
    position: relative;
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
