<template>
  <div class="login-container">
    <h1>Anime Fan Sign Up!</h1>
    <form @submit.prevent="handleSignUp">
      <input
        type="email"
        id="email"
        v-model="email"
        placeholder="Email"
        required
      />
      <input
        type="text"
        id="username"
        v-model="username"
        placeholder="Username"
        required
      />
      <input
        type="password"
        id="password"
        v-model="password"
        placeholder="Password"
        required
      />

      <button type="submit" id="loginBtn">Sign Up</button>
      <button @click="$emit('toggle')">Go to Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
      email: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleSignUp() {
      try {
        const response = await fetch(`http://localhost:8000/app/signUp`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
            email: this.email,
          }),
        });

        const data = await response.json();
        console.log(data);

        if (data.success) {
          console.log("Successfully created account");
          this.$emit("signUp-successful");
        } else if (data.errorMessage.username) {
          console.log("Used username");
          alert(data.errorMessage.username);
        } else {
          console.log("Used email");
          alert(data.errorMessage.errorMessage);
        }
      } catch (err) {
        console.error(err);
      }
      //   alert("Sign up clicked! Redirect to registration page.");
    },
  },
};
</script>

<style src="./LoginPageStyle.css" scoped></style>
