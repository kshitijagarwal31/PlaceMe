<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Placement Drives</h1>
        <p>All placement drives</p>
      </div>

      <input
        v-model="search"
        class="search-input"
        type="text"
        placeholder="Search by company, role or status..."
      />
    </div>

    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>S.No</th>
            <th>Company</th>
            <th>Role</th>
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
            <td>{{ drive.company_name }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.end_date }}</td>
            <td>{{ drive.salary }}</td>
            <td>
              <span :class="getStatusClass(drive.status)">
                {{ drive.status }}
              </span>
            </td>
            <td>
              <div class="actions">
                <template v-if="drive.status === 'Pending'">
                  <button class="btn-approve" @click="approveDrive(drive)">
                    Approve
                  </button>
                  <button class="btn-reject" @click="rejectDrive(drive)">
                    Reject
                  </button>
                </template>

                <template v-if="drive.status === 'Active' || drive.status === 'Closed'">
                  <button class="btn-view" @click="viewDetail(drive)">
                    View Detail
                  </button>
                </template>

                <template v-if="drive.status === 'Rejected'">
                  <span class="text-rejected">—</span>
                </template>
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
      @click.self="selectedDrive = null"
    >
      <div class="modal">

        <div class="modal-header">
          <h3>Drive Detail</h3>
          <button class="btn-close" @click="selectedDrive = null">✕</button>
        </div>

        <div class="detail-top">
          <div class="avatar-lg">
            {{ selectedDrive.company_name?.charAt(0) || '?' }}
          </div>

          <div>
            <h4>{{ selectedDrive.company_name }}</h4>
            <p>{{ selectedDrive.job_title }} · {{ selectedDrive.salary }}</p>
          </div>

          <span :class="getStatusClass(selectedDrive.status)">
            {{ selectedDrive.status }}
          </span>
        </div>

        <div class="detail-rows">

          <div class="detail-row">
            <span class="detail-label">Company</span>
            <span class="detail-value">{{ selectedDrive.company_name || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Role</span>
            <span class="detail-value">{{ selectedDrive.job_title || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Package</span>
            <span class="detail-value">{{ selectedDrive.salary || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Start Date</span>
            <span class="detail-value">{{ selectedDrive.start_date || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Last Date</span>
            <span class="detail-value">{{ selectedDrive.end_date || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Skills Required</span>
            <span class="detail-value">{{ selectedDrive.skills_required || '—' }}</span>
          </div>

        </div>

        <div class="modal-footer">
          <button class="btn-close-modal" @click="selectedDrive = null">
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
  name: "AdminPlacementDrivesView",

  data() {
    return {
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
          drive.company_name.toLowerCase().includes(q) ||
          drive.job_title.toLowerCase().includes(q) ||
          drive.status.toLowerCase().includes(q)
        )
      })
    }
  },

  async mounted() {
    const token = localStorage.getItem("token")

    const res = await axios.get("https://placeme-api.up.railway.app/admin/placement_drives", {
      headers: { "Authentication-Token": token }
    })

    const active = res.data.active_drives || []
    const pending = res.data.pending_drives || []
    const closed = res.data.closed_drives || []

    this.drives = [...active, ...pending, ...closed]
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
      if (status === "Active") return "badge-active"
      if (status === "Rejected") return "badge-rejected"
      if (status === "Closed") return "badge-closed"
      return "badge-pending"
    },

    viewDetail(drive) {
      this.selectedDrive = drive
    },

    async approveDrive(drive) {
      await axios.post(
        `https://placeme-api.up.railway.app/admin/placement_drive/approve/${drive.id}`,
        {},
        this.getHeaders()
      )
      drive.status = "Active"
    },

    async rejectDrive(drive) {
      await axios.post(
        `https://placeme-api.up.railway.app/admin/placement_drive/reject/${drive.id}`,
        {},
        this.getHeaders()
      )
      drive.status = "Rejected"
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
  flex-wrap: wrap;
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

.btn-approve {
  background: #dcfce7;
  color: #16a34a;
  border: none;
  padding: 7px 12px;
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
  padding: 7px 12px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-reject:hover {
  background: #fecaca;
}

.text-rejected {
  color: #9ca3af;
  font-size: 14px;
}

.badge-pending {
  background: #fef9c3;
  color: #ca8a04;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.badge-active {
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