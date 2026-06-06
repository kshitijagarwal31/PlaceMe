import { createRouter, createWebHistory } from "vue-router"

import HomeView from "../views/HomeView.vue"
import LoginView from "../views/LoginView.vue"
import RegisterView from "../views/RegisterView.vue"

import AdminDashboardView from "../views/AdminDashboardView.vue"
import AdminHomeView from "../views/AdminHomeView.vue"
import AdminStudentsView from "../views/AdminStudentsView.vue"
import AdminCompaniesView from "../views/AdminCompaniesView.vue"
import AdminPlacementDrivesView from "../views/AdminPlacementDrivesView.vue"
import AdminApplicationsView from "../views/AdminApplicationsView.vue"

import StudentDashboardView from "../views/StudentDashboardView.vue"
import StudentHomeView from "../views/StudentHomeView.vue"
import StudentProfileView from "../views/StudentProfileView.vue"
import StudentPlacementDriveView from "../views/StudentPlacementDriveView.vue"
import StudentApplicationView from "../views/StudentApplicationView.vue"

import CompanyDashboardView from "../views/CompanyDashboardView.vue"
import CompanyHomeView from "../views/CompanyHomeView.vue"
import CompanyCreateDriveView from "../views/CompanyCreateDriveView.vue"
import CompanyApplicationsView from "../views/CompanyApplicationsView.vue"
import CompanyPlacementDriveView from "../views/CompanyPlacementDriveView.vue"
import CompanyProfileView from "../views/CompanyProfileView.vue"

const routes = [
    {path: "/", component: HomeView},
    {path: "/login", component: LoginView},
    {path: "/register", component: RegisterView},
    
    {path: "/admin_dashboard", component: AdminDashboardView, meta: { requiresAuth: true }, children: [
        {path: "", component: AdminHomeView},
        {path: "students", component: AdminStudentsView},
        {path: "companies", component: AdminCompaniesView,},
        {path: "placement_drives", component: AdminPlacementDrivesView},
        {path: "applications", component: AdminApplicationsView}
    ]},

    {path: "/student_dashboard", component: StudentDashboardView, meta: { requiresAuth: true }, children: [
        {path: "", component: StudentHomeView},
        {path: "profile", component: StudentProfileView},
        {path: "placement_drives", component: StudentPlacementDriveView},
        {path: "applications", component: StudentApplicationView},
    ]},

    {path: "/company_dashboard", component: CompanyDashboardView, meta: { requiresAuth: true }, children: [
        {path: "", component: CompanyHomeView},
        {path: "create_drive", component: CompanyCreateDriveView},
        {path: "applications", component: CompanyApplicationsView},
        {path: "placement_drives", component: CompanyPlacementDriveView},
        {path: "profile", component: CompanyProfileView}
    ]}
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from) => {
    const token = localStorage.getItem('token')
    if (to.meta.requiresAuth && !token) {
        return '/' 
    }
    return true  
})

export default router