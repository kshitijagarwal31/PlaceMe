<template>
  <div class="page">

    <Navbar />

    <div class="register-page">
      <div class="register-card">

        <div class="top-section">
          <h2>Create Account</h2>
          <p>Register on Placement Portal</p>
        </div>

        <div v-if="errorMessage" class="error-box">
          {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="success-box">
          {{ successMessage }}
        </div>

        <form @submit.prevent="handleRegister">

          <div class="input-group">
            <label>Full Name</label>
            <input
              v-model="fullName"
              type="text"
              placeholder="Enter your name"
              required
            />
          </div>

          <div class="input-group">
            <label>Username</label>
            <input
              v-model="username"
              type="text"
              placeholder="Enter username"
              required
            />
          </div>

          <div class="input-group">
            <label>Email</label>
            <input
              v-model="email"
              type="email"
              placeholder="Enter email"
              required
            />
          </div>

          <div class="input-group">
            <label>Role</label>
            <select v-model="role" required>
              <option disabled value="">Select role</option>
              <option value="student">Student</option>
              <option value="company">Company</option>
            </select>
          </div>

          <div class="input-group">
            <label>Password</label>
            <div class="password-box">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Create password"
                required
              />
              <button
                type="button"
                class="show-btn"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? "Hide" : "Show" }}
              </button>
            </div>
          </div>

          <button type="submit" class="register-btn" :disabled="loading">
            <span v-if="loading">Creating Account...</span>
            <span v-else>Register</span>
          </button>

        </form>

        <p class="bottom-text">
          Already have an account?
          <router-link to="/login">Login</router-link>
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
  name: "RegisterView",

  components: {
    Navbar,
    Footer
  },

  data() {
    return {
      fullName: "",
      username: "",
      email: "",
      role: "",
      password: "",
      showPassword: false,
      loading: false,
      errorMessage: "",
      successMessage: ""
    }
  },

  methods: {
    async handleRegister() {
      this.errorMessage = ""
      this.successMessage = ""
      this.loading = true

      const url =
        this.role === "student"
          ? "http://localhost:5000/register/student"
          : "http://localhost:5000/register/company"

      try {
        const res = await axios.post(url, {
          name: this.fullName,
          username: this.username,
          email: this.email,
          password: this.password
        })

        this.successMessage = res.data.message

        setTimeout(() => {
          this.$router.push("/login")
        }, 2000)
      } catch (err) {
        this.errorMessage =
          err.response?.data?.message || "Something went wrong!"
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>

.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  font-family: Arial, Helvetica, sans-serif;
}

.register-page {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 32px 20px;
  background: #f5f7fb;
}

.register-card {
  width: 100%;
  max-width: 420px;
  background: white;
  padding: 32px;
  border-radius: 14px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
}

.top-section {
  text-align: center;
  margin-bottom: 22px;
}

.top-section h2 {
  font-size: 26px;
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

.success-box {
  background: #f0fdf4;
  color: #16a34a;
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 13px;
  font-weight: 600;
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

.input-group input,
.input-group select {
  width: 100%;
  padding: 11px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  outline: none;
  font-size: 13px;
  transition: 0.2s;
  background: white;
  box-sizing: border-box;
}

.input-group input:focus,
.input-group select:focus {
  border-color: #2563eb;
}

.password-box {
  position: relative;
}

.password-box input {
  padding-right: 52px;
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

.register-btn {
  width: 100%;
  padding: 12px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  margin-top: 4px;
}

.register-btn:hover {
  background: #1d4ed8;
}

.register-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.bottom-text {
  text-align: center;
  margin-top: 18px;
  font-size: 13px;
  color: #6b7280;
}

.bottom-text a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
}

</style>