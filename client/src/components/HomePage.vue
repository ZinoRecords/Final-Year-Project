<template>
  <div>
    <!-- <nav>
      <ul>
        <li><a href="#popular">Popular</a></li>
        <li><a href="#new-releases">New Releases</a></li>
        <li><a href="#genres">Genres</a></li>
        <li><a href="#my-list">My List</a></li>
        <li><a href="#community">Community</a></li>
        <li><a href="#news">News</a></li>
      </ul>
    </nav> -->
    <div class="container">
      <header>
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
        <h2>Welcome!</h2>
        <div class="grid-container">
          <a href="#popular" class="grid-item">Popular</a>
          <a href="#new-releases" class="grid-item">New Releases</a>
          <a href="#genres" class="grid-item">Genres</a>
          <a href="#my-list" class="grid-item">My List</a>
          <a href="#community" class="grid-item">Community</a>
          <a href="#news" class="grid-item">News</a>
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      searchTerm: "",
    };
  },
  methods: {
    performSearch() {
      if (this.searchTerm.trim()) {
        alert(`Searching for: ${this.searchTerm}`);
        // Here you would typically send the search term to a backend API
        // and display the results on the page
      }
    },
  },
};
</script>

<style src="./HomePageStyle.css" scoped></style>
