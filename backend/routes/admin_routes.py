from flask import Blueprint, request, make_response, jsonify
from flask_security import auth_required, roles_required, current_user
from user_datastore import user_datastore 
from database import db 
from models import User, Role, StudentProfile, CompanyProfile, PlacementDrive, Application
from extensions import cache 

admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route("/admin/dashboard_data", methods=["GET"])
@auth_required("token")
@roles_required("admin")
@cache.cached(key_prefix="admin_dashboard")
def admin_dashboard_data():

    total_students     = User.query.join(User.roles).filter(Role.name == "student").count()
    total_companies    = User.query.join(User.roles).filter(Role.name == "company", User.is_approved == True).count()
    total_drives       = PlacementDrive.query.filter_by(status="Active").count()
    total_applications = Application.query.count()
    total_placements   = Application.query.filter_by(status="Selected").count()
    placement_rate     = round((total_placements / total_students) * 100) if total_students > 0 else 0

    company_requests = User.query.join(User.roles).filter(
        Role.name == "company",
        User.is_approved == False
    ).all()

    pending_companies = [
        {
            "id": c.id,
            "name": c.name,
            "industry": c.company_profile.industry if c.company_profile else "N/A",
            "address": c.company_profile.address if c.company_profile else "N/A",
        }
        for c in company_requests
    ]

    pending_drive_list = PlacementDrive.query.filter_by(status="Pending").all()

    pending_drives = [
        {
            "id": d.id,
            "job_title": d.job_title,
            "company_name": d.company.name if d.company else "N/A",
            "start_date": str(d.start_date),
        }
        for d in pending_drive_list
    ]

    return jsonify({
        "stats": {
            "total_students":     total_students,
            "total_companies":    total_companies,
            "total_drives":       total_drives,
            "total_applications": total_applications,
            "total_placements":   total_placements,
            "placement_rate":     placement_rate,
        },
        "admin_name": current_user.name,
        "pending_companies": pending_companies,
        "pending_drives":    pending_drives,
    }), 200


@admin_bp.route("/admin/students", methods=["GET"])
@auth_required("token")
@roles_required("admin")
@cache.cached(key_prefix="admin_students")
def admin_students():
    students = User.query.join(User.roles).filter(Role.name == "student").all()
    students_list = []
    for s in students:
        profile = s.student_profile
        students_list.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "username": s.username,
            "is_active": s.active,
            "cgpa": profile.cgpa if profile else "N/A",
            "college": profile.college_name if profile else "N/A",
            "skills": profile.skills if profile else "N/A",
            "resume": profile.resume if profile else ""
        })
    return jsonify({"students": students_list}), 200


@admin_bp.route("/admin/companies", methods=["GET"])
@auth_required("token")
@roles_required("admin")
@cache.cached(key_prefix="admin_companies")
def admin_companies():
    companies = User.query.join(User.roles).filter(
        Role.name == "company",
        User.is_approved == True
    ).all()
    companies_list = []
    for c in companies:
        profile = c.company_profile
        companies_list.append({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "is_active": c.active,
            "industry": profile.industry if profile else "N/A",
            "address": profile.address if profile else "N/A",
            "website": profile.website_link if profile else "N/A",
            "contact": profile.hr_contact_number if profile else "N/A",
            "description": profile.description if profile else "N/A"
        })

    company_requests = User.query.join(User.roles).filter(
        Role.name == "company",
        User.is_approved == False
    ).all()
    company_requests_list = []
    for c in company_requests:
        profile = c.company_profile
        company_requests_list.append({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "industry": profile.industry if profile else "N/A",
            "address": profile.address if profile else "N/A",
            "website": profile.website_link if profile else "N/A",
            "contact": profile.hr_contact_number if profile else "N/A",
            "description": profile.description if profile else "N/A"
        })

    return jsonify({
        "companies": companies_list,
        "company_requests": company_requests_list
    }), 200


@admin_bp.route("/admin/placement_drives", methods=["GET"])
@auth_required("token")
@roles_required("admin")
@cache.cached(key_prefix="admin_placement_drives")
def admin_placement_drives():
    active_drives = PlacementDrive.query.filter_by(status="Active").all()
    pending_drives = PlacementDrive.query.filter_by(status="Pending").all()
    closed_drives = PlacementDrive.query.filter_by(status="Closed").all()

    def drive_to_dict(d):
        return {
            "id": d.id,
            "job_title": d.job_title,
            "company_name": d.company.name if d.company else "N/A",
            "company_id": d.company_id,
            "salary": d.salary,
            "start_date": str(d.start_date),
            "end_date": str(d.last_date),
            "skills_required": d.skills_required,
            "status": d.status
        }

    return jsonify({
        "active_drives": [drive_to_dict(d) for d in active_drives],
        "pending_drives": [drive_to_dict(d) for d in pending_drives],
        "closed_drives": [drive_to_dict(d) for d in closed_drives]
    }), 200


