<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Students</h1>
        <p>All registered students</p>
      </div>

      <input
        v-model="search"
        class="search-input"
        type="text"
        placeholder="Search by name or email..."
      />
    </div>

    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>S.No</th>
            <th>Name</th>
            <th>Email</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="(student, index) in filteredStudents"
            :key="student.id"
          >
            <td>{{ index + 1 }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.email }}</td>
            <td>
              <span :class="getStatusClass(student.is_active)">
                {{ student.is_active ? "Active" : "Blacklisted" }}
              </span>
            </td>
            <td>
              <div class="actions">
                <button class="btn-view" @click="viewProfile(student)">
                  View Profile
                </button>
                <button
                  v-if="student.is_active"
                  class="btn-blacklist"
                  @click="blacklistStudent(student)"
                >
                  Blacklist
                </button>
                <button
                  v-else
                  class="btn-unblacklist"
                  @click="unblacklistStudent(student)"
                >
                  Unblacklist
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="filteredStudents.length === 0" class="empty">
        No students found
      </div>
    </div>

    <div
      v-if="selectedStudent"
      class="modal-overlay"
      @click.self="selectedStudent = null"
    >
      <div class="modal">

        <div class="modal-header">
          <h3>Student Profile</h3>
          <button class="btn-close" @click="selectedStudent = null">✕</button>
        </div>

        <div class="detail-top">
          <div class="avatar-lg">
            {{ selectedStudent.name?.charAt(0) || "?" }}
          </div>

          <div>
            <h4>{{ selectedStudent.name }}</h4>
            <p>{{ selectedStudent.college }} · CGPA {{ selectedStudent.cgpa }}</p>
          </div>

          <span :class="getStatusClass(selectedStudent.is_active)">
            {{ selectedStudent.is_active ? "Active" : "Blacklisted" }}
          </span>
        </div>

        <div class="detail-rows">

          <div class="detail-row">
            <span class="detail-label">Name</span>
            <span class="detail-value">{{ selectedStudent.name || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Username</span>
            <span class="detail-value">{{ selectedStudent.username || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Email</span>
            <span class="detail-value">{{ selectedStudent.email || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">CGPA</span>
            <span class="detail-value">{{ selectedStudent.cgpa || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">College</span>
            <span class="detail-value">{{ selectedStudent.college || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Skills</span>
            <span class="detail-value">{{ selectedStudent.skills || "—" }}</span>
          </div>

          <div class="detail-row" v-if="selectedStudent.resume">
            <span class="detail-label">Resume</span>
            <a
               :href="'http://placeme-api.up.railway.app' + selectedStudent.resume"
                target="_blank"
                class="resume-link"
              >
              View Resume
            </a>
          </div>

        </div>

        <div class="modal-footer">
          <button class="btn-close-modal" @click="selectedStudent = null">
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
  name: "AdminStudentsView",

  data() {
    return {
      search: "",
      selectedStudent: null,
      students: []
    }
  },

  computed: {
    filteredStudents() {
      const q = this.search.toLowerCase()

      return this.students.filter((student) => {
        const statusText = student.is_active ? "active" : "blacklisted"

        return (
          student.name.toLowerCase().includes(q) ||
          student.email.toLowerCase().includes(q) ||
          statusText.includes(q)
        )
      })
    }
  },

  async mounted() {
    const token = localStorage.getItem("token")

    const res = await axios.get("http://placeme-api.up.railway.app/admin/students", {
      headers: { "Authentication-Token": token }
    })

    this.students = res.data.students || []
  },

  methods: {
    getHeaders() {
      return {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    },

    getStatusClass(isActive) {
      if (isActive) return "badge-active"
      return "badge-blacklisted"
    },

    viewProfile(student) {
      this.selectedStudent = student
    },

    async blacklistStudent(student) {
      await axios.post(
        `http://placeme-api.up.railway.app/admin/student/blacklist/${student.id}`,
        {},
        this.getHeaders()
      )
      student.is_active = false
    },

    async unblacklistStudent(student) {
      await axios.post(
        `http://placeme-api.up.railway.app/admin/student/unblacklist/${student.id}`,
        {},
        this.getHeaders()
      )
      student.is_active = true
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

.btn-blacklist {
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

.btn-blacklist:hover {
  background: #fecaca;
}

.btn-unblacklist {
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

.btn-unblacklist:hover {
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

.badge-blacklisted {
  background: #fee2e2;
  color: #dc2626;
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