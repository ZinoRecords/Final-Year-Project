<template>
  <div class="container">
    <header class="main-header">
      <div class="header-content">
        <button class="back-button" @click="handleBack">
          <span class="back-icon">◀</span>
          <span @click="prevPage">Back</span>
        </button>
        <h1>AnimeWorld</h1>
      </div>

      <div class="search-container">
        <input type="text" placeholder="Search anime..." id="searchInput" />
        <button id="searchBtn">🔍</button>
      </div>
    </header>

    <main>
      <h2 class="section-title">Anime Overview</h2>

      <div class="anime-overview">
        <div class="anime-header">
          <div class="anime-image-container">
            <div
              v-if="animeData.imageURL.includes('placeholder')"
              class="image-placeholder"
            >
              Insert Image
            </div>

            <!-- Image of anime -->
            <img
              v-else
              :src="animeData.imageURL"
              :alt="animeData.name"
              class="anime-cover-image"
            />
          </div>

          <div class="anime-info">
            <h3 class="anime-title">{{ animeData.name }}</h3>

            <!-- Favorite Button  -->
            <button
              class="favorite-button"
              @click="toggleFavorite(animeData)"
              :class="{ 'is-favorite': isFavorite(animeData.id) }"
              :aria-label="
                isFavorite(animeData.id)
                  ? 'Remove from favorites'
                  : 'Add to favorites'
              "
            >
              <span class="favorite-icon">♥</span>
              <span class="favorite-text">
                {{
                  isFavorite(animeData.id)
                    ? "Remove from favorites"
                    : "Add to favorites"
                }}
              </span>
            </button>

            <!-- Anime Details -->
            <div class="anime-meta-grid">
              <div class="meta-item">
                <span class="meta-label">ID</span>
                <span class="meta-value">{{ animeData.id }}</span>
              </div>

              <div class="meta-item">
                <span class="meta-label">Release Date</span>
                <span class="meta-value">{{ formattedDate }}</span>
              </div>

              <div class="meta-item">
                <span class="meta-label">Genre</span>
                <div class="genre-tags">
                  <span
                    v-for="(genre, index) in genreList"
                    :key="index"
                    class="genre-tag"
                  >
                    {{ genre }}
                  </span>
                </div>
              </div>

              <div class="meta-item">
                <span class="meta-label">Rating</span>
                <div class="rating-display">
                  <span class="rating-value">{{ animeData.rating }}/10</span>
                  <div class="rating-stars">
                    <div
                      v-for="(star, index) in stars"
                      :key="index"
                      :class="['star', star.type]"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Anime description -->
        <section class="anime-section">
          <h3 class="section-heading">Description</h3>
          <p class="anime-description">{{ animeData.description }}</p>
        </section>

        <!-- Characters -->
        <section class="anime-section">
          <div class="section-header">
            <h3 class="section-heading">Characters</h3>
            <a href="#" class="view-all">View All</a>
          </div>

          <div class="slider-container">
            <button
              class="slider-btn prev-btn"
              @click="handleSlide('characters', -1)"
            >
              ◀
            </button>
            <div
              class="anime-slider characters-slider"
              ref="charactersSliderRef"
            >
              <!-- Character -->
              <div
                v-for="character in animeData.characters"
                :key="character.id"
                class="character-card"
              >
                <div class="character-image">
                  <div
                    v-if="character.image.includes('placeholder')"
                    class="image-placeholder small"
                  >
                    Insert Image
                  </div>
                  <img
                    v-else
                    :src="character.image"
                    :alt="character.name"
                    class="character-avatar"
                  />
                </div>
                <div class="character-details">
                  <h4 class="character-name">{{ character.name }}</h4>
                  <span class="character-role">{{ character.role }}</span>
                  <p class="character-description">
                    {{ character.description }}
                  </p>
                </div>
              </div>
            </div>
            <button
              class="slider-btn next-btn"
              @click="handleSlide('characters', 1)"
            >
              ▶
            </button>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "AnimeOverview",

  props: {
    animeID: {
      type: Number,
      required: true,
    },
  },

  data() {
    return {
      animeData: {
        id: null,
        name: "",
        description: "",
        imageURL: "",
        releaseDate: "",
        genre: "",
        rating: 0,
        characters: [],
      },

      formattedDate: "",
      genreList: [],
      stars: [],
      placeholderImg: "https://placehold.co/300x400?text=No+Image",
      favorites: new Set(),
    };
  },

  methods: {
    isFavorite(animeId) {
      return this.favorites.has(animeId);
    },

    getCSRFToken() {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; csrftoken=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
      return "";
    },

    // Favorite and unfavorite animes
    async toggleFavorite(anime) {
      if (this.favorites.has(anime.id)) {
        // Remove from favorites on page
        this.favorites.delete(anime.id);
        // Remove from favorites on database
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
              body: JSON.stringify({ name: anime.name }),
            }
          );
          const data = await response.json();
          console.log(data.message || data.error);
        } catch (error) {
          console.error("Request failed:", error);
        }
      } else {
        // Add to favorites
        this.favorites.add(anime.id);
        // Add to database
        try {
          console.log(anime);
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
                imageURL: anime.imageURL,
                releaseDate: anime.releaseDate.slice(0, 10),
                genre: this.genreList.join(", "),
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

    // Make the star design, rounds to nearest half
    generateStarsFromRating(rating) {
      const stars = [];
      const scaledRating = (rating / 10) * 5;
      const max = Math.floor(scaledRating);
      const half = scaledRating % 1 >= 0.5;

      for (let i = 0; i < max; i++) stars.push({ type: "filled" });
      if (half) stars.push({ type: "half" });
      for (let i = stars.length; i < 5; i++) stars.push({ type: "" });

      return stars;
    },

    // Get stars
    generateStars() {
      this.stars = this.generateStarsFromRating(this.animeData.rating);
    },

    // Slider
    handleSlide(direction) {
      const slider = this.$refs.charactersSliderRef;
      if (slider) {
        const scrollAmount = direction * (slider.clientWidth * 0.8);
        slider.scrollBy({ left: scrollAmount, behavior: "smooth" });
      }
    },

    // Get full date for anime release
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return isNaN(date)
        ? "Unknown"
        : date.toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
          });
    },

    // Go back to previous page
    prevPage() {
      this.$emit("goBack");
    },

    // Get anime details
    async fetchAnimeOverview(id) {
      try {
        const animeRes = await fetch(`https://api.jikan.moe/v4/anime/${id}`);
        const animeData = await animeRes.json();

        if (!animeData.data) throw new Error("Anime not found");

        const anime = animeData.data;

        this.animeData.id = anime.mal_id;
        this.animeData.name = anime.title;
        this.animeData.description =
          anime.synopsis || "No description available.";
        this.animeData.imageURL =
          anime.images?.jpg?.image_url || this.placeholderImg;
        this.animeData.releaseDate = anime.aired?.from || "";
        this.animeData.genre = anime.genres.map((g) => g.name).join(", ");
        this.animeData.rating = anime.score || 0;

        this.formattedDate = this.formatDate(this.animeData.releaseDate);
        this.genreList = anime.genres.map((g) => g.name);

        this.generateStars();

        // Character info has to be fetched separately
        const charRes = await fetch(
          `https://api.jikan.moe/v4/anime/${id}/characters`
        );
        const charData = await charRes.json();

        this.animeData.characters = (charData.data || [])
          .slice(0, 6)
          .map((c) => ({
            id: c.character.mal_id,
            name: c.character.name,
            image: c.character.images?.jpg?.image_url || this.placeholderImg,
            role: c.role,
            description: "",
          }));
      } catch (err) {
        console.error("Failed to fetch anime overview:", err);
      }
    },

    // Get users favorites
    async getFavorites() {
      try {
        const response = await fetch("http://localhost:8000/app/favorites/", {
          credentials: "include",
        });
        const data = await response.json();
        this.favorites = new Set(data.map((anime) => anime.id));
      } catch (error) {
        console.error("Failed to fetch favorites:", error);
        this.favorites = new Set();
      }
    },

    // Goes back to whichever page we came from
    handleBack() {
      this.prevPage();
    },
  },

  mounted() {
    this.fetchAnimeOverview(this.animeID);
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
  background-color: #ffffff;
  color: #333;
}

