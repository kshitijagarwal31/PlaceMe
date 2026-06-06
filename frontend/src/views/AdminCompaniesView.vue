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
          <tr
            v-for="(company, index) in filteredCompanies"
            :key="company.id"
          >
            <td>{{ index + 1 }}</td>
            <td>{{ company.name }}</td>
            <td>{{ company.email }}</td>
            <td>
              <span :class="getStatusClass(company.status)">
                {{ company.status }}
              </span>
            </td>
            <td>
              <div class="actions">
                <template v-if="company.status === 'Pending'">
                  <button class="btn-approve" @click="approveCompany(company)">
                    Approve
                  </button>
                  <button class="btn-reject" @click="rejectCompany(company)">
                    Reject
                  </button>
                </template>

                <template v-if="company.status === 'Active'">
                  <button class="btn-view" @click="viewProfile(company)">
                    View Profile
                  </button>
                  <button class="btn-blacklist" @click="blacklistCompany(company)">
                    Blacklist
                  </button>
                </template>

                <template v-if="company.status === 'Blacklisted'">
                  <button class="btn-view" @click="viewProfile(company)">
                    View Profile
                  </button>
                  <button class="btn-unblacklist" @click="unblacklistCompany(company)">
                    Unblacklist
                  </button>
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

    <div
      v-if="selectedCompany"
      class="modal-overlay"
      @click.self="selectedCompany = null"
    >
      <div class="modal">

        <div class="modal-header">
          <h3>Company Profile</h3>
          <button class="btn-close" @click="selectedCompany = null">✕</button>
        </div>

        <div class="detail-top">
          <div class="avatar-lg">
            {{ selectedCompany.name?.charAt(0) || '?' }}
          </div>

          <div>
            <h4>{{ selectedCompany.name }}</h4>
            <p>{{ selectedCompany.industry }} · {{ selectedCompany.address }}</p>
          </div>

          <span :class="getStatusClass(selectedCompany.status)">
            {{ selectedCompany.status }}
          </span>
        </div>

        <div class="detail-rows">

          <div class="detail-row">
            <span class="detail-label">Name</span>
            <span class="detail-value">{{ selectedCompany.name || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Email</span>
            <span class="detail-value">{{ selectedCompany.email || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Industry</span>
            <span class="detail-value">{{ selectedCompany.industry || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">HR Contact</span>
            <span class="detail-value">{{ selectedCompany.contact || '—' }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Address</span>
            <span class="detail-value">{{ selectedCompany.address || '—' }}</span>
          </div>

          <div class="detail-row" v-if="selectedCompany.website">
            <span class="detail-label">Website</span>
            <a
              :href="selectedCompany.website"
              target="_blank"
              class="website-link"
            >
              {{ selectedCompany.website }}
            </a>
          </div>

          <div class="detail-row">
            <span class="detail-label">Description</span>
            <span class="detail-value">{{ selectedCompany.description || '—' }}</span>
          </div>

        </div>

        <div class="modal-footer">
          <button class="btn-close-modal" @click="selectedCompany = null">
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
  name: "AdminCompaniesView",

  data() {
    return {
      search: "",
      selectedCompany: null,
      companies: []
    }
  },

  computed: {
    filteredCompanies() {
      const q = this.search.toLowerCase()

      return this.companies.filter((company) => {
        return (
          company.name.toLowerCase().includes(q) ||
          company.industry.toLowerCase().includes(q) ||
          company.status.toLowerCase().includes(q)
        )
      })
    }
  },

  async mounted() {
    const token = localStorage.getItem("token")

    const res = await axios.get("http://localhost:5000/admin/companies", {
      headers: { "Authentication-Token": token }
    })

    const approved = res.data.companies.map((company) => ({
      ...company,
      status: company.is_active ? "Active" : "Blacklisted"
    }))

    const pending = res.data.company_requests.map((company) => ({
      ...company,
      status: "Pending"
    }))

    this.companies = [...approved, ...pending]
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
      if (status === "Blacklisted") return "badge-blacklisted"
      if (status === "Rejected") return "badge-rejected"
      return "badge-pending"
    },

    viewProfile(company) {
      this.selectedCompany = company
    },

    async approveCompany(company) {
      await axios.post(
        `http://localhost:5000/admin/company/approve/${company.id}`,
        {},
        this.getHeaders()
      )
      company.status = "Active"
    },

    async rejectCompany(company) {
      await axios.post(
        `http://localhost:5000/admin/company/reject/${company.id}`,
        {},
        this.getHeaders()
      )
      company.status = "Rejected"
    },

    async blacklistCompany(company) {
      await axios.post(
        `http://localhost:5000/admin/company/blacklist/${company.id}`,
        {},
        this.getHeaders()
      )
      company.status = "Blacklisted"
    },

    async unblacklistCompany(company) {
      await axios.post(
        `http://localhost:5000/admin/company/unblacklist/${company.id}`,
        {},
        this.getHeaders()
      )
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

.text-rejected {
  color: #9ca3af;
  font-size: 14px;
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

.badge-blacklisted {
  background: #fee2e2;
  color: #dc2626;
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

.website-link {
  color: #2563eb;
  font-weight: 600;
  font-size: 13px;
  text-decoration: none;
  text-align: right;
  max-width: 60%;
  word-break: break-word;
}

.website-link:hover {
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