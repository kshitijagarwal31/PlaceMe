<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Welcome, {{ studentName }}! </h1>
        <p>Here's your placement overview</p>
      </div>
    </div>

    <div v-if="!profileComplete" class="profile-banner">
      <div class="banner-left">
        <span class="banner-icon">⚠️</span>
        <div>
          <p class="banner-title">Complete Your Profile First!</p>
          <p class="banner-sub">Please complete your profile before applying for a drive.</p>
        </div>
      </div>
      <button class="btn-complete" @click="goToProfile">Complete Profile</button>
    </div>

    <div v-if="loadingStats" class="empty" style="padding: 40px 0;">
      Loading...
    </div>

    <div v-else class="cards">
      <div class="card">
        <h2>{{ stats.total_applications }}</h2>
        <p>Total Applications</p>
      </div>
      <div class="card">
        <h2>{{ stats.shortlisted }}</h2>
        <p>Shortlisted</p>
      </div>
      <div class="card">
        <h2>{{ stats.selected }}</h2>
        <p>Selected</p>
      </div>
      <div class="card">
        <h2>{{ stats.ongoing_drives }}</h2>
        <p>Active Drives</p>
      </div>
    </div>

    <div class="requests-grid">

      <div class="section-box">
        <div class="section-header">
          <h3>My Recent Applications</h3>
        </div>

        <div v-if="loadingStats" class="empty">Loading...</div>

        <div v-else-if="applications.length === 0" class="empty">
          No applications yet
        </div>

        <div
          v-for="app in applications.slice(0, 5)"
          :key="app.id"
          class="request-item"
        >
          <div class="request-left">
            <div class="avatar">{{ app.company ? app.company.charAt(0) : '?' }}</div>
            <div>
              <p class="request-name">{{ app.company }}</p>
              <p class="request-sub">{{ app.drive_title }} · {{ app.apply_date }}</p>
            </div>
          </div>
          <span :class="
            app.status === 'Selected'    ? 'badge-selected'    :
            app.status === 'Shortlisted' ? 'badge-shortlisted' :
            app.status === 'Pending'     ? 'badge-pending'     :
            app.status === 'Interview Scheduled' ? 'badge-interview' :
            'badge-rejected'
          ">{{ app.status }}</span>
        </div>
      </div>

      <div class="section-box">
        <div class="section-header">
          <h3>Active Drives</h3>
        </div>

        <div v-if="loadingStats" class="empty">Loading...</div>

        <div v-else-if="drives.length === 0" class="empty">
          No active drives
        </div>

        <div
          v-for="drive in drives.slice(0, 5)"
          :key="drive.id"
          class="request-item"
        >
          <div class="request-left">
            <div class="avatar">{{ drive.company ? drive.company.charAt(0) : '?' }}</div>
            <div>
              <p class="request-name">{{ drive.company }}</p>
              <p class="request-sub">{{ drive.job_title }} · {{ drive.end_date }}</p>
            </div>
          </div>
          <span class="badge-upcoming">{{ drive.salary || 'N/A' }}</span>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "StudentHomeView",

  data() {
    return {
      studentName: "",
      loadingStats:    true,
      profileComplete: true,
      stats: {
        total_applications: 0,
        selected:           0,
        shortlisted:        0,
        ongoing_drives:     0,
      },
      applications: [],
      drives:       [],
    }
  },

  async mounted() {
    await this.fetchDashboardData()
  },

  methods: {

    getHeaders() {
      return {
        headers: {
          "Authentication-Token": localStorage.getItem("token"),
        },
      }
    },

    async fetchDashboardData() {
      this.loadingStats = true
      try {
        const res = await axios.get("http://localhost:5000/student/dashboard_data", this.getHeaders())
        const data = res.data
        this.stats           = Object.assign({}, data.stats)
        this.applications    = data.applications     || []
        this.drives          = data.placement_drives || []
        this.profileComplete = data.profile_complete
        this.studentName     = data.student_name || ""
      } catch (err) {
        console.error("Dashboard data load failed:", err)
      } finally {
        this.loadingStats = false
      }
    },

    goToProfile() {
      this.$router.push("/student_dashboard/profile")
    }

  }
}
</script>

<style scoped>

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 26px;
  flex-wrap: wrap;
  gap: 16px;
}

.topbar h1 {
  font-size: 30px;
  color: #111827;
  font-weight: 700;
}

.topbar p {
  font-size: 13px;
  color: #6b7280;
  margin-top: 4px;
}

.profile-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fefce8;
  border: 1px solid #fde047;
  border-radius: 14px;
  padding: 15px 19px;
  margin-bottom: 22px;
}

.banner-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.banner-icon {
  font-size: 21px;
}

.banner-title {
  font-size: 14px;
  font-weight: 700;
  color: #854d0e;
}

.banner-sub {
  font-size: 12px;
  color: #a16207;
}

.btn-complete {
  background: #ca8a04;
  color: white;
  border: none;
  padding: 9px 18px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-complete:hover {
  background: #a16207;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 18px;
  margin-bottom: 26px;
}

.card {
  background: white;
  padding: 22px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  transition: 0.2s;
}

.card:hover {
  transform: translateY(-2px);
}

.card h2 {
  font-size: 27px;
  color: #2563eb;
  font-weight: 700;
  margin-bottom: 6px;
}

.card p {
  font-size: 13px;
  color: #6b7280;
}

.requests-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.section-box {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
  padding: 20px;
}

.section-header {
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
  padding: 12px 0;
  border-bottom: 1px solid #f3f4f6;
}

.request-left {
  display: flex;
  align-items: center;
  gap: 11px;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #eff6ff;
  color: #2563eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
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

.badge-selected,
.badge-shortlisted,
.badge-pending,
.badge-rejected,
.badge-upcoming,
.badge-interview {
  font-size: 11.5px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 16px;
  white-space: nowrap;
}

.badge-selected { 
  background: #dbeafe; 
  color: #2563eb; 
}

.badge-shortlisted { 
  background: #dcfce7; 
  color: #16a34a; 
}

.badge-pending { 
  background: #fef9c3; 
  color: #ca8a04; 
}

.badge-rejected { 
  background: #fee2e2; 
  color: #dc2626; 
}

.badge-upcoming { 
  background: #eff6ff; 
  color: #2563eb; 
}

.badge-interview { 
  background: #f3e8ff; 
  color: #7c3aed; 
}

.empty {
  text-align: center;
  color: #9ca3af;
  font-size: 13px;
  padding: 26px 0;
}

</style>