@admin_bp.route("/admin/applications", methods=["GET"])
@auth_required("token")
@roles_required("admin")
@cache.cached(key_prefix="admin_applications")
def admin_applications():
    applications = Application.query.all()

    applications_list = []

    for a in applications:
        student = a.student
        drive = a.placement_drive
        profile = student.student_profile if student else None

        applications_list.append({
            "id": a.id,
            "student_name": student.name if student else "N/A",
            "email": student.email if student else "N/A",

            "company_name": drive.company.name if drive and drive.company else "N/A",
            "drive": drive.job_title if drive else "N/A",

            "package": drive.salary if drive else "N/A",
            "apply_date": str(a.apply_date),

            "status": a.status or "Pending",
            "feedback": a.feedback or "N/A",

            "resume": profile.resume if profile else ""
        })

    return jsonify({"applications": applications_list}), 200


@admin_bp.route('/admin/application_detail/<int:id>', methods=['GET'])
@auth_required('token')
@roles_required('admin')
def admin_application_detail(id):
    application = Application.query.get_or_404(id)
    student = application.student        
    drive = application.placement_drive  
    profile = student.student_profile if student else None
    
    return jsonify({
        "email":    student.email if student else "—",
        "package":  drive.salary if drive else "—",   
        "feedback": application.feedback or "N/A",
        "resume":   profile.resume if profile else "", 
    })


@admin_bp.route("/admin/company/approve/<int:id>", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def approve_company(id):
    company = User.query.join(User.roles).filter(
        User.id == id, Role.name == "company"
    ).first()
    if not company:
        return {"message": "Company not found"}, 404
    company.is_approved = True
    db.session.commit()    
    cache.delete("admin_companies")
    cache.delete("admin_dashboard")
    return {"message": "Company approved successfully"}, 200


@admin_bp.route("/admin/company/reject/<int:id>", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def reject_company(id):
    company = User.query.get(id)
    if not company:
        return {"message": "Company not found"}, 404
    db.session.delete(company)
    db.session.commit()
    cache.delete("admin_companies")
    cache.delete("admin_dashboard")
    return {"message": "Company rejected and deleted"}, 200


@admin_bp.route("/admin/company/blacklist/<int:company_id>", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def blacklist_company(company_id):
    user = User.query.get(company_id)
    if not user:
        return jsonify({"message": "Company not found"}), 404
    user.active = False
    company = CompanyProfile.query.filter_by(user_id=company_id).first()
    if company:
        company.is_active = False
    db.session.commit()
    cache.delete("admin_companies")
    return jsonify({"message": "Company blacklisted"})


@admin_bp.route("/admin/company/unblacklist/<int:company_id>", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def unblacklist_company(company_id):
    user = User.query.get(company_id)
    if not user:
        return jsonify({"message": "Company not found"}), 404
    user.active = True
    company = CompanyProfile.query.filter_by(user_id=company_id).first()
    if company:
        company.is_active = True
    db.session.commit()
    cache.delete("admin_companies")
    return jsonify({"message": "Company unblacklisted"})


@admin_bp.route("/admin/student/blacklist/<int:student_id>", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def blacklist_student(student_id):
    user = User.query.get(student_id)
    if not user:
        return jsonify({"message": "Student not found"}), 404
    user.active = False
    student = StudentProfile.query.filter_by(user_id=student_id).first()
    if student:
        student.is_active = False
    db.session.commit()
    cache.delete("admin_students")
    return jsonify({"message": "Student blacklisted"})


@admin_bp.route("/admin/student/unblacklist/<int:student_id>", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def unblacklist_student(student_id):
    user = User.query.get(student_id)
    if not user:
        return jsonify({"message": "Student not found"}), 404
    user.active = True
    student = StudentProfile.query.filter_by(user_id=student_id).first()
    if student:
        student.is_active = True
    db.session.commit()
    cache.delete("admin_students")
    return jsonify({"message": "Student unblacklisted"})


@admin_bp.route("/admin/placement_drive/approve/<int:drive_id>", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def approve_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found"}), 404
    drive.status = "Active"    
    drive.is_approved = True
    db.session.commit()
    cache.delete("admin_placement_drives")
    cache.delete("admin_dashboard")
    return jsonify({"message": "Drive approved"})


@admin_bp.route("/admin/placement_drive/reject/<int:drive_id>", methods=["POST"])
@auth_required("token")
@roles_required("admin")
def reject_drive(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found"}), 404
    drive.status = "Rejected"
    db.session.commit()
    cache.delete("admin_placement_drives")
    cache.delete("admin_dashboard")
    return jsonify({"message": "Drive rejected"})