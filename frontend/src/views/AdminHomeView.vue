<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Welcome, {{ adminName }}! </h1>
        <p>Here's your placement overview</p>
      </div>
    </div>

    <div v-if="loading" class="empty" style="padding: 60px 0;">
      Loading dashboard...
    </div>

    <div v-else>

      <div class="cards">
        <div class="card">
          <h2>{{ stats.total_students }}</h2>
          <p>Total Students</p>
        </div>
        <div class="card">
          <h2>{{ stats.total_companies }}</h2>
          <p>Total Companies</p>
        </div>
        <div class="card">
          <h2>{{ stats.total_drives }}</h2>
          <p>Placement Drives</p>
        </div>
        <div class="card">
          <h2>{{ stats.total_applications }}</h2>
          <p>Total Applications</p>
        </div>
        <div class="card">
          <h2>{{ stats.total_placements }}</h2>
          <p>Total Placements</p>
        </div>
        <div class="card">
          <h2>{{ stats.placement_rate }}%</h2>
          <p>Placement Rate</p>
        </div>
      </div>

      <div class="requests-grid">

        <div class="section-box">
          <div class="section-header">
            <h3>Company Requests</h3>
            <span class="pending-count">{{ pendingCompanies.length }} Pending</span>
          </div>

          <div v-if="pendingCompanies.length === 0" class="empty">
            No pending requests
          </div>

          <div
            v-for="company in pendingCompanies.slice(0, 5)"
            :key="company.id"
            class="request-item"
          >
            <div class="request-left">
              <div class="avatar">{{ company.name.charAt(0) }}</div>
              <div>
                <p class="request-name">{{ company.name }}</p>
                <p class="request-sub">{{ company.industry }} · {{ company.address }}</p>
              </div>
            </div>
            <div class="request-actions">
              <button class="btn-approve" @click="approveCompany(company)">Approve</button>
              <button class="btn-reject"  @click="rejectCompany(company)">Reject</button>
            </div>
          </div>

          <div v-if="pendingCompanies.length > 5" class="view-all">
            Showing 5 of {{ pendingCompanies.length }} — go to Companies page
          </div>
        </div>

        <div class="section-box">
          <div class="section-header">
            <h3>Drive Requests</h3>
            <span class="pending-count">{{ pendingDrives.length }} Pending</span>
          </div>

          <div v-if="pendingDrives.length === 0" class="empty">
            No pending requests
          </div>

          <div
            v-for="drive in pendingDrives.slice(0, 5)"
            :key="drive.id"
            class="request-item"
          >
            <div class="request-left">
              <div class="avatar">{{ drive.company_name.charAt(0) }}</div>
              <div>
                <p class="request-name">{{ drive.company_name }}</p>
                <p class="request-sub">{{ drive.job_title }} · {{ drive.start_date }}</p>
              </div>
            </div>
            <div class="request-actions">
              <button class="btn-approve" @click="approveDrive(drive)">Approve</button>
              <button class="btn-reject"  @click="rejectDrive(drive)">Reject</button>
            </div>
          </div>

          <div v-if="pendingDrives.length > 5" class="view-all">
            Showing 5 of {{ pendingDrives.length }} — go to Drives page
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdminHomeView",

  data() {
    return {
      adminName: "",
      loading: true,
      stats: {
        total_students:     0,
        total_companies:    0,
        total_drives:       0,
        total_applications: 0,
        total_placements:   0,
        placement_rate:     0,
      },
      pendingCompanies: [],
      pendingDrives:    [],
    };
  },

  async mounted() {
    await this.fetchDashboardData();
  },

  methods: {

    getHeaders() {
      return {
        headers: {
          "Authentication-Token": localStorage.getItem("token"), 
        },
      };
    },

    async fetchDashboardData() {
      this.loading = true;
      try {
        const res = await axios.get("http://localhost:5000/admin/dashboard_data", this.getHeaders()); 
        console.log("Full response:", res.data);
        this.stats            = res.data.stats             || this.stats;
        this.pendingCompanies = res.data.pending_companies || [];
        this.pendingDrives    = res.data.pending_drives    || [];
        this.adminName        = res.data.admin_name        || [];
      } catch (err) {
        console.error("Error:", err.response);
      } finally {
        this.loading = false;
      }
    },

    async approveCompany(company) {
      try {
        await axios.post(`http://localhost:5000/admin/company/approve/${company.id}`, {}, this.getHeaders());
        this.pendingCompanies = this.pendingCompanies.filter(c => c.id !== company.id);
        this.stats.total_companies++;
      } catch (err) {
        console.error("Approve company failed:", err);
        alert("Could not approve company.");
      }
    },

    async rejectCompany(company) {
      try {
        await axios.post(`http://localhost:5000/admin/company/reject/${company.id}`, {}, this.getHeaders());
        this.pendingCompanies = this.pendingCompanies.filter(c => c.id !== company.id);
      } catch (err) {
        console.error("Reject company failed:", err);
        alert("Could not reject company.");
      }
    },

    async approveDrive(drive) {
      try {
        await axios.post(`http://localhost:5000/admin/placement_drive/approve/${drive.id}`, {}, this.getHeaders());
        this.pendingDrives = this.pendingDrives.filter(d => d.id !== drive.id);
        this.stats.total_drives++;
      } catch (err) {
        console.error("Approve drive failed:", err);
        alert("Could not approve drive.");
      }
    },

    async rejectDrive(drive) {
      try {
        await axios.post(`http://localhost:5000/admin/placement_drive/reject/${drive.id}`, {}, this.getHeaders());
        this.pendingDrives = this.pendingDrives.filter(d => d.id !== drive.id);
      } catch (err) {
        console.error("Reject drive failed:", err);
        alert("Could not reject drive.");
      }
    },

  },
};
</script>

<style scoped>

.topbar {
  margin-bottom: 27px;
}

.topbar h1 {
  font-size: 31px;
  color: #111827;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(162px, 1fr));
  gap: 18px;
  margin-bottom: 27px;
}

.card {
  background: white;
  padding: 22px;
  border-radius: 16px;
  box-shadow: 0 4px 13px rgba(0, 0, 0, 0.05);
}

.card h2 {
  font-size: 27px;
  color: #2563eb;
  margin-bottom: 7px;
  font-weight: 700;
}

.card p {
  color: #6b7280;
  font-size: 13px;
}

.requests-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.section-box {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 13px rgba(0, 0, 0, 0.05);
  padding: 22px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.section-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.pending-count {
  background: #fef9c3;
  color: #ca8a04;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 11px;
  border-radius: 18px;
}

.request-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 13px 0;
  border-bottom: 1px solid #f3f4f6;
}

.request-item:last-of-type {
  border-bottom: none;
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

.request-actions {
  display: flex;
  gap: 7px;
}

.btn-approve {
  background: #dcfce7;
  color: #16a34a;
  border: none;
  padding: 6px 13px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-approve:hover {
  background: #bbf7d0;
}

.btn-reject {
  background: #fee2e2;
  color: #dc2626;
  border: none;
  padding: 6px 13px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-reject:hover {
  background: #fecaca;
}

.empty {
  text-align: center;
  color: #9ca3af;
  font-size: 13px;
  padding: 27px 0;
}

.view-all {
  text-align: center;
  color: #9ca3af;
  font-size: 12px;
  margin-top: 13px;
}

</style>