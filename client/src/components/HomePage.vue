<template>
  <div>
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
        <h2>Welcome {{ username }}!</h2>
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
      username: "",
    };
  },
  methods: {
    performSearch() {
      if (this.searchTerm.trim()) {
        alert(`Searching for: ${this.searchTerm}`);
      }
    },

    async getName() {
      const res = await fetch("http://localhost:8000/app/whoami/", {
        credentials: "include",
      });

      if (res.ok) {
        const user = await res.json();
        this.username = user.username;
        this.$emit("login-successful");
      }
    },
  },

  mounted() {
    this.getName();
  },
};
</script>

<style src="./HomePageStyle.css" scoped></style>