.container {
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

.header-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Back button */
.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: transparent;
  border: none;
  color: #8a2be2;
  font-weight: 500;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.back-button:hover {
  background-color: rgba(138, 43, 226, 0.1);
}

.back-icon {
  font-size: 0.8rem;
}

h1 {
  color: #8a2be2;
  font-size: 2.5rem;
  margin-bottom: 0;
}

/* Search bar  */
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

/* Section Title */
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

/* Subheader */
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

/* Anime Info */
.anime-overview {
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.anime-header {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  padding: 2rem;
  background: linear-gradient(to right, #8a2be2, #4a00e0);
  color: white;
}

/* Larger screen adjustments */
@media (min-width: 768px) {
  .anime-header {
    flex-direction: row;
  }
}

/* Image */
.anime-image-container {
  flex-shrink: 0;
  width: 100%;
  max-width: 300px;
  height: 400px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  position: relative;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .anime-image-container {
    margin: 0;
  }
}

.anime-cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 500;
  color: white;
  border: 2px dashed rgba(255, 255, 255, 0.5);
}

.image-placeholder.small {
  font-size: 1rem;
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

.anime-info {
  flex-grow: 1;
}

.anime-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: white;
}

/* Favorites button */
.favorite-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.5);
  color: white;
  font-weight: 500;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.favorite-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* If already favorite */
.favorite-button.is-favorite {
  background-color: #ec4899;
  border-color: #ec4899;
  box-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
}

.favorite-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.favorite-button:hover .favorite-icon {
  transform: scale(1.2);
}

/* Animation */
.favorite-button.is-favorite .favorite-icon {
  color: white;
  animation: pulse 1s ease-in-out;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.3);
  }
  100% {
    transform: scale(1);
  }
}

