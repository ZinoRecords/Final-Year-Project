<template>
  <div class="login-container">
    <h1>Anime Fan Login</h1>
    <form @submit.prevent="handleLogin">
      <input
        type="text"
        id="username"
        v-model="username"
        placeholder="Username/Email"
        required
      />
      <input
        type="password"
        id="password"
        v-model="password"
        placeholder="Password"
        required
      />
      <button type="submit" id="loginBtn">Log In</button>
      <button @click="$emit('toggle')" type="button" id="signupBtn">
        Go to Sign Up
      </button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
      error: "",
    };
  },
  methods: {
    async handleLogin() {
      this.error = "";

      // Trigger CSRF cookie setup
      await fetch("http://localhost:8000/app/api/whoami/", {
        credentials: "include",
      });

      const response = await fetch("http://localhost:8000/app/api/login/", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": this.getCSRFToken(),
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      });

      if (response.ok) {
        this.$emit("login-successful");
      } else {
        const data = await response.json();
        this.error = data.error || "Login failed.";
      }
    },
    handleSignUp() {
      alert("Sign up clicked! Redirect to registration page.");
    },
  },
};
</script>

<style src="./LoginPageStyle.css" scoped></style>
