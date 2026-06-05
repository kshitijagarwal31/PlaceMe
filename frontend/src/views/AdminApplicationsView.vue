<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Applications</h1>
        <p>All student applications</p>
      </div>

      <input
        v-model="search"
        class="search-input"
        type="text"
        placeholder="Search by student, company or status..."
      />
    </div>

    <!-- TABLE -->
    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>S.No</th>
            <th>Student</th>
            <th>Company</th>
            <th>Role</th>
            <th>Applied On</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="(application, index) in filteredApplications"
            :key="application.id"
          >
            <td>{{ index + 1 }}</td>
            <td>{{ application.student_name }}</td>
            <td>{{ application.company_name }}</td>
            <td>{{ application.drive }}</td>
            <td>{{ application.apply_date }}</td>
            <td>
              <span :class="getStatusClass(application.status)">
                {{ application.status }}
              </span>
            </td>
            <td>
              <button class="btn-view" @click="viewDetail(application)">
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="filteredApplications.length === 0" class="empty">
        No applications found
      </div>
    </div>

    <!-- MODAL -->
    <div
      v-if="selectedApplication"
      class="modal-overlay"
      @click.self="selectedApplication = null"
    >
      <div class="modal">

        <div class="modal-header">
          <h3>Application Detail</h3>
          <button class="btn-close" @click="selectedApplication = null">✕</button>
        </div>

        <div class="detail-top">
          <div class="avatar-lg">
            {{ selectedApplication.student_name?.charAt(0) || '?' }}
          </div>

          <div>
            <h4>{{ selectedApplication.student_name }}</h4>
            <p>{{ selectedApplication.company_name }} · {{ selectedApplication.drive }}</p>
          </div>

          <span :class="getStatusClass(selectedApplication.status)">
            {{ selectedApplication.status }}
          </span>
        </div>

        <div class="detail-rows">

          <div class="detail-row">
            <span class="detail-label">Student Name</span>
            <span class="detail-value">{{ selectedApplication.student_name || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Email</span>
            <span class="detail-value">{{ selectedApplication.email || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Company</span>
            <span class="detail-value">{{ selectedApplication.company_name || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Role</span>
            <span class="detail-value">{{ selectedApplication.drive || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Package</span>
            <span class="detail-value">{{ selectedApplication.package || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Applied On</span>
            <span class="detail-value">{{ selectedApplication.apply_date || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Feedback</span>
            <span class="detail-value">{{ selectedApplication.feedback || 'N/A' }}</span>
          </div>

          <div class="detail-row" v-if="selectedApplication.resume">
            <span class="detail-label">Resume</span>
            <a
              :href="'http://localhost:5000' + selectedApplication.resume"
              target="_blank"
              class="resume-link"
            >
              📄 View Resume
            </a>
          </div>

        </div>

        <div class="modal-footer">
          <button class="btn-close-modal" @click="selectedApplication = null">
            Close
          </button>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "AdminApplicationsView",

  data() {
    return {
      search: "",
      selectedApplication: null,
      applications: []
    }
  },

  computed: {
    filteredApplications() {
      const q = this.search.toLowerCase()

      return this.applications.filter((application) => {
        return (
          application.student_name.toLowerCase().includes(q) ||
          application.company_name.toLowerCase().includes(q) ||
          application.status.toLowerCase().includes(q)
        )
      })
    }
  },

  async mounted() {
    const token = localStorage.getItem("token")

    const res = await axios.get("http://localhost:5000/admin/applications", {
      headers: { "Authentication-Token": token }
    })

    this.applications = res.data.applications
  },

  methods: {
    viewDetail(application) {
      this.selectedApplication = application
    },

    getStatusClass(status) {
      if (status === "Selected") return "badge-selected"
      if (status === "Shortlisted") return "badge-shortlisted"
      if (status === "Rejected") return "badge-rejected"
      if (status === "Pending") return "badge-pending"
      if (status === "Interview Scheduled") return "badge-interview"
      return "badge-pending"
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
  margin-bottom: 3px;
}

.topbar p {
  color: #6b7280;
  font-size: 13px;
}

.search-input {
  width: 240px;
  padding: 10px 13px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 13px;
  outline: none;
  transition: 0.2s;
  background: white;
}

.search-input:focus {
  border-color: #2563eb;
}

.table-box {
  background: white;
  border-radius: 14px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f9fafb;
}

th {
  padding: 14px 18px;
  text-align: left;
  font-size: 13px;
  color: #6b7280;
  font-weight: 600;
  border-bottom: 1px solid #e5e7eb;
}

td {
  padding: 14px 18px;
  font-size: 14px;
  color: #111827;
  border-bottom: 1px solid #f3f4f6;
  font-weight: 600;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover td {
  background: #f9fafb;
}

.btn-view {
  background: #eff6ff;
  color: #2563eb;
  border: none;
  padding: 7px 12px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-view:hover {
  background: #dbeafe;
}

.badge-pending {
  background: #fef9c3;
  color: #ca8a04;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.badge-selected {
  background: #dbeafe;
  color: #2563eb;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.badge-shortlisted {
  background: #dcfce7;
  color: #16a34a;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.badge-rejected {
  background: #fee2e2;
  color: #dc2626;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.badge-applied {
  background: #dbeafe;
  color: #2563eb;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.badge-interview {
  background: #f3e8ff;
  color: #7c3aed;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.empty {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  padding: 35px 0;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 14px;
  width: 560px;
  max-width: 90%;
  max-height: 82vh;
  overflow-y: auto;
  padding: 24px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  position: sticky;
  top: 0;
  background: white;
  z-index: 1;
  padding-bottom: 14px;
  border-bottom: 1px solid #f3f4f6;
}

.modal-header h3 {
  font-size: 17px;
  font-weight: 600;
  color: #111827;
}

.btn-close {
  background: #f3f4f6;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  font-size: 13px;
  cursor: pointer;
  color: #374151;
}

.detail-top {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid #f3f4f6;
}

.avatar-lg {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: #eff6ff;
  color: #2563eb;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 19px;
  font-weight: 700;
  flex-shrink: 0;
}

.detail-top h4 {
  font-size: 15px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 3px;
  flex: 1;
}

.detail-top p {
  font-size: 12px;
  color: #6b7280;
}

.detail-rows {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 22px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f3f4f6;
}

.detail-label {
  color: #6b7280;
}

.detail-value {
  color: #111827;
  font-weight: 600;
  text-align: right;
  max-width: 60%;
  word-break: break-word;
}

.resume-link {
  color: #2563eb;
  font-weight: 600;
  font-size: 13px;
  text-decoration: none;
}

.resume-link:hover {
  text-decoration: underline;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.btn-close-modal {
  background: #f3f4f6;
  color: #374151;
  border: none;
  padding: 8px 14px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-close-modal:hover {
  background: #e5e7eb;
}

</style>