/* Info Layout */
.anime-meta-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 640px) {
  .anime-meta-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.meta-label {
  font-size: 0.875rem;
  font-weight: 500;
  opacity: 0.8;
}

.meta-value {
  font-size: 1rem;
  font-weight: 500;
}

/* Genre stuff */
.genre-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.genre-tag {
  font-size: 0.75rem;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

/* Rating stars and score */
.rating-display {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.rating-value {
  font-size: 1.25rem;
  font-weight: 600;
}

.rating-stars {
  display: flex;
  gap: 2px;
}

.star {
  width: 18px;
  height: 18px;
  background-color: rgba(255, 255, 255, 0.3);
  clip-path: polygon(
    50% 0%,
    61% 35%,
    98% 35%,
    68% 57%,
    79% 91%,
    50% 70%,
    21% 91%,
    32% 57%,
    2% 35%,
    39% 35%
  );
}

.star.filled {
  background-color: #ffdd00;
}

.star.half {
  position: relative;
  overflow: hidden;
}

.star.half::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 50%;
  height: 100%;
  background-color: #ffdd00;
}

/* Section padding and border */
.anime-section {
  padding: 2rem;
  border-bottom: 1px solid #e5e7eb;
}

.anime-section:last-child {
  border-bottom: none;
}

.anime-description {
  font-size: 1rem;
  line-height: 1.8;
  color: #666;
}

/* Slider styles */
.slider-container {
  position: relative;
  padding: 0 2rem;
}

.anime-slider {
  display: flex;
  overflow-x: auto;
  gap: 1rem;
  padding: 1rem 0;
  scroll-behavior: smooth;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.anime-slider::-webkit-scrollbar {
  display: none;
}

/* Navigation buttons for slider */
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

/* Characters */
.characters-slider {
  padding: 1rem 0;
}

.character-card {
  flex-shrink: 0;
  width: 280px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  background-color: white;
}

.character-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(138, 43, 226, 0.2);
}

.character-image {
  position: relative;
  height: 150px;
  width: 100%;
  background-color: #f0f0f0;
}

.character-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.character-details {
  padding: 1rem;
}

.character-name {
  font-weight: bold;
  color: #8a2be2;
  margin-bottom: 0.25rem;
}

.character-role {
  display: inline-block;
  font-size: 0.75rem;
  background-color: #f3e8ff;
  color: #8a2be2;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  margin-bottom: 0.75rem;
}

.character-description {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Small screen stuff */
@media (max-width: 768px) {
  .main-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-container {
    width: 100%;
    margin-top: 1rem;
  }

  .character-card {
    width: 240px;
  }

  .review-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .review-rating {
    align-items: flex-start;
  }
}
</style>
