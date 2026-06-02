<template>

  <div class="home">

    <Navbar />

    <main class="main-content">

      <section class="hero">

        <div class="hero-left">

          <p class="hero-small-text">
            SMART COLLEGE PLACEMENT PLATFORM
          </p>

          <h1>
            Connecting Students <br />
            With Top Companies
          </h1>

          <p class="hero-description">
            PlaceMe helps students discover opportunities, apply for jobs,
            track applications and connect with leading companies from one platform.
          </p>

          <div class="hero-buttons">

            <router-link to="/register" class="primary-btn">
              Get Started
            </router-link>

            <router-link to="/login" class="secondary-btn">
              Sign In
            </router-link>

          </div>

        </div>

        <div class="hero-right">

          <div class="dashboard-card">

            <div class="dashboard-top">

              <h3>
                Placement Overview
              </h3>

              <span class="live-badge">
                Live
              </span>

            </div>

            <div class="stats-grid">

              <div class="stat-box">
                <h2>500+</h2>
                <p>Companies</p>
              </div>

              <div class="stat-box">
                <h2>10K+</h2>
                <p>Students</p>
              </div>

              <div class="stat-box">
                <h2>95%</h2>
                <p>Placement</p>
              </div>

              <div class="stat-box">
                <h2>1.2K+</h2>
                <p>Job Posts</p>
              </div>

            </div>

          </div>

        </div>

      </section>

      <section class="features-section">

        <div class="section-heading">

          <h2>
            Why Choose PlaceMe?
          </h2>

          <p>
            Everything required to manage placements efficiently.
          </p>

        </div>

        <div class="features-grid">

          <div class="feature-card">

            <div class="feature-icon">
              🎓
            </div>

            <h3>
              Student Profiles
            </h3>

            <p>
              Create profiles, upload resumes and manage placement details.
            </p>

          </div>

          <div class="feature-card">

            <div class="feature-icon">
              🏢
            </div>

            <h3>
              Company Access
            </h3>

            <p>
              Companies can post jobs and shortlist candidates easily.
            </p>

          </div>

          <div class="feature-card">

            <div class="feature-icon">
              📄
            </div>

            <h3>
              Easy Applications
            </h3>

            <p>
              Apply to internships and jobs in just a few clicks.
            </p>

          </div>

          <div class="feature-card">

            <div class="feature-icon">
              📊
            </div>

            <h3>
              Placement Tracking
            </h3>

            <p>
              Monitor applications, interviews and placement status.
            </p>

          </div>

        </div>

      </section>

    </main>

    <footer class="footer">

      <p>
        © 2026 PlaceMe Portal. All Rights Reserved.
      </p>

    </footer>

  </div>

</template>

<script>

import Navbar from "../components/Navbar.vue"

export default {
  name: "HomeView",
  components:{
    Navbar
  }
}

</script>

<style scoped>

.hero{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:54px 40px;
  gap:27px;
}

.hero-small-text{
  font-size:11px;
  margin-bottom:13px;
}

.hero-left h1{
  font-size:43px;
  line-height:1.2;
  margin-bottom:16px;
}

.hero-description{
  color:#6b7280;
  font-size:14px;
  line-height:1.7;
  max-width:500px;
  margin-bottom:25px;
}

.hero-buttons{
  display:flex;
  gap:12px;
}

.primary-btn{
  text-decoration:none;
  background:#2563eb;
  color:white;
  padding:11px 22px;
  border-radius:8px;
  font-weight:bold;
  font-size:13px;
  transition:0.2s;
}

.secondary-btn{
  text-decoration:none;
  border:2px solid #2563eb;
  color:#2563eb;
  padding:11px 22px;
  border-radius:8px;
  font-weight:bold;
  font-size:13px;
  transition:0.2s;
}

.hero-right{
  flex:1;
  display:flex;
  justify-content:center;
}

.dashboard-card{
  width:100%;
  max-width:340px;
  background:white;
  border-radius:16px;
  padding:22px;
  box-shadow:0 10px 35px rgba(0,0,0,0.08);
}

.dashboard-top{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:18px;
}

.dashboard-top h3{
  font-size:18px;
}

.live-badge{
  background:#dcfce7;
  color:#16a34a;
  padding:5px 10px;
  border-radius:20px;
  font-size:11px;
  font-weight:bold;
}

.stats-grid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:12px;
}

.stat-box{
  background:#f9fafb;
  border-radius:12px;
  padding:18px 12px;
  text-align:center;
}

.stat-box h2{
  color:#2563eb;
  font-size:24px;
  margin-bottom:6px;
}

.stat-box p{
  color:#6b7280;
  font-weight:bold;
  font-size:12px;
}

.features-section{
  padding:18px 40px 60px;
}

.section-heading{
  text-align:center;
  margin-bottom:35px;
}

.section-heading h2{
  font-size:32px;
  margin-bottom:8px;
}

.section-heading p{
  color:#6b7280;
  font-size:13px;
}

.features-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:18px;
}

.feature-card{
  background:white;
  padding:22px 18px;
  border-radius:16px;
  text-align:center;
  box-shadow:0 3px 15px rgba(0,0,0,0.05);
  transition:0.2s;
}

.feature-card:hover{
  transform:translateY(-4px);
}

.feature-icon{
  font-size:38px;
  margin-bottom:14px;
}

.feature-card h3{
  margin-bottom:10px;
  font-size:18px;
}

.feature-card p{
  color:#6b7280;
  line-height:1.6;
  font-size:13px;
}

.footer{
  text-align:center;
  padding:18px;
  border-top:1px solid #e5e7eb;
  color:#6b7280;
  background:white;
  font-size:12px;
}

</style>