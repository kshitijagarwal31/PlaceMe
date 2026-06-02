<template>
  <div class="page">

    <Navbar />

    <div class="login-page">

      <div class="login-card">

        <div class="top-section">
          <h2>Welcome Back</h2>
          <p>Sign in to continue to PlaceMe Portal</p>
        </div>

        <div v-if="errorMessage" class="error-box">
          {{ errorMessage }}
        </div>

        <form @submit.prevent="handleLogin">

          <div class="input-group">
            <label>Username</label>
            <input type="text" v-model="username" placeholder="Enter your username" required />
          </div>

          <div class="input-group">
            <label>Password</label>

            <div class="password-box">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                placeholder="Enter your password"
                required
              />

              <button type="button" class="show-btn" @click="showPassword = !showPassword">
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
            </div>
          </div>

          <button type="submit" class="login-btn" :disabled="loading">
            <span v-if="loading">Signing In...</span>
            <span v-else>Login</span>
          </button>

        </form>

        <p class="register-text">
          Don't have an account?
          <router-link to="/register">Register</router-link>
        </p>

      </div>

    </div>

    <Footer />

  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"
import Footer from "../components/Footer.vue"
import axios from "axios"

export default {
  name: "LoginView",
  components: {
    Navbar,
    Footer
  },

  data() {
    return {
      username: "",
      password: "",
      showPassword: false,
      loading: false,
      errorMessage: ""
    }
  },

  methods: {
    async handleLogin() {
      this.errorMessage = ""
      this.loading = true

      try {
        const res = await axios.post("http://localhost:5000/login", {
          username: this.username,
          password: this.password
        })

        localStorage.setItem("token", res.data.auth_token)
        localStorage.setItem("user", JSON.stringify(res.data.user))

        const role = res.data.user.roles[0]

        if (role === "admin") {
          this.$router.push("/admin_dashboard")
        } else if (role === "company") {
          this.$router.push("/company_dashboard")
        } else if (role === "student") {
          this.$router.push("/student_dashboard")
        }

      } catch (err) {
          this.errorMessage =
            err.response?.data?.message ||
            "Something went wrong!"
      } finally {
        this.loading = false
      }

    }
  }
}
</script>

<style scoped>

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.login-page {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 30px 20px;
  background: #f5f7fb;
  font-family: Arial, Helvetica, sans-serif;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.06);
}

.top-section {
  text-align: center;
  margin-bottom: 22px;
}

.top-section h2 {
  font-size: 28px;
  color: #111827;
  margin-bottom: 6px;
  font-weight: 700;
}

.top-section p {
  color: #6b7280;
  font-size: 13px;
}

.error-box {
  background: #fef2f2;
  color: #dc2626;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 13px;
}

.input-group {
  margin-bottom: 16px;
}

.input-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.input-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
  font-size: 13px;
  transition: 0.2s;
}

.input-group input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
}

.password-box {
  position: relative;
}

.show-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: none;
  color: #2563eb;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.2s;
}

.login-btn:hover {
  background: #1d4ed8;
}

.login-btn:disabled {
  opacity: 0.7;
}

.register-text {
  text-align: center;
  margin-top: 18px;
  color: #6b7280;
  font-size: 13px;
}

.register-text a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 700;
}

</style>