<template>
  <div class="auth-page">
    <LoginPage
      v-if="!isLogged"
      @login-successful="onSuccessfulLogin"
      @toggle="togglePage"
    />
    <SignUp
      v-else
      @signUp-successful="onSuccessfulLogin"
      @toggle="togglePage"
    />
  </div>
</template>
<script>
import LoginPage from "./LoginPage.vue";
import SignUp from "./SignUp.vue";
import "./HomepageStyle.css";
export default {
  components: {
    LoginPage,
    SignUp,
  },
  data() {
    return {
      isLogged: false, // Correctly initialize this property in the `data` object
    };
  },
  methods: {
    togglePage() {
      this.isLogged = !this.isLogged; // Use `this` to refer to component properties
    },
    async onSuccessfulLogin() {
      const res = await fetch("http://localhost:8000/app/whoami/", {
        // Changed from /api/whoami/
        credentials: "include",
      });

      if (res.ok) {
        const user = await res.json();
        console.log("Logged in as:", user);
        this.$emit("login-successful"); // Added this.
      }
    },
  },
};
</script>
<style lang=""></style>
