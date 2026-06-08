<template>
  <div class="home">

    <Navbar />

    <section class="hero">
      <div class="container">
        <div class="hero-inner">

          <div class="hero-left">
            <span class="badge">🎓 Placement Portal</span>
            <h1>Land Your Dream Job <span class="highlight">Faster</span></h1>
            <p>PlaceMe connects students with top companies. Apply, track and get placed — all from one powerful platform.</p>
            <div class="btns">
              <router-link to="/register" class="btn-primary">Get Started →</router-link>
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
      </div>
    </section>

    <section class="features">
      <div class="container">
        <div class="features-inner">

          <div class="features-left">
            <span class="badge">Features</span>
            <h2>Everything in One Place</h2>
            <p>From applying to getting placed — PlaceMe handles it all smoothly.</p>
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
      </div>
    </section>

    <section class="cta">
      <h2>Ready to Get Placed?</h2>
      <p>Join PlaceMe and start your placement journey today</p>
      <router-link to="/register" class="cta-btn">Create Account →</router-link>
    </section>

    <Footer />

  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"
import Footer from "../components/Footer.vue"

export default {
  name: "HomeView",
  components: { Navbar, Footer }
}

</script>

<style scoped>

* { 
  box-sizing: border-box; 
  margin: 0; 
  padding: 0; 
}

.home {
  min-height: 100vh;
  background: #f8fafc;
  font-family: 'Plus Jakarta Sans', sans-serif;
  color: #111827;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 32px;
}

.hero {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 80px 0;
}

.hero-inner {
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
  font-weight: 700;
  padding: 5px 14px;
  border-radius: 20px;
  margin-bottom: 20px;
}

.hero-left h1 {
  font-size: 46px;
  font-weight: 800;
  line-height: 1.15;
  color: #111827;
  margin-bottom: 16px;
  letter-spacing: -0.5px;
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
  flex-wrap: wrap; 
}

.btn-primary {
  text-decoration: none;
  background: #2563eb;
  color: white;
  padding: 13px 26px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 14px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  transition: all 0.2s;
  display: inline-block;
  box-shadow: 0 4px 14px rgba(37,99,235,0.3);
}

.btn-primary:hover {
  background: #1d4ed8;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(37,99,235,0.4);
}

.btn-ghost {
  text-decoration: none;
  background: transparent;
  color: #374151;
  padding: 13px 26px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 14px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  border: 1.5px solid #e5e7eb;
  transition: all 0.2s;
}

.btn-ghost:hover { 
  background: #f9fafb; 
  border-color: #d1d5db; 
}

.hero-right { 
  flex: 0 0 300px; 
}

.info-card {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 26px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 14px;
}

.dot { 
  width: 8px; 
  height: 8px; 
  border-radius: 50%; 
  flex-shrink: 0; 
}

.dot.green { 
  background: #16a34a; 
  box-shadow: 0 0 6px rgba(22,163,74,0.5); 
}

.divider { 
  height: 1px; 
  background: #e5e7eb; 
  margin-bottom: 14px; 
}

.info-item { 
  display: flex; 
  flex-direction: column; 
  gap: 2px; 
  margin-bottom: 12px; 
}

.label {
  font-size: 10px;
  color: #9ca3af;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.6px;
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
  border-radius: 8px;
  font-weight: 700;
  font-size: 13px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  margin-top: 16px;
  transition: all 0.2s;
  box-shadow: 0 3px 10px rgba(37,99,235,0.3);
}

.card-btn:hover { 
  background: #1d4ed8; 
}

.features {
  padding: 80px 0;
  background: #f8fafc;
}

.features-inner {
  display: flex;
  gap: 80px;
  align-items: flex-start;
}

.features-left { 
  flex: 0 0 260px; 
}

.features-left h2 {
  font-size: 28px;
  font-weight: 800;
  margin: 10px 0;
  color: #111827;
  line-height: 1.3;
  letter-spacing: -0.3px;
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
  gap: 14px;
}

.feat {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.2s;
}

.feat:hover {
  border-color: #bfdbfe;
  box-shadow: 0 4px 14px rgba(37,99,235,0.08);
  transform: translateY(-1px);
}

.feat-icon { 
  font-size: 22px; 
  flex-shrink: 0; 
  margin-top: 1px; 
}

.feat h4 {
  font-size: 14px;
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
  padding: 72px 32px;
  text-align: center;
}

.cta h2 {
  font-size: 30px;
  font-weight: 800;
  color: white;
  margin-bottom: 10px;
  letter-spacing: -0.3px;
}

.cta p {
  color: #bfdbfe;
  font-size: 15px;
  margin-bottom: 28px;
}

.cta-btn {
  text-decoration: none;
  background: white;
  color: #2563eb;
  padding: 13px 28px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 14px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  transition: all 0.2s;
  display: inline-block;
  box-shadow: 0 4px 14px rgba(0,0,0,0.15);
}

.cta-btn:hover { 
  background: #eff6ff; 
  transform: translateY(-1px); 
}

</style>