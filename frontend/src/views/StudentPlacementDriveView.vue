<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Placement Drives</h1>
        <p>All available placement drives</p>
      </div>
      <input
        v-model="search"
        class="search-input"
        type="text"
        placeholder="Search by company or drive..."
      />
    </div>

    <div v-if="loading" class="empty" style="padding: 60px 0;">
      Loading drives...
    </div>

    <div v-else class="table-box">
      <table>
        <thead>
          <tr>
            <th>S.No</th>
            <th>Company</th>
            <th>Job Title</th>
            <th>Last Date</th>
            <th>Salary</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(drive, index) in filteredDrives" :key="drive.id">
            <td>{{ index + 1 }}</td>
            <td>{{ drive.company }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.end_date }}</td>
            <td>{{ drive.salary || '—' }}</td>
            <td>
              <span :class="
                drive.status === 'Active'  ? 'badge-ongoing'   :
                drive.status === 'Pending' ? 'badge-upcoming'  :
                'badge-completed'
              ">{{ drive.status }}</span>
            </td>
            <td>
              <div class="actions">
                <button class="btn-view" @click="viewDetail(drive)">View Details</button>
                <button
                  class="btn-apply"
                  @click="applyDrive(drive.id)"
                  :disabled="drive.already_applied"
                  :class="{ 'btn-applied': drive.already_applied }"
                >
                  {{ drive.already_applied ? 'Applied ✓' : 'Apply' }}
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="filteredDrives.length === 0" class="empty">
        No drives found
      </div>
    </div>

    <div v-if="selectedDrive" class="modal-overlay" @click.self="selectedDrive = null">
      <div class="modal">

        <div class="modal-header">
          <h3>Drive Details</h3>
          <button class="btn-close" @click="selectedDrive = null">✕</button>
        </div>

        <div v-if="modalLoading" class="empty" style="padding: 40px 0;">
          Loading detail...
        </div>

        <div v-else>
          <div class="detail-top">
            <div class="avatar-lg">{{ selectedDrive.company.charAt(0) }}</div>
            <div>
              <h4>{{ selectedDrive.company }}</h4>
              <p>{{ selectedDrive.job_title }} · {{ selectedDrive.salary || '—' }}</p>
            </div>
            <span :class="
              selectedDrive.status === 'Active'  ? 'badge-ongoing'  :
              selectedDrive.status === 'Pending' ? 'badge-upcoming' :
              'badge-completed'
            ">{{ selectedDrive.status }}</span>
          </div>

          <div class="detail-rows">
            <div class="detail-row">
              <span class="detail-label">Company</span>
              <span class="detail-value">{{ selectedDrive.company }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Job Title</span>
              <span class="detail-value">{{ selectedDrive.job_title }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Salary</span>
              <span class="detail-value">{{ selectedDrive.salary || '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Start Date</span>
              <span class="detail-value">{{ selectedDrive.start_date }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Last Date</span>
              <span class="detail-value">{{ selectedDrive.end_date }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Skills Required</span>
              <span class="detail-value">{{ selectedDrive.skills_required || '—' }}</span>
            </div>
            <div class="detail-row">
              <span class="detail-label">Description</span>
              <span class="detail-value">{{ selectedDrive.description || '—' }}</span>
            </div>
          </div>

          <div class="modal-footer">
            <button class="btn-close-modal" @click="selectedDrive = null">Close</button>
            <button
              class="btn-apply-modal"
              @click="applyDrive(selectedDrive.id)"
              :disabled="selectedDrive.already_applied"
              :class="{ 'btn-applied': selectedDrive.already_applied }"
            >
              {{ selectedDrive.already_applied ? 'Already Applied ✓' : 'Apply Now' }}
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
  name: "StudentPlacementDrivesView",

  data() {
    return {
      loading:       true,
      modalLoading:  false,
      search:        "",
      selectedDrive: null,
      drives:        [],
    }
  },

  async mounted() {
    await this.fetchDrives()
  },

  computed: {
    filteredDrives() {
      const q = this.search.toLowerCase()
      return this.drives.filter(drive =>
        drive.company.toLowerCase().includes(q) ||
        drive.job_title.toLowerCase().includes(q)
      )
    }
  },

  methods: {

    getHeaders() {
      return {
        headers: {
          "Authentication-Token": localStorage.getItem("token"),
        },
      }
    },

    async fetchDrives() {
      this.loading = true
      try {
        const res = await axios.get("http://localhost:5000/student/all_drives", this.getHeaders())
        this.drives = res.data.drives || []
      } catch (err) {
        console.error("Drives load failed:", err)
      } finally {
        this.loading = false
      }
    },

    async viewDetail(drive) {
      this.selectedDrive = drive
      this.modalLoading  = true
      try {
        const res = await axios.get(`http://localhost:5000/student/drive_detail/${drive.id}`, this.getHeaders())
        this.selectedDrive = res.data
      } catch (err) {
        console.error("Drive detail load failed:", err)
      } finally {
        this.modalLoading = false
      }
    },

    async applyDrive(driveId) {
      try {
        await axios.post(`http://localhost:5000/student/apply/${driveId}`, {}, this.getHeaders())
        alert("Applied successfully! ✅")

        const drive = this.drives.find(d => d.id === driveId)
        if (drive) drive.already_applied = true

        if (this.selectedDrive && this.selectedDrive.id === driveId) {
          this.selectedDrive.already_applied = true
        }

      } catch (err) {
        const msg = err.response?.data?.message || "Something went wrong!"
        alert(msg)
      }
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

.actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.btn-view,
.btn-apply {
  padding: 7px 12px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  border: none;
}

.btn-view {
  background: #eff6ff;
  color: #2563eb;
}

.btn-view:hover {
  background: #dbeafe;
}

.btn-apply {
  background: #dcfce7;
  color: #16a34a;
}

.btn-apply:hover {
  background: #bbf7d0;
}

.btn-applied {
  background: #f3f4f6 !important;
  color: #9ca3af !important;
  cursor: not-allowed !important;
}

.badge-upcoming,
.badge-ongoing,
.badge-completed {
  padding: 4px 10px;
  border-radius: 18px;
  font-size: 12px;
  font-weight: 600;
}

.badge-upcoming {
  background: #dbeafe;
  color: #2563eb;
}

.badge-ongoing {
  background: #dcfce7;
  color: #16a34a;
}

.badge-completed {
  background: #dcfce7;
  color: #16a34a;
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

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.btn-close-modal,
.btn-apply-modal {
  padding: 8px 14px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.btn-close-modal {
  background: #f3f4f6;
  color: #374151;
}

.btn-close-modal:hover {
  background: #e5e7eb;
}

.btn-apply-modal {
  background: #dcfce7;
  color: #16a34a;
}

.btn-apply-modal:hover {
  background: #bbf7d0;
}

</style>