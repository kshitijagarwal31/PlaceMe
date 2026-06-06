<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Welcome, {{ companyName }}!</h1>
        <p>Here's your placement overview</p>
      </div>
    </div>

    <div v-if="!checkingProfile && !isProfileComplete" class="profile-banner">
      <div class="banner-left">
        <div>
          <p class="banner-title">Complete Your Profile First!</p>
          <p class="banner-sub">Complete your profile before creating a Placement Drive.</p>
        </div>
      </div>
      <button class="btn-complete" @click="goToProfile">
        Complete Profile
      </button>
    </div>

    <div v-if="loadingStats" class="loading">
      Loading...
    </div>

    <!-- STATS -->
    <div v-else class="cards">
      <div class="card">
        <h2>{{ stats.total_drives }}</h2>
        <p>Total Drives</p>
      </div>
      <div class="card">
        <h2>{{ stats.active_drives }}</h2>
        <p>Active Drives</p>
      </div>
      <div class="card">
        <h2>{{ stats.total_applications }}</h2>
        <p>Total Applications</p>
      </div>
      <div class="card">
        <h2>{{ stats.selected_count }}</h2>
        <p>Selected Students</p>
      </div>
    </div>

    <div v-if="!loadingStats" class="requests-grid">

      <!-- DRIVES -->
      <div class="section-box">
        <div class="section-header">
          <h3>Active Drives</h3>
          <button class="btn-export" @click="exportCSV">Export CSV</button>
        </div>

        <div v-if="drives.length === 0" class="empty">
          No drives yet
        </div>

        <div
          v-for="drive in drives.slice(0, 5)"
          :key="drive.id"
          class="request-item"
        >
          <div class="request-left">
            <div class="avatar">
              {{ drive.job_title?.charAt(0) || "?" }}
            </div>
            <div>
              <p class="request-name">{{ drive.job_title }}</p>
              <p class="request-sub">{{ drive.start_date }} · {{ drive.end_date }}</p>
            </div>
          </div>
          <span :class="getDriveStatusClass(drive.status)">
            {{ drive.status }}
          </span>
        </div>
      </div>

      <!-- APPLICATIONS -->
      <div class="section-box">
        <div class="section-header">
          <h3>Recent Applicants</h3>
        </div>

        <div v-if="applications.length === 0" class="empty">
          No applicants yet
        </div>

        <div
          v-for="application in applications.slice(0, 5)"
          :key="application.id"
          class="request-item"
        >
          <div class="request-left">
            <div class="avatar">
              {{ application.student_name?.charAt(0) || "?" }}
            </div>
            <div>
              <p class="request-name">{{ application.student_name }}</p>
              <p class="request-sub">{{ application.drive_title }}</p>
            </div>
          </div>
          <span :class="getStatusClass(application.status)">
            {{ application.status }}
          </span>
        </div>
      </div>


    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyHomeView",

  data() {
    return {
      companyName: "",
      isProfileComplete: false,
      checkingProfile: true,
      loadingStats: true,
      stats: {
        total_drives: 0,
        active_drives: 0,
        total_applications: 0,
        selected_count: 0
      },
      applications: [],
      drives: []
    }
  },

  async mounted() {
    await this.checkProfile()
    await this.fetchDashboardData()
  },

  methods: {
    getHeaders() {
      return {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    },

    getStatusClass(status) {
      if (status === "Pending") return "badge-pending"
      if (status === "Shortlisted") return "badge-shortlisted"
      if (status === "Rejected") return "badge-rejected"
      if (status === "Selected") return "badge-selected"
      if (status === "Interview Scheduled") return "badge-interview"
      return "badge-pending"
    },

    getDriveStatusClass(status) {
      if (status === "Active") return "badge-active"
      if (status === "Pending") return "badge-pending"
      if (status === "Closed") return "badge-closed"
      return "badge-closed"
    },

    async checkProfile() {
      this.checkingProfile = true

      try {
        const res = await axios.get(
          "http://localhost:5000/company/complete_profile",
          this.getHeaders()
        )
        const profile = res.data

        if (
          profile.name &&
          profile.industry &&
          profile.address &&
          profile.hr_contact_number &&
          profile.website_link
        ) {
          this.isProfileComplete = true
        } else {
          this.isProfileComplete = false
        }
      } catch (err) {
        console.error("Profile check failed:", err)
        this.isProfileComplete = false
      } finally {
        this.checkingProfile = false
      }
    },

    async fetchDashboardData() {
      this.loadingStats = true

      try {
        const res = await axios.get(
          "http://localhost:5000/company/dashboard_data",
          this.getHeaders()
        )
        const data = res.data

        this.stats = data.stats || this.stats
        this.applications = data.applications || []
        this.drives = data.placement_drives || []
        this.companyName = data.company_name || ""
      } catch (err) {
        console.error("Dashboard data load failed:", err)
      } finally {
        this.loadingStats = false
      }
    },

    goToProfile() {
      this.$router.push("/company_dashboard/profile")
    },

    async exportCSV() {
      try {
        await axios.get(
          "http://localhost:5000/company/export_csv",
          this.getHeaders()
        )
        alert("✅ Check your email, your applications CSV has been sent!")
      } catch (err) {
        console.error("Export failed:", err)
        alert("Export failed, please try again!")
      }
    }
  }
}
</script>

<style scoped>

.profile-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  background: #fefce8;
  border: 1px solid #fde047;
  border-radius: 14px;
  padding: 14px 18px;
  margin-bottom: 22px;
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.banner-title {
  font-size: 14px;
  font-weight: 700;
  color: #854d0e;
}

.banner-sub {
  font-size: 12px;
  color: #a16207;
  margin-top: 2px;
}

.btn-complete {
  background: #ca8a04;
  color: white;
  border: none;
  padding: 9px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: 0.2s;
}

.btn-complete:hover {
  background: #a16207;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 26px;
}

.topbar h1 {
  font-size: 30px;
  color: #111827;
  margin-bottom: 3px;
}

.topbar p {
  font-size: 13px;
  color: #6b7280;
}

.loading {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  padding: 40px 0;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
  margin-bottom: 26px;
}

.card {
  background: white;
  padding: 22px;
  border-radius: 14px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
}

.card h2 {
  font-size: 28px;
  color: #2563eb;
  margin-bottom: 6px;
  font-weight: 700;
}

.card p {
  color: #6b7280;
  font-size: 13px;
}

.requests-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.section-box {
  background: white;
  border-radius: 14px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
  padding: 22px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 17px;
  font-weight: 600;
  color: #111827;
}

.request-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.request-item:last-of-type {
  border-bottom: none;
}

.request-left {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #eff6ff;
  color: #2563eb;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}

.request-name {
  font-size: 13px;
  font-weight: 600;
  color: #111827;
}

.request-sub {
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
}

.badge-pending {
  background: #fef9c3;
  color: #ca8a04;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.badge-shortlisted {
  background: #dcfce7;
  color: #16a34a;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.badge-selected {
  background: #dbeafe;
  color: #2563eb;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.badge-rejected {
  background: #fee2e2;
  color: #dc2626;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.badge-active {
  background: #dcfce7;
  color: #16a34a;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.badge-closed {
  background: #f3f4f6;
  color: #4b5563;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.badge-interview {
  background: #f3e8ff;
  color: #7c3aed;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  white-space: nowrap;
}

.empty {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  padding: 35px 0;
}

.btn-export {
  background: #2563eb;
  color: white;
  border: none;
  padding: 5px 12px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-export:hover {
  background: #1d4ed8;
}

</style>