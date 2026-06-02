<template>

  <aside class="sidebar">

    <div class="top-section">

      <div class="logo-box">
        🎓
      </div>

      <div class="logo-content">

        <h2>
          PlaceMe
        </h2>

        <p>
          Placement Portal
        </p>

      </div>

    </div>

    <div class="menu-section">

      <div v-if="role === 'admin'">

        <router-link to="/admin_dashboard" class="menu-item" exact>
          📊 Dashboard
        </router-link>

        <router-link to="/admin_dashboard/students" class="menu-item">
          🎓 Students
        </router-link>

        <router-link to="/admin_dashboard/companies" class="menu-item">
          🏢 Companies
        </router-link>

        <router-link to="/admin_dashboard/placement_drives" class="menu-item">
          📅 Placement Drives
        </router-link>

        <router-link to="/admin_dashboard/applications" class="menu-item">
          📄 Applications
        </router-link>

      </div>

      <div v-if="role === 'student'">

        <router-link to="/student_dashboard" class="menu-item">
          📊 Dashboard
        </router-link>

        <router-link to="/student_dashboard/profile" class="menu-item">
          👤 My Profile
        </router-link>

        <router-link to="/student_dashboard/placement_drives" class="menu-item">
          📅 Placement Drives
        </router-link>

        <router-link to="/student_dashboard/applications" class="menu-item">
          📄 My Applications
        </router-link>

      </div>

      <div v-if="role === 'company'">

        <router-link to="/company_dashboard" class="menu-item">
          📊 Dashboard
        </router-link>

        <router-link to="/company_dashboard/profile" class="menu-item">
          👤 My Profile
        </router-link>

        <router-link to="/company_dashboard/create_drive" class="menu-item">
          💼 Create Drive
        </router-link>

        <router-link to="/company_dashboard/placement_drives" class="menu-item">
          📅 My Placement Drives
        </router-link>

        <router-link to="/company_dashboard/applications" class="menu-item">
          👨‍🎓 Applications
        </router-link>


      </div>

    </div>

    <div class="bottom-section">

      <div class="profile-box">

        <div class="profile-icon">
          👤
        </div>

        <div>

          <h4>
            {{ role }}
          </h4>

          <p>
            Portal User
          </p>

        </div>

      </div>

      <button class="logout-btn" @click="logout">
        Logout
      </button>

    </div>

  </aside>

</template>

<script>

export default {

  name: "Sidebar",
  props: {
    role: {
      type: String,
      required: true
    }
  }, 

  methods: {
    logout() {
      
      localStorage.removeItem("token")
      localStorage.removeItem("role")
      localStorage.removeItem("user")

      this.$router.push("/login")
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

.sidebar {
  width: 250px;
  min-height: 100vh;
  background: linear-gradient(180deg, #2563eb, #1d4ed8);
  padding: 20px 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-family: Arial, Helvetica, sans-serif;
}

.top-section {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 30px;
}

.logo-box {
  width: 46px;
  height: 46px;
  border-radius: 10px;
  background: rgba(255,255,255,0.15);
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 22px;
}

.logo-content h2 {
  color: white;
  font-size: 19px;
  line-height: 1.1;
}

.logo-content p {
  color: rgba(255,255,255,0.8);
  font-size: 11px;
  margin-top: 2px;
}

.menu-section {
  flex: 1;
}

.menu-item {
  width: 100%;
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
  padding: 12px 14px;
  border-radius: 10px;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 600;
  transition: 0.2s;
}

.menu-item:hover {
  background: rgba(255,255,255,0.12);
}

.menu-item.router-link-exact-active {
  background: rgba(255,255,255,0.22);
  border-left: 3px solid white;
}

.bottom-section {
  margin-top: 24px;
}

.profile-box {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255,255,255,0.12);
  padding: 12px;
  border-radius: 10px;
}

.profile-icon {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 16px;
}

.profile-box h4 {
  color: white;
  text-transform: capitalize;
  font-size: 14px;
  margin-bottom: 2px;
}

.profile-box p {
  color: rgba(255,255,255,0.7);
  font-size: 11px;
}

.logout-btn {
  width: 100%;
  margin-top: 14px;
  padding: 11px;
  border: none;
  border-radius: 10px;
  background: white;
  color: #2563eb;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.2s;
}

.logout-btn:hover {
  background: #dbeafe;
}

</style>