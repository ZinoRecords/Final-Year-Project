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
    getCSRFToken() {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; csrftoken=`);
      if (parts.length === 2) return parts.pop().split(";").shift();
      return "";
    },
    async handleLogin() {
      this.error = "";

      try {
        const response = await fetch("http://localhost:8000/app/login/", {
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

        const data = await response.json();

        if (response.ok && data.success) {
          console.log("Login successful:", data);
          this.$emit("login-successful");
        } else {
          this.error =
            data.error || "Login failed. Please check your credentials.";
          console.error("Login failed:", data);
        }
      } catch (error) {
        console.error("Login error:", error);
        this.error =
          "Server error: Please check if the backend server is running.";
      }
    },
    handleSignUp() {
      alert("Sign up clicked! Redirect to registration page.");
    },
  },
};
</script>

<style src="./LoginPageStyle.css" scoped></style>
