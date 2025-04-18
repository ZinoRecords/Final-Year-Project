<template>
  <div class="container">
    <header>
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
      <h2>Highest Rated Anime</h2>

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

      <div
        :class="[
          'anime-container',
          viewMode === 'grid' ? 'grid-view' : 'list-view',
        ]"
      >
        <div v-for="anime in filteredAnime" :key="anime.id" class="anime-card">
          <div class="anime-image">
            <div
              class="favorite-btn"
              @click.stop="toggleFavorite(anime)"
              :title="favorites.has(anime.id) ? 'Unfavorite' : 'Favorite'"
            >
              <span :class="{ favorited: favorites.has(anime.id) }">★</span>
            </div>

            <img :src="anime.image" alt="anime.name" />
          </div>
          <div class="anime-details">
            <h3 class="anime-title" :title="anime.name">{{ anime.name }}</h3>

            <div v-if="viewMode === 'list'" class="anime-meta">
              <span>{{ anime.episodes }} Episodes</span>
              <span class="separator"></span>
              <span class="anime-rating">{{ anime.rating }}/10</span>
              <span class="separator"></span>
              <span>Released: {{ anime.releaseYear }}</span>
            </div>

            <div v-if="viewMode === 'list'" class="anime-description">
              {{ anime.description }}
            </div>
            <div v-else class="anime-rating">{{ anime.rating }}/10</div>
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

    async fetchAnime() {
      try {
        const response = await fetch(
          "https://api.jikan.moe/v4/top/anime?limit=25"
        );
        const { data } = await response.json();

        // Map Jikan API data to your internal format
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
        }));
      } catch (error) {
        console.error("Failed to fetch anime from Jikan:", error);
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
              credentials: "include", // include cookies for session auth
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": this.getCSRFToken(), // include CSRF token
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
        const response = await fetch(
          "http://localhost:8000/app/favorites/add/",
          {
            method: "POST",
            credentials: "include", // include cookies for session auth
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": this.getCSRFToken(), // include CSRF token
            },
            body: JSON.stringify({
              name: anime.name,
              description: anime.description,
              imageURL: anime.image,
              releaseDate: anime.releaseYear, // should be in 'YYYY-MM-DD' format
              genre: anime.genres,
              rating: anime.rating,
              characters: anime.characters || [],
              id: anime.id,
            }),
          }
        )
          .then((response) => response.json())
          .then((data) => {
            console.log(data.message || data.error);
          })
          .catch((error) => {
            console.error("Request failed:", error);
          });
      }
      console.log(this.favorites);
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

html,
body {
  height: 100%;
  font-family: "Arial", sans-serif;
}

body {
  display: flex;
  flex-direction: column;
  background-image: linear-gradient(135deg, #f8e1ff 0%, #e6e6fa 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.8);
  min-height: 100vh;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  color: #8a2be2;
  font-size: 2.5rem;
}

.search-container {
  display: flex;
  align-items: center;
}

input {
  padding: 0.5rem;
  border: 1px solid #e6e6fa;
  border-radius: 4px 0 0 4px;
  width: 250px;
}

input:focus {
  outline: none;
  border-color: #8a2be2;
}

button {
  background-color: #ff69b4;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #ff1493;
}

main {
  flex-grow: 1;
}

h2 {
  color: #8a2be2;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
}

.view-toggle {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 1.5rem;
}

.view-toggle span {
  margin-right: 0.5rem;
  font-size: 0.9rem;
}

.view-toggle button {
  background-color: transparent;
  color: #8a2be2;
  border: 1px solid #8a2be2;
  border-radius: 4px;
  padding: 0.3rem 0.8rem;
  margin-left: 0.5rem;
}

.view-toggle button.active {
  background-color: #8a2be2;
  color: white;
}

/* List View */
.list-view .anime-card {
  display: flex;
  margin-bottom: 1.5rem;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.list-view .anime-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(147, 112, 219, 0.2);
}

.list-view .anime-image {
  width: 25%;
  min-height: 200px;
  background-image: linear-gradient(135deg, #f8e1ff 0%, #e6e6fa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8a2be2;
  font-weight: 500;
}

.list-view .anime-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.list-view .anime-details {
  padding: 1.5rem;
  width: 75%;
}

.list-view .anime-title {
  color: #8a2be2;
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
}

.list-view .anime-meta {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.list-view .anime-meta .separator {
  display: inline-block;
  width: 6px;
  height: 6px;
  background-color: #ff69b4;
  border-radius: 50%;
  margin: 0 0.8rem;
}

.list-view .anime-rating {
  color: #ff69b4;
  font-weight: bold;
}

.list-view .anime-description {
  color: #555;
  line-height: 1.5;
  margin-top: 0.8rem;
}

/* Grid View */
.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.grid-view .anime-card {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.grid-view .anime-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(147, 112, 219, 0.2);
}

.grid-view .anime-image {
  height: 180px;
  background-image: linear-gradient(135deg, #f8e1ff 0%, #e6e6fa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8a2be2;
  font-weight: 500;
  position: relative;
}

.grid-view .anime-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.grid-view .anime-details {
  padding: 1rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.grid-view .anime-title {
  color: #8a2be2;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.grid-view .anime-rating {
  color: #ff69b4;
  font-weight: bold;
  font-size: 0.9rem;
}

.grid-view .anime-meta,
.grid-view .anime-description {
  display: none;
}

@media (max-width: 768px) {
  header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-container {
    width: 100%;
    margin-top: 1rem;
  }

  input {
    width: 100%;
  }

  .list-view .anime-card {
    flex-direction: column;
  }

  .list-view .anime-image {
    width: 100%;
    min-height: 150px;
  }

  .list-view .anime-details {
    width: 100%;
  }

  .grid-view {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
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
  z-index: 5;
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
</style>
