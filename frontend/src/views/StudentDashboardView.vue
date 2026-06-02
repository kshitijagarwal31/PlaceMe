<template>
  <div class="dashboard">
    <Sidebar role="student" />
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar.vue"
export default {
  name: "StudentDashboardView",
  components: { Sidebar }
}
</script>

<style scoped>
.dashboard {
  display: flex;
  min-height: 100vh;
  background: #f5f7fb;
  font-family: Arial, Helvetica, sans-serif;
}
.main-content {
  flex: 1;
  padding: 28px;
}
</style>