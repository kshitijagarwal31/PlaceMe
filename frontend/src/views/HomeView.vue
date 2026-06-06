<template>
  <div class="home">

    <Navbar />

    <section class="hero">
      <div class="hero-inner">
        <div class="hero-left">
          <span class="badge">🎓 Placement Portal</span>
          <h1>Land Your Dream Job <span class="highlight">Faster</span></h1>
          <p>PlaceMe connects students with top companies. Apply, track and get placed — all from one powerful platform.</p>
          <div class="btns">
            <router-link to="/register" class="btn-primary">Start Now →</router-link>
            <router-link to="/login" class="btn-ghost">Sign In</router-link>
          </div>
        </div>
        <div class="hero-right">
          <div class="info-card">
            <div class="info-row">
              <span class="dot green"></span>
              <span>Placement drives are live</span>
            </div>
            <div class="divider"></div>
            <div class="info-item">
              <span class="label">For Students</span>
              <span class="val">Apply to drives & track status</span>
            </div>
            <div class="info-item">
              <span class="label">For Companies</span>
              <span class="val">Post drives & hire talent</span>
            </div>
            <div class="info-item">
              <span class="label">For Admins</span>
              <span class="val">Manage everything centrally</span>
            </div>
            <router-link to="/register" class="card-btn">Get Started →</router-link>
          </div>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="features-inner">
        <div class="features-left">
          <span class="badge">Features</span>
          <h2>Everything in One Place</h2>
          <p>From applying to getting placed — PlaceMe handles it all smoothly and efficiently.</p>
        </div>
        <div class="features-right">
          <div class="feat">
            <div class="feat-icon">⚡</div>
            <div>
              <h4>One Click Apply</h4>
              <p>Apply to placement drives instantly without any paperwork.</p>
            </div>
          </div>
          <div class="feat">
            <div class="feat-icon">📊</div>
            <div>
              <h4>Real Time Tracking</h4>
              <p>Know your application status at every stage of the process.</p>
            </div>
          </div>
          <div class="feat">
            <div class="feat-icon">🔔</div>
            <div>
              <h4>Instant Notifications</h4>
              <p>Get email alerts for shortlists, interviews and selections.</p>
            </div>
          </div>
          <div class="feat">
            <div class="feat-icon">🛡️</div>
            <div>
              <h4>Secure Platform</h4>
              <p>Role based access for students, companies and admins.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="cta">
      <h2>Ready to Get Placed?</h2>
      <p>Join PlaceMe and start your placement journey today</p>
      <router-link to="/register" class="btn-primary">Create Account →</router-link>
    </section>

    <footer class="footer">
      <p>© 2026 PlaceMe Portal. All Rights Reserved.</p>
    </footer>

  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"

export default {
  name: "HomeView",
  components: { Navbar }
}
</script>

<style scoped>

* { box-sizing: border-box; margin: 0; padding: 0; }

.home {
  min-height: 100vh;
  background: #f8fafc;
  font-family: 'Segoe UI', sans-serif;
  color: #111827;
}

.hero {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 70px 60px;
}

.hero-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 60px;
}

.hero-left {
  flex: 1;
}

.badge {
  display: inline-block;
  background: #eff6ff;
  color: #2563eb;
  font-size: 12px;
  font-weight: 600;
  padding: 5px 12px;
  border-radius: 20px;
  margin-bottom: 20px;
}

.hero-left h1 {
  font-size: 46px;
  font-weight: 800;
  line-height: 1.2;
  color: #111827;
  margin-bottom: 16px;
}

.highlight { 
  color: #2563eb; 
}

.hero-left p {
  font-size: 15px;
  color: #6b7280;
  line-height: 1.8;
  margin-bottom: 32px;
  max-width: 440px;
}

.btns {
  display: flex;
  gap: 12px;
}

.btn-primary {
  text-decoration: none;
  background: #2563eb;
  color: white;
  padding: 13px 26px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 14px;
  transition: 0.2s;
  display: inline-block;
}

.btn-primary:hover { 
  background: #1d4ed8; 
}

.btn-ghost {
  text-decoration: none;
  background: transparent;
  color: #374151;
  padding: 13px 26px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  border: 1px solid #e5e7eb;
  transition: 0.2s;
}

.btn-ghost:hover { 
  background: #f9fafb; 
}

.hero-right { 
  flex: 0 0 320px; 
}

.info-card {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 28px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot.green { 
  background: #16a34a; 
}

.divider {
  height: 1px;
  background: #e5e7eb;
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-bottom: 14px;
}

.label {
  font-size: 11px;
  color: #9ca3af;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.val {
  font-size: 13px;
  color: #374151;
  font-weight: 500;
}

.card-btn {
  display: block;
  text-align: center;
  text-decoration: none;
  background: #2563eb;
  color: white;
  padding: 11px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 13px;
  margin-top: 18px;
  transition: 0.2s;
}

.card-btn:hover { 
  background: #1d4ed8; 
}

.features {
  padding: 80px 60px;
}

.features-inner {
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  gap: 80px;
  align-items: flex-start;
}

.features-left {
  flex: 0 0 280px;
}

.features-left h2 {
  font-size: 32px;
  font-weight: 800;
  margin: 12px 0;
  color: #111827;
  line-height: 1.3;
}

.features-left p {
  font-size: 14px;
  color: #6b7280;
  line-height: 1.7;
}

.features-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.feat {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 22px;
  transition: 0.2s;
}

.feat:hover {
  border-color: #bfdbfe;
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}

.feat-icon {
  font-size: 26px;
  flex-shrink: 0;
}

.feat h4 {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 4px;
}

.feat p {
  font-size: 13px;
  color: #6b7280;
  line-height: 1.6;
}

.cta {
  background: #2563eb;
  padding: 70px 40px;
  text-align: center;
}

.cta h2 {
  font-size: 32px;
  font-weight: 800;
  color: white;
  margin-bottom: 10px;
}

.cta p {
  color: #bfdbfe;
  font-size: 15px;
  margin-bottom: 28px;
}

.cta .btn-primary {
  background: white;
  color: #2563eb;
}

.cta .btn-primary:hover {
  background: #eff6ff;
}

.footer {
  text-align: center;
  padding: 22px;
  border-top: 1px solid #e5e7eb;
  color: #9ca3af;
  font-size: 12px;
  background: white;
}

</style>