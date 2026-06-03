<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Applications</h1>
        <p>All applications for your drives</p>
      </div>

      <input
        v-model="search"
        class="search-input"
        type="text"
        placeholder="Search by student, drive or status..."
      />
    </div>

    <div v-if="loading" class="loading">
      Loading applications...
    </div>

    <!-- TABLE -->
    <div v-else class="table-box">
      <table>
        <thead>
          <tr>
            <th>S.No</th>
            <th>Student</th>
            <th>Drive</th>
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
            <td>{{ application.drive_title }}</td>
            <td>{{ application.apply_date }}</td>
            <td>
              <span :class="getStatusClass(application.status)">
                {{ application.status }}
              </span>
            </td>
            <td>
              <div class="actions">
                <button class="btn-view" @click="viewDetail(application)">
                  View Details
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="filteredApplications.length === 0" class="empty">
        No applications found
      </div>
    </div>

    <!-- MODAL -->
    <div v-if="selectedApp" class="modal-overlay" @click.self="closeModal">
      <div class="modal">

        <div class="modal-header">
          <h3>Application Detail</h3>
          <button class="btn-close" @click="closeModal">✕</button>
        </div>

        <div v-if="modalLoading" class="loading-modal">
          Loading detail...
        </div>

        <div v-else>

          <div class="detail-top">
            <div class="avatar-lg">
              {{ selectedApp.student_name?.charAt(0) || "?" }}
            </div>

            <div class="detail-top-text">
              <h4>{{ selectedApp.student_name }}</h4>
              <p>CGPA {{ selectedApp.cgpa }}</p>
            </div>

            <span :class="getStatusClass(selectedApp.status)">
              {{ selectedApp.status }}
            </span>
          </div>

          <div class="detail-rows">

            <div class="detail-row">
              <span class="detail-label">Drive</span>
              <span class="detail-value">{{ selectedApp.drive_name || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Applied On</span>
              <span class="detail-value">{{ selectedApp.apply_date || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Email</span>
              <span class="detail-value">{{ selectedApp.email || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Skills</span>
              <span class="detail-value">{{ selectedApp.skills || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Bio</span>
              <span class="detail-value">{{ selectedApp.bio || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Resume</span>
              <a
                v-if="selectedApp.resume"
                :href="selectedApp.resume"
                target="_blank"
                class="resume-link"
              >
                View Resume
              </a>
              <span v-else class="detail-value">—</span>
            </div>

            <template v-if="selectedApp.interview_date">
              <div class="detail-row">
                <span class="detail-label">Interview Date</span>
                <span class="detail-value">{{ selectedApp.interview_date }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Interview Time</span>
                <span class="detail-value">{{ selectedApp.interview_time }}</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Interview Location</span>
                <span class="detail-value">{{ selectedApp.interview_location }}</span>
              </div>
            </template>

          </div>

          <div v-if="selectedApp.status === 'Shortlisted'" class="schedule-section">
            <div class="schedule-title">Schedule Interview</div>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Date <span class="required">*</span></label>
                <input
                  v-model="interview.date"
                  type="date"
                  class="form-input"
                  :min="todayDate"
                />
              </div>
              <div class="form-group">
                <label class="form-label">Time <span class="required">*</span></label>
                <input v-model="interview.time" type="time" class="form-input" />
              </div>
            </div>

            <div class="form-group form-group-full">
              <label class="form-label">Location / Meeting Link <span class="required">*</span></label>
              <input
                v-model="interview.location"
                type="text"
                class="form-input"
                placeholder="e.g. Room 301 or https://meet.google.com/xyz"
              />
            </div>

            <div v-if="scheduleError" class="error-msg">
              {{ scheduleError }}
            </div>
          </div>

          <div class="feedback-section">
            <label class="feedback-label">Feedback</label>
            <textarea
              v-model="feedback"
              class="feedback-input"
              placeholder="Write feedback for this student..."
              rows="3"
            ></textarea>
          </div>

          <div v-if="selectedApp.status === 'Pending'" class="modal-actions">
            <button class="btn-shortlist" @click="updateStatus('Shortlisted')">
              Shortlist
            </button>
            <button class="btn-reject" @click="updateStatus('Rejected')">
              Reject
            </button>
          </div>

          <div v-else-if="selectedApp.status === 'Shortlisted'" class="modal-actions">
            <button
              class="btn-schedule"
              @click="confirmSchedule"
              :disabled="scheduleLoading"
            >
              {{ scheduleLoading ? "Scheduling..." : "Confirm Schedule" }}
            </button>
            <button class="btn-reject" @click="updateStatus('Rejected')">
              Reject
            </button>
          </div>

          <div v-else-if="selectedApp.status === 'Interview Scheduled'" class="modal-actions">
            <button class="btn-select" @click="updateStatus('Selected')">
              Selected
            </button>
            <button class="btn-reject" @click="updateStatus('Rejected')">
              Reject
            </button>
          </div>

          <div v-else class="modal-actions">
            <button class="btn-feedback" @click="saveFeedback">
              Save Feedback
            </button>
          </div>

        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyApplicationsView",

  data() {
    return {
      loading: true,
      modalLoading: false,
      scheduleLoading: false,
      scheduleError: "",
      search: "",
      selectedApp: null,
      feedback: "",
      applications: [],
      interview: {
        date: "",
        time: "",
        location: ""
      }
    }
  },

  computed: {
    filteredApplications() {
      const q = this.search.toLowerCase()

      return this.applications.filter((application) => {
        return (
          application.student_name.toLowerCase().includes(q) ||
          application.drive_title.toLowerCase().includes(q) ||
          application.status.toLowerCase().includes(q)
        )
      })
    },

    todayDate() {
      return new Date().toISOString().split("T")[0]
    }
  },

  async mounted() {
    await this.fetchApplications()
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

    async fetchApplications() {
      this.loading = true

      try {
        const res = await axios.get(
          "http://localhost:5000/company/dashboard_data",
          this.getHeaders()
        )
        this.applications = res.data.applications || []
      } catch (err) {
        console.error("Applications load failed:", err)
      } finally {
        this.loading = false
      }
    },

    async viewDetail(application) {
      this.selectedApp = application
      this.modalLoading = true
      this.feedback = ""
      this.scheduleError = ""
      this.interview = { date: "", time: "", location: "" }

      try {
        const res = await axios.get(
          `http://localhost:5000/company/application_detail/${application.id}`,
          this.getHeaders()
        )
        this.selectedApp = res.data
        this.feedback = res.data.feedback || ""
      } catch (err) {
        console.error("Application detail load failed:", err)
      } finally {
        this.modalLoading = false
      }
    },

    async updateStatus(status) {
      try {
        await axios.patch(
          `http://localhost:5000/company/application_update/${this.selectedApp.id}`,
          { status, feedback: this.feedback },
          this.getHeaders()
        )

        const application = this.applications.find(
          (item) => item.id === this.selectedApp.id
        )
        if (application) application.status = status

        this.closeModal()
      } catch (err) {
        console.error("Status update failed:", err)
      }
    },

    async saveFeedback() {
      try {
        await axios.patch(
          `http://localhost:5000/company/application_update/${this.selectedApp.id}`,
          { status: this.selectedApp.status, feedback: this.feedback },
          this.getHeaders()
        )
        alert("Feedback saved!")
      } catch (err) {
        console.error("Feedback save failed:", err)
      }
    },

    async confirmSchedule() {
      if (!this.interview.date || !this.interview.time || !this.interview.location) {
        this.scheduleError = "Please fill Date, Time and Location."
        return
      }

      this.scheduleLoading = true
      this.scheduleError = ""

      try {
        await axios.patch(
          `http://localhost:5000/company/application_update/${this.selectedApp.id}`,
          {
            status: "Interview Scheduled",
            feedback: this.feedback,
            interview_date: this.interview.date,
            interview_time: this.interview.time,
            interview_location: this.interview.location
          },
          this.getHeaders()
        )

        const application = this.applications.find(
          (item) => item.id === this.selectedApp.id
        )
        if (application) application.status = "Interview Scheduled"

        this.closeModal()
        alert("Interview scheduled!")
      } catch (err) {
        this.scheduleError = "Failed to schedule. Please try again."
        console.error("Schedule failed:", err)
      } finally {
        this.scheduleLoading = false
      }
    },

    closeModal() {
      this.selectedApp = null
      this.feedback = ""
      this.scheduleError = ""
      this.interview = { date: "", time: "", location: "" }
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

.loading {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  padding: 60px 0;
}

.loading-modal {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  padding: 40px 0;
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

.actions {
  display: flex;
  gap: 8px;
  align-items: center;
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

.badge-selected {
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
  padding-bottom: 14px;
  border-bottom: 1px solid #f3f4f6;
  position: sticky;
  top: 0;
  background: white;
  z-index: 1;
}

.modal-header h3 {
  font-size: 17px;
  font-weight: 600;
  color: #111827;
}

.btn-close {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: none;
  background: #f3f4f6;
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

.detail-top-text {
  flex: 1;
  min-width: 0;
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
}

.detail-top p {
  font-size: 12px;
  color: #6b7280;
}

.detail-rows {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
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
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
}

.resume-link:hover {
  text-decoration: underline;
}

.schedule-section {
  background: #f8faff;
  border: 1px solid #e0eaff;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 18px;
}

.schedule-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e40af;
  margin-bottom: 14px;
}

.form-row {
  display: flex;
  gap: 12px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group-full {
  margin-top: 12px;
}

.form-label {
  font-size: 13px;
  color: #6b7280;
  font-weight: 600;
}

.required {
  color: #dc2626;
}

.form-input {
  padding: 9px 11px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  outline: none;
  transition: 0.2s;
  background: white;
  color: #111827;
}

.form-input:focus {
  border-color: #2563eb;
}

.error-msg {
  margin-top: 10px;
  background: #fee2e2;
  color: #dc2626;
  font-size: 13px;
  padding: 8px 12px;
  border-radius: 8px;
}

.feedback-section {
  margin-bottom: 18px;
}

.feedback-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 7px;
}

.feedback-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  outline: none;
  resize: vertical;
  font-family: inherit;
  color: #111827;
  transition: 0.2s;
}

.feedback-input:focus {
  border-color: #2563eb;
}

.modal-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-shortlist,
.btn-schedule,
.btn-select,
.btn-reject,
.btn-feedback {
  flex: 1;
  padding: 10px 14px;
  font-size: 13px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
  min-width: 120px;
}

.btn-shortlist {
  background: #dcfce7;
  color: #16a34a;
}

.btn-shortlist:hover {
  background: #bbf7d0;
}

.btn-schedule {
  background: #eff6ff;
  color: #2563eb;
}

.btn-schedule:hover {
  background: #dbeafe;
}

.btn-schedule:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-select {
  background: #dcfce7;
  color: #16a34a;
}

.btn-select:hover {
  background: #bbf7d0;
}

.btn-reject {
  background: #fee2e2;
  color: #dc2626;
}

.btn-reject:hover {
  background: #fecaca;
}

.btn-feedback {
  background: #f3f4f6;
  color: #374151;
}

.btn-feedback:hover {
  background: #e5e7eb;
}

</style>