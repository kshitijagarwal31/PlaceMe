<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Placement Drives</h1>
        <p>All your posted placement drives</p>
      </div>

      <input
        v-model="search"
        class="search-input"
        type="text"
        placeholder="Search by role or status..."
      />
    </div>

    <div v-if="loading" class="loading">
      Loading drives...
    </div>

    <div v-else class="table-box">
      <table>
        <thead>
          <tr>
            <th>S.No</th>
            <th>Role</th>
            <th>Start Date</th>
            <th>Last Date</th>
            <th>Package</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="(drive, index) in filteredDrives"
            :key="drive.id"
          >
            <td>{{ index + 1 }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.start_date }}</td>
            <td>{{ drive.end_date }}</td>
            <td>{{ drive.salary || "—" }}</td>
            <td>
              <span :class="getStatusClass(drive.status)">
                {{ drive.status }}
              </span>
            </td>
            <td>
              <div class="actions">
                <button class="btn-view" @click="viewDetail(drive)">
                  View Detail
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

    <div
      v-if="selectedDrive"
      class="modal-overlay"
      @click.self="closeModal"
    >
      <div class="modal">

        <div class="modal-header">
          <h3>Drive Detail</h3>
          <button class="btn-close" @click="closeModal">✕</button>
        </div>

        <div v-if="modalLoading" class="loading-modal">
          Loading detail...
        </div>

        <div v-else>

          <div class="detail-top">
            <div class="avatar-lg">
              {{ selectedDrive.job_title?.charAt(0) || "?" }}
            </div>

            <div class="detail-top-text">
              <h4>{{ selectedDrive.job_title }}</h4>
              <p>{{ selectedDrive.salary || "Package not mentioned" }}</p>
            </div>

            <span :class="getStatusClass(selectedDrive.status)">
              {{ selectedDrive.status }}
            </span>
          </div>

          <div class="detail-rows">

            <div class="detail-row">
              <span class="detail-label">Role</span>
              <span class="detail-value">{{ selectedDrive.job_title || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Package</span>
              <span class="detail-value">{{ selectedDrive.salary || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Start Date</span>
              <span class="detail-value">{{ selectedDrive.start_date || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Last Date</span>
              <span class="detail-value">{{ selectedDrive.end_date || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Skills Required</span>
              <span class="detail-value">{{ selectedDrive.skills_required || "—" }}</span>
            </div>

            <div class="detail-row">
              <span class="detail-label">Description</span>
              <span class="detail-value">{{ selectedDrive.description || "—" }}</span>
            </div>

          </div>

          <div class="modal-footer">
            <button class="btn-close-modal" @click="closeModal">
              Close
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
  name: "CompanyDrivesView",

  data() {
    return {
      loading: true,
      modalLoading: false,
      search: "",
      selectedDrive: null,
      drives: []
    }
  },

  computed: {
    filteredDrives() {
      const q = this.search.toLowerCase()

      return this.drives.filter((drive) => {
        return (
          drive.job_title.toLowerCase().includes(q) ||
          drive.status.toLowerCase().includes(q)
        )
      })
    }
  },

  async mounted() {
    await this.fetchDrives()
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
      if (status === "Active") return "badge-active"
      if (status === "Pending") return "badge-pending"
      if (status === "Rejected") return "badge-rejected"
      if (status === "Closed") return "badge-closed"
      return "badge-closed"
    },

    async fetchDrives() {
      this.loading = true

      try {
        const res = await axios.get(
          "https://placeme-api.up.railway.app/company/my_drives",
          this.getHeaders()
        )
        this.drives = res.data.drives || []
      } catch (err) {
        console.error("Drives load failed:", err)
      } finally {
        this.loading = false
      }
    },

    async viewDetail(drive) {
      this.selectedDrive = drive
      this.modalLoading = true

      try {
        const res = await axios.get(
          `https://placeme-api.up.railway.app/company/drive_detail/${drive.id}`,
          this.getHeaders()
        )
        this.selectedDrive = res.data
      } catch (err) {
        console.error("Drive detail load failed:", err)
      } finally {
        this.modalLoading = false
      }
    },

    closeModal() {
      this.selectedDrive = null
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

.badge-active {
  background: #dcfce7;
  color: #16a34a;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.badge-pending {
  background: #fef9c3;
  color: #ca8a04;
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

.badge-closed {
  background: #f3f4f6;
  color: #4b5563;
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