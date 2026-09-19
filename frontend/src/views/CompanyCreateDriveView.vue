<template>
  <div>

    <div class="topbar">
      <div>
        <h1>Create Placement Drive</h1>
        <p>Create a new placement drive for students</p>
      </div>
    </div>

    <div class="form-grid">

      <div class="section-box">

        <div class="preview-top">
          <div class="preview-avatar">
            {{ form.job_title ? form.job_title.charAt(0) : "?" }}
          </div>
          <h2>{{ form.job_title || "Job Title" }}</h2>
          <p>{{ form.salary || "Package" }}</p>
        </div>

        <div class="profile-details">

          <div class="detail-row">
            <span class="detail-label">Start Date</span>
            <span class="detail-value">{{ form.start_date || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Last Date</span>
            <span class="detail-value">{{ form.last_date || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Skills Required</span>
            <span class="detail-value">{{ form.skills_required || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Job Description</span>
            <span class="detail-value">{{ form.job_description || "—" }}</span>
          </div>

        </div>

        <div class="info-box">
          <p>After submission, admin will review and approve your drive.</p>
        </div>

      </div>

      <div class="section-box">

        <h3 class="form-title">Drive Details</h3>

        <div class="form-group">
          <label>Job Title <span class="required">*</span></label>
          <input
            v-model="form.job_title"
            type="text"
            placeholder="e.g. Software Engineer"
          />
        </div>

        <div class="form-group">
          <label>Job Description <span class="required">*</span></label>
          <textarea
            v-model="form.job_description"
            placeholder="Describe the job role, responsibilities..."
            rows="4"
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Package / Salary</label>
            <input
              v-model="form.salary"
              type="text"
              placeholder="e.g. 12 LPA"
            />
          </div>
          <div class="form-group">
            <label>Skills Required</label>
            <input
              v-model="form.skills_required"
              type="text"
              placeholder="e.g. Python, React, SQL"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Start Date <span class="required">*</span></label>
            <input v-model="form.start_date" type="date" />
          </div>
          <div class="form-group">
            <label>Last Date to Apply <span class="required">*</span></label>
            <input v-model="form.last_date" type="date" />
          </div>
        </div>

        <div class="form-bottom">
          <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
          <p v-if="submitted" class="save-msg">
            Drive submitted! Waiting for admin approval.
          </p>
          <button class="btn-save" @click="submitDrive">
            Submit Drive
          </button>
        </div>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "CompanyPostDriveView",

  data() {
    return {
      submitted: false,
      errorMsg: "",
      form: {
        job_title: "",
        job_description: "",
        salary: "",
        skills_required: "",
        start_date: "",
        last_date: ""
      }
    }
  },

  methods: {
    getHeaders() {
      return {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    },

    async submitDrive() {
      const required = ["job_title", "job_description", "start_date", "last_date"]
      const allFilled = required.every((field) => this.form[field] !== "")

      if (!allFilled) {
        this.errorMsg = "Please fill all required fields!"
        return
      }

      if (this.form.start_date >= this.form.last_date) {
        this.errorMsg = "Last date must be after start date!"
        return
      }

      this.errorMsg = ""

      try {
        await axios.post(
          "http://localhost:5000/company/create_drive",
          this.form,
          this.getHeaders()
        )

        this.submitted = true

        setTimeout(() => {
          this.submitted = false
          this.form = {
            job_title: "",
            job_description: "",
            salary: "",
            skills_required: "",
            start_date: "",
            last_date: ""
          }
        }, 3000)
      } catch (err) {
        console.error("Drive submit failed:", err)

        if (err.response && err.response.status === 403) {
          this.errorMsg = err.response.data.message
        } else {
          this.errorMsg = "Something went wrong! Try again."
        }
      }
    }
  }
}
</script>

<style scoped>

.topbar {
  margin-bottom: 26px;
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

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1.6fr;
  gap: 16px;
}

.section-box {
  background: white;
  border-radius: 14px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
  padding: 24px;
}

.preview-top {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding-bottom: 18px;
  border-bottom: 1px solid #f3f4f6;
  margin-bottom: 18px;
}

.preview-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #eff6ff;
  color: #2563eb;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 12px;
}

.preview-top h2 {
  font-size: 17px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 3px;
}

.preview-top p {
  font-size: 13px;
  color: #6b7280;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 18px;
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

.info-box {
  background: #eff6ff;
  border-radius: 10px;
  padding: 12px;
  font-size: 13px;
  color: #2563eb;
  line-height: 1.5;
}

.form-title {
  font-size: 17px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 18px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-group {
  margin-bottom: 14px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.required {
  color: #dc2626;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 13px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 13px;
  color: #111827;
  outline: none;
  transition: 0.2s;
  box-sizing: border-box;
  background: white;
  font-family: inherit;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #2563eb;
}

.form-bottom {
  margin-top: 4px;
}

.btn-save {
  width: 100%;
  padding: 11px;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.btn-save:hover {
  background: #1d4ed8;
}

.save-msg {
  color: #16a34a;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
}

.error-msg {
  color: #dc2626;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
}

</style>