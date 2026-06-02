<template>

  <nav class="navbar">

    <div class="navbar-left">

      <router-link to="/" class="logo-area">

        <div class="logo">
          🎓
        </div>

        <div>

          <h2 class="logo-title">
            PlaceMe
          </h2>

          <p class="logo-subtitle">
            Placement Portal
          </p>

        </div>

      </router-link>

    </div>

    <div class="navbar-right">

      <router-link to="/" class="nav-link">
        Home
      </router-link>

      <router-link to="/login" class="nav-link">
        Login
      </router-link>

      <router-link to="/register" class="register-btn">
        Register
      </router-link>

    </div>

  </nav>

</template>

<script>

export default {

  name: "Navbar"

}

</script>

<style scoped>

*{
  margin:0;
  padding:0;
  box-sizing:border-box;
}

.navbar{
  width:100%;
  height:62px;
  padding:0 24px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  background:#2563eb;
  position:sticky;
  top:0;
  z-index:1000;
  box-shadow:0 3px 10px rgba(0,0,0,0.08);
}

.logo-area{
  display:flex;
  align-items:center;
  gap:8px;
  text-decoration:none;
}

.logo{
  width:38px;
  height:38px;
  background:white;
  border-radius:8px;
  display:flex;
  justify-content:center;
  align-items:center;
  font-size:18px;
}

.logo-title{
  font-size:17px;
  font-weight:700;
  color:white;
  line-height:1.1;
}

.logo-subtitle{
  font-size:9px;
  color:#dbeafe;
  margin-top:1px;
}

.navbar-right{
  display:flex;
  align-items:center;
  gap:8px;
}

.nav-link{
  text-decoration:none;
  color:white;
  font-size:13px;
  font-weight:600;
  padding:7px 10px;
  border-radius:6px;
  transition:0.2s;
}

.nav-link:hover{
  background:rgba(255,255,255,0.15);
}

.register-btn{
  text-decoration:none;
  background:white;
  color:#2563eb;
  padding:8px 14px;
  border-radius:7px;
  font-size:13px;
  font-weight:700;
  transition:0.2s;
}

.register-btn:hover{
  background:#e0e7ff;
}

</style>