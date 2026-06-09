<template>
  <div>

    <div class="topbar">
      <div>
        <h1>My Profile</h1>
        <p>Fill your details to unlock full features and start applying</p>
      </div>
    </div>

    <div v-if="loading" class="loading">
      Loading profile...
    </div>

    <div v-else class="profile-grid">

      <div class="section-box preview-box">

        <div class="profile-top">
          <div class="profile-avatar">
            {{ form.name ? form.name.charAt(0) : "?" }}
          </div>
          <h2>{{ form.name || "Your Name" }}</h2>
          <p>{{ form.username ? "@" + form.username : "@username" }}</p>
        </div>

        <div class="preview-details">

          <div class="detail-row">
            <span class="detail-label">Email</span>
            <span class="detail-value">{{ form.email || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">College</span>
            <span class="detail-value">{{ form.college || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">CGPA</span>
            <span class="detail-value">{{ form.cgpa || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Skills</span>
            <span class="detail-value">{{ form.skills || "—" }}</span>
          </div>

          <div class="detail-row">
            <span class="detail-label">Resume</span>
            <span class="detail-value">{{ form.resume ? "Uploaded" : "—" }}</span>
          </div>

        </div>

        <div class="info-box">
          <p>Complete your profile to start applying for placement drives.</p>
        </div>

      </div>

      <div class="section-box form-box">

        <h3 class="form-title">Personal Information</h3>

        <div class="form-row">
          <div class="form-group">
            <label>Full Name <span class="required">*</span></label>
            <input v-model="form.name" type="text" placeholder="Rahul Sharma" />
          </div>
          <div class="form-group">
            <label>Username <span class="required">*</span></label>
            <input v-model="form.username" type="text" placeholder="rahul_sharma" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Email <span class="required">*</span></label>
            <input v-model="form.email" type="email" placeholder="rahul@college.com" />
          </div>
          <div class="form-group">
            <label>CGPA <span class="required">*</span></label>
            <input v-model="form.cgpa" type="text" placeholder="8.7" />
          </div>
        </div>

        <div class="form-group">
          <label>College Name <span class="required">*</span></label>
          <input
            v-model="form.college"
            type="text"
            placeholder="IIT Delhi / ABC Engineering College"
          />
        </div>

        <div class="form-group">
          <label>Skills <span class="required">*</span></label>
          <input
            v-model="form.skills"
            type="text"
            placeholder="Vue.js, Python, Java, React, Node.js"
          />
        </div>

        <div class="form-group">
          <label>Bio / About Yourself</label>
          <textarea
            v-model="form.bio"
            placeholder="Write something about yourself..."
            rows="4"
          ></textarea>
        </div>

        <div class="form-group">
        <label>Resume (PDF) <span class="required">*</span></label>

        <div v-if="form.resume && !newResume" class="resume-existing">
          <a :href="'http://placeme-api.up.railway.app' + form.resume" target="_blank" class="resume-link">
            View Current Resume
          </a>
          <button class="btn-change-resume" @click="newResume = true">
            Change Resume
          </button>
        </div>

          <input
            v-else
            type="file"
            accept=".pdf"
            class="file-input"
            @change="handleResumeUpload"
          />
        </div>

        <div class="form-bottom">
          <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
          <p v-if="successMsg" class="success-msg">Profile updated successfully!</p>
          <button class="btn-save" @click="saveProfile">
            Save & Continue
          </button>
        </div>

      </div>

    </div>

  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "StudentCompleteProfile",

  data() {
    return {
      loading: true,
      errorMsg: "",
      successMsg: false,
      newResume: false,
      resumeFile: null,
      form: {
        name: "",
        username: "",
        email: "",
        college: "",
        cgpa: "",
        skills: "",
        bio: "",
        resume: ""
      }
    }
  },

  async mounted() {
    await this.fetchProfile()
  },

  methods: {
    getHeaders() {
      return {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    },

    async fetchProfile() {
      this.loading = true

      try {
        const res = await axios.get(
          "http://placeme-api.up.railway.app/student/complete_profile",
          this.getHeaders()
        )
        const data = res.data

        this.form.name = data.name || ""
        this.form.username = data.username || ""
        this.form.email = data.email || ""
        this.form.college = data.college_name || ""
        this.form.cgpa = data.cgpa || ""
        this.form.skills = data.skills || ""
        this.form.bio = data.bio || ""
        this.form.resume = data.resume || ""
      } catch (err) {
        console.error("Profile load failed:", err)
      } finally {
        this.loading = false
      }
    },

    handleResumeUpload(event) {
      this.resumeFile = event.target.files[0]
    },

    async saveProfile() {
      const required = ["name", "username", "email", "college", "cgpa", "skills"]
      const allFilled = required.every((field) => this.form[field] !== "")

      if (!allFilled) {
        this.errorMsg = "Please fill all required fields!"
        return
      }

      if (!this.form.resume && !this.resumeFile) {
        this.errorMsg = "Please upload your resume!"
        return
      }

      this.errorMsg = ""

      try {
        const formData = new FormData()
        formData.append("name", this.form.name)
        formData.append("username", this.form.username)
        formData.append("email", this.form.email)
        formData.append("college_name", this.form.college)
        formData.append("cgpa", this.form.cgpa)
        formData.append("skills", this.form.skills)
        formData.append("bio", this.form.bio)

        if (this.resumeFile) {
          formData.append("resume", this.resumeFile)
        }

        await axios.put(
          "http://placeme-api.up.railway.app/student/complete_profile",
          formData,
          {
            headers: {
              "Authentication-Token": localStorage.getItem("token"),
              "Content-Type": "multipart/form-data"
            }
          }
        )

        this.successMsg = true
        this.newResume = false
        await this.fetchProfile()

        setTimeout(() => {
          this.successMsg = false
        }, 3000)
      } catch (err) {
        console.error("Profile save failed:", err)
        this.errorMsg = err.response?.data?.message || "Something went wrong!"
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

.loading {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  padding: 60px 0;
}

.profile-grid {
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

.preview-box {
  text-align: center;
}

.profile-top {
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: #eff6ff;
  color: #2563eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 12px;
}

.profile-top h2 {
  font-size: 17px;
  color: #111827;
  margin-bottom: 3px;
}

.profile-top p {
  color: #6b7280;
  font-size: 13px;
}

.preview-details {
  text-align: left;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f3f4f6;
  font-size: 13px;
}

.detail-label {
  color: #6b7280;
}

.detail-value {
  font-weight: 600;
  color: #111827;
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
  margin-top: 18px;
  text-align: left;
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
  margin-bottom: 6px;
  font-weight: 600;
  color: #374151;
  font-size: 13px;
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
  outline: none;
  box-sizing: border-box;
  font-family: inherit;
  transition: 0.2s;
  color: #111827;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #2563eb;
}

.file-input {
  width: 100%;
  padding: 8px;
  border: 1px dashed #cbd5e1;
  border-radius: 8px;
  background: #f8fafc;
  box-sizing: border-box;
}

.resume-existing {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
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

.btn-change-resume {
  background: #f3f4f6;
  color: #374151;
  border: none;
  padding: 6px 12px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.btn-change-resume:hover {
  background: #e5e7eb;
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

.success-msg {
  color: #16a34a;
  font-weight: 600;
  text-align: center;
  margin-bottom: 8px;
  font-size: 13px;
}

.error-msg {
  color: #dc2626;
  font-weight: 600;
  text-align: center;
  margin-bottom: 8px;
  font-size: 13px;
}

</style>