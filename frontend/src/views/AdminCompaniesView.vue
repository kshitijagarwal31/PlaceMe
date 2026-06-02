<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Companies</h1>
        <p>Manage all registered companies</p>
      </div>
      <input
        v-model="search"
        class="search-input"
        type="text"
        placeholder="Search by name or industry..."
      />
    </div>

    <div class="table-box">
      <table>
        <thead>
          <tr>
            <th>S.No</th>
            <th>Company</th>
            <th>Email</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(company, index) in filteredCompanies" :key="company.id">
            <td>{{ index + 1 }}</td>
            <td>{{ company.name }}</td>
            <td>{{ company.email }}</td>
            <td>
              <span :class="
                company.status === 'Pending'     ? 'badge-pending'     :
                company.status === 'Active'      ? 'badge-active'      :
                company.status === 'Blacklisted' ? 'badge-blacklisted' :
                'badge-rejected'
              ">{{ company.status }}</span>
            </td>
            <td>
              <div class="actions">
                <template v-if="company.status === 'Pending'">
                  <button class="btn-approve" @click="approveCompany(company)">Approve</button>
                  <button class="btn-reject"  @click="rejectCompany(company)">Reject</button>
                </template>
                <template v-if="company.status === 'Active'">
                  <button class="btn-view"      @click="viewProfile(company)">View Profile</button>
                  <button class="btn-blacklist" @click="blacklistCompany(company)">Blacklist</button>
                </template>
                <template v-if="company.status === 'Blacklisted'">
                  <button class="btn-view"        @click="viewProfile(company)">View Profile</button>
                  <button class="btn-unblacklist" @click="unblacklistCompany(company)">Unblacklist</button>
                </template>
                <template v-if="company.status === 'Rejected'">
                  <span class="text-rejected">—</span>
                </template>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="filteredCompanies.length === 0" class="empty">
        No companies found
      </div>
    </div>

    <div v-if="selectedCompany" class="modal-overlay" @click.self="selectedCompany = null">
      <div class="modal">

        <div class="modal-header">
          <h3>Company Profile</h3>
          <button class="btn-close" @click="selectedCompany = null">✕</button>
        </div>

        <div class="detail-top">
          <div class="avatar-lg">{{ selectedCompany.name.charAt(0) }}</div>
          <div>
            <h4>{{ selectedCompany.name }}</h4>
            <p>{{ selectedCompany.industry }} · {{ selectedCompany.address }}</p>
          </div>
          <span :class="
            selectedCompany.status === 'Active'      ? 'badge-active'      :
            selectedCompany.status === 'Pending'     ? 'badge-pending'     :
            selectedCompany.status === 'Blacklisted' ? 'badge-blacklisted' :
            'badge-rejected'
          ">{{ selectedCompany.status }}</span>
        </div>

        <div class="detail-rows">
          <div class="detail-row">
            <span class="detail-label">Name</span>
            <span class="detail-value">{{ selectedCompany.name }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Email</span>
            <span class="detail-value">{{ selectedCompany.email }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Industry</span>
            <span class="detail-value">{{ selectedCompany.industry }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">HR Contact</span>
            <span class="detail-value">{{ selectedCompany.contact }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Address</span>
            <span class="detail-value">{{ selectedCompany.address }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Website</span>
            <a :href="selectedCompany.website" target="_blank" class="website-link">🌐 {{ selectedCompany.website }}</a>
          </div>
          <div class="detail-row">
            <span class="detail-label">Description</span>
            <span class="detail-value">{{ selectedCompany.description }}</span>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "AdminCompaniesView",

  data() {
    return {
      search:          "",
      selectedCompany: null,
      companies:       [],
    }
  },

  async mounted() {
    const token = localStorage.getItem("token")
    const res = await axios.get("http://localhost:5000/admin/companies", {
      headers: { "Authentication-Token": token }
    })
    const approved = res.data.companies.map(c => ({ ...c, status: "Active" }))
    const pending  = res.data.company_requests.map(c => ({ ...c, status: "Pending" }))
    this.companies = [...approved, ...pending]
  },

  computed: {
    filteredCompanies() {
      const q = this.search.toLowerCase()
      return this.companies.filter(c =>
        c.name.toLowerCase().includes(q) ||
        c.industry.toLowerCase().includes(q)
      )
    },
    companyDrives() {
      if (!this.selectedCompany) return []
      return this.selectedCompany.drives || []
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

    viewProfile(company) {
      this.selectedCompany = company
    },

    async approveCompany(company) {
      await axios.post(`http://localhost:5000/admin/company/approve/${company.id}`, {}, this.getHeaders())
      company.status = "Active"
    },

    async rejectCompany(company) {
      await axios.post(`http://localhost:5000/admin/company/reject/${company.id}`, {}, this.getHeaders())
      company.status = "Rejected"
    },

    async blacklistCompany(company) {
      await axios.post(`http://localhost:5000/admin/company/blacklist/${company.id}`, {}, this.getHeaders())
      company.status = "Blacklisted"
    },

    async unblacklistCompany(company) {
      await axios.post(`http://localhost:5000/admin/company/unblacklist/${company.id}`, {}, this.getHeaders())
      company.status = "Active"
    }

  }
}
</script>

<style scoped>

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 27px;
}

.topbar h1 {
  font-size: 31px;
  color: #111827;
  margin-bottom: 4px;
}

.topbar p {
  color: #6b7280;
  font-size: 14px;
}

.search-input {
  padding: 10px 13px;
  border: 1px solid #e5e7eb;
  border-radius: 9px;
  font-size: 13px;
  color: #111827;
  width: 252px;
  outline: none;
  transition: 0.2s;
  background: white;
}

.search-input:focus {
  border-color: #2563eb;
}

.table-box {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 13px rgba(0, 0, 0, 0.05);
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
  gap: 9px;
  align-items: center;
}

.btn-view {
  background: #eff6ff;
  color: #2563eb;
  border: none;
  padding: 7px 13px;
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
  padding: 7px 13px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-blacklist:hover {
  background: #fecaca;
}

.badge-active {
  background: #dcfce7;
  color: #16a34a;
  padding: 4px 11px;
  border-radius: 18px;
  font-size: 12px;
  font-weight: 600;
}

.badge-blacklisted {
  background: #fee2e2;
  color: #dc2626;
  padding: 4px 11px;
  border-radius: 18px;
  font-size: 12px;
  font-weight: 600;
}

.empty {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  padding: 36px 0;
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
  border-radius: 16px;
  width: 560px;
  max-width: 90%;
  max-height: 85vh;
  overflow-y: auto;
  padding: 25px;
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
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.btn-close {
  background: #f3f4f6;
  border: none;
  width: 29px;
  height: 29px;
  border-radius: 50%;
  font-size: 13px;
  cursor: pointer;
  color: #374151;
}

.detail-top {
  display: flex;
  align-items: center;
  gap: 13px;
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid #f3f4f6;
}

.avatar-lg {
  width: 47px;
  height: 47px;
  border-radius: 50%;
  background: #eff6ff;
  color: #2563eb;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-weight: 700;
  flex-shrink: 0;
}

.detail-top h4 {
  font-size: 14px;
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
  gap: 9px;
  margin-bottom: 25px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  padding-bottom: 9px;
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

.app-section {
  margin-top: 4px;
}

.app-section-title {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 13px;
  display: flex;
  align-items: center;
  gap: 7px;
}

.app-count {
  background: #eff6ff;
  color: #2563eb;
  padding: 2px 9px;
  border-radius: 18px;
  font-size: 12px;
  font-weight: 600;
}

.app-empty {
  text-align: center;
  color: #9ca3af;
  font-size: 13px;
  padding: 18px 0;
}

.app-table-box {
  border-radius: 11px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.app-table {
  width: 100%;
  border-collapse: collapse;
}

.app-table thead {
  background: #f9fafb;
}

.app-table th {
  padding: 11px 14px;
  text-align: left;
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
  border-bottom: 1px solid #e5e7eb;
}

.app-table td {
  padding: 11px 14px;
  font-size: 13px;
  color: #111827;
  border-bottom: 1px solid #f3f4f6;
  font-weight: 500;
}

.app-table tr:last-child td {
  border-bottom: none;
}

.app-table tr:hover td {
  background: #f9fafb;
}

.status-badge {
  padding: 4px 9px;
  border-radius: 18px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.status-pending {
  background: #fef9c3;
  color: #ca8a04;
}

.status-shortlisted {
  background: #dbeafe;
  color: #2563eb;
}

.status-rejected {
  background: #fee2e2;
  color: #dc2626;
}

</style>