<template>
  <nav class="navbar">

    <div class="navbar-left">
      <router-link to="/" class="logo-area">
        <div class="logo">🎓</div>
        <div>
          <h2 class="logo-title">PlaceMe</h2>
          <p class="logo-subtitle">Placement Portal</p>
        </div>
      </router-link>
    </div>

    <div class="navbar-right">
      <router-link to="/" class="nav-link">Home</router-link>
      <router-link to="/login" class="nav-link login-link">Login</router-link>
      <router-link to="/register" class="register-btn">Register</router-link>
    </div>

  </nav>
</template>

<script>

export default {
  name: "Navbar"
}

</script>

<style scoped>

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.navbar {
  width: 100%;
  height: 66px;
  padding: 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #2563eb;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(37, 99, 235, 0.35);
  font-family: 'Segoe UI', sans-serif;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo {
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 19px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.logo-title {
  font-size: 17px;
  font-weight: 800;
  color: white;
  line-height: 1.1;
  letter-spacing: -0.3px;
}

.logo-subtitle {
  font-size: 9.5px;
  color: #bfdbfe;
  margin-top: 1px;
  font-weight: 600;
  letter-spacing: 0.4px;
  text-transform: uppercase;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link {
  text-decoration: none;
  color: white;
  font-size: 13.5px;
  font-weight: 600;
  padding: 7px 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
  font-family: 'Segoe UI', sans-serif;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.15);
}

.login-link {
  border: 1.5px solid rgba(255, 255, 255, 0.5);
  padding: 7px 14px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.login-link:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: white;
}

.register-btn {
  text-decoration: none;
  background: white;
  color: #2563eb;
  padding: 8px 18px;
  border-radius: 8px;
  font-size: 13.5px;
  font-weight: 700;
  font-family: 'Segoe UI', sans-serif;
  transition: all 0.2s ease;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
  margin-left: 4px;
}

.register-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
  background: #e0e7ff;
}

.register-btn:active {
  transform: translateY(0);
}

</style>