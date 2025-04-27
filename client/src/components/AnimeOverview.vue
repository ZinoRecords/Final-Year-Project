<template>
  <div class="container">
    <header class="main-header">
      <h1>AnimeWorld</h1>
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
            <img
              v-else
              :src="animeData.imageURL"
              :alt="animeData.name"
              class="anime-cover-image"
            />
            <div class="anime-type">TV</div>
          </div>

          <div class="anime-info">
            <h3 class="anime-title">{{ animeData.name }}</h3>

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
                      :style="star.style"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <section class="anime-section">
          <h3 class="section-heading">Description</h3>
          <p class="anime-description">{{ animeData.description }}</p>
        </section>

        <section class="anime-section">
          <div class="section-header">
            <h3 class="section-heading">Characters</h3>
            <a href="#" class="view-all">View All</a>
          </div>

          <div class="slider-container">
            <button class="slider-btn prev-btn" @click="handleSlide(-1)">
              ◀
            </button>
            <div class="anime-slider characters-slider" ref="sliderRef">
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
            <button class="slider-btn next-btn" @click="handleSlide(1)">
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
    };
  },

  methods: {
    generateStars() {
      const rating = this.animeData.rating;
      const fullStars = Math.floor(rating);
      const hasHalfStar = rating % 1 >= 0.5;
      const maxStars = 5;

      // Calculate what portion of the max rating (10) this represents for 5 stars
      const scaledRating = (rating / 10) * 5;
      const scaledFullStars = Math.floor(scaledRating);
      const scaledHasHalfStar = scaledRating % 1 >= 0.5;

      // Use the original rating if it's out of 5, or the scaled rating if it's out of 10
      const starsToShow =
        rating <= 5
          ? { full: fullStars, half: hasHalfStar }
          : { full: scaledFullStars, half: scaledHasHalfStar };

      // Add filled stars
      for (let i = 0; i < starsToShow.full; i++) {
        this.stars.push({ type: "filled" });
      }

      // Add half star if needed
      if (starsToShow.half) {
        this.stars.push({ type: "half" });
      }

      // Add empty stars
      const emptyStars =
        maxStars - starsToShow.full - (starsToShow.half ? 1 : 0);
      for (let i = 0; i < emptyStars; i++) {
        this.stars.push({ type: "" });
      }
    },
    handleSlide(direction) {
      if (this.$refs.sliderRef) {
        const scrollAmount =
          direction * (this.$refs.sliderRef.clientWidth * 0.8);
        this.$refs.sliderRef.scrollBy({
          left: scrollAmount,
          behavior: "smooth",
        });
      }
    },
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

        // Format the date
        const date = new Date(this.animeData.releaseDate);
        this.formattedDate = isNaN(date)
          ? "Unknown"
          : date.toLocaleDateString("en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
            });

        this.genreList = anime.genres.map((g) => g.name);

        // Generate stars
        this.stars = [];
        this.generateStars();

        // Fetch characters
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
            description: "", // Jikan doesn't provide character descriptions in this endpoint
          }));
      } catch (err) {
        console.error("Failed to fetch anime overview:", err);
      }
    },
  },
  mounted() {
    this.fetchAnimeOverview(this.animeID);
  },
};
</script>

<style>
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

/* Section Header */
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

/* Anime Overview */
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

@media (min-width: 768px) {
  .anime-header {
    flex-direction: row;
  }
}

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

/* Anime Section */
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

/* Slider */
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
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.anime-slider::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
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

/* Character Cards */
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

  .character-card {
    width: 240px;
  }
}
</style>
