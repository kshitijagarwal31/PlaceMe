from flask import Blueprint, request, make_response, jsonify
from flask_security import auth_required, roles_required, current_user
from database import db
from models import StudentProfile, PlacementDrive, Application
from extensions import cache


student_bp = Blueprint("student_bp", __name__)


@student_bp.route("/student/dashboard_data", methods=["GET"])
@auth_required("token")
@roles_required("student")
def student_dashboard_data():
    my_applications = Application.query.filter_by(student_id=current_user.id).all()

    stats = {
        "total_applications": len(my_applications),
        "shortlisted"       : Application.query.filter_by(student_id=current_user.id, status="Shortlisted").count(),
        "selected"          : Application.query.filter_by(student_id=current_user.id, status="Selected").count(),
        "ongoing_drives"    : PlacementDrive.query.filter_by(status="Active").count(),
    }
    
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    profile_complete = bool(
        profile and profile.cgpa and profile.skills and profile.resume and profile.bio
    )

    active_drives = PlacementDrive.query.filter_by(status="Active").all()
    drives_list = [
        {
            "id"        : d.id,
            "job_title" : d.job_title,
            "company"   : d.company.name if d.company else "N/A",
            "salary"    : d.salary or "N/A",
            "start_date": str(d.start_date),
            "end_date"  : str(d.last_date)
        } for d in active_drives
    ]

    applications_list = [
        {
            "id"         : a.id,
            "drive_title": a.placement_drive.job_title if a.placement_drive else "N/A",
            "company"    : a.placement_drive.company.name if a.placement_drive and a.placement_drive.company else "N/A",
            "status"     : a.status,
            "apply_date" : str(a.apply_date)
        } for a in my_applications
    ]

    return jsonify({
        "student_name": current_user.name,
        "stats"            : stats,
        "profile_complete" : profile_complete, 
        "placement_drives" : drives_list,
        "applications"     : applications_list
    }), 200


@student_bp.route("/student/all_drives", methods=["GET"])
@auth_required("token")
@roles_required("student")
def student_all_drives():
    all_drives = PlacementDrive.query.filter_by(status="Active").all()

    return jsonify({
        "drives": [
            {
                "id"             : d.id,
                "job_title"      : d.job_title,
                "company"        : d.company.name if d.company else "N/A",
                "salary"         : d.salary or "",
                "status"         : d.status,
                "start_date"     : str(d.start_date),
                "end_date"       : str(d.last_date),
                "already_applied": Application.query.filter_by(
                    student_id=current_user.id,
                    drive_id=d.id
                ).first() is not None
            } for d in all_drives
        ]
    }), 200


@student_bp.route("/student/drive_detail/<int:drive_id>", methods=["GET"])
@auth_required("token")
@roles_required("student")
def student_drive_detail(drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    existing_application = Application.query.filter_by(
        student_id=current_user.id,
        drive_id=drive_id
    ).first()

    return jsonify({
        "id"             : drive.id,
        "job_title"      : drive.job_title,
        "company"        : drive.company.name if drive.company else "N/A",
        "salary"         : drive.salary,
        "skills_required": drive.skills_required,
        "description"    : drive.job_description,
        "start_date"     : str(drive.start_date),
        "end_date"       : str(drive.last_date),
        "already_applied": existing_application is not None
    }), 200


@student_bp.route("/student/apply/<int:drive_id>", methods=["POST"])
@auth_required("token")
@roles_required("student")
def apply_drive(drive_id):
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()

    if not profile or not profile.cgpa or not profile.skills or not profile.resume or not profile.bio:
        return jsonify({"message": "Please complete your profile before applying for a drive"}), 403

    drive = PlacementDrive.query.get(drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404
    if drive.status != "Active":
        return jsonify({"message": "Drive is not active"}), 400

    existing = Application.query.filter_by(
        student_id=current_user.id,
        drive_id=drive_id
    ).first()

    if existing:
        return jsonify({"message": "Already applied!"}), 400

    application = Application(
        student_id=current_user.id,
        drive_id=drive_id,
        status="Pending"
    )
    db.session.add(application)
    db.session.commit()
    cache.delete(f"student_applications_{current_user.id}")   
    cache.delete("admin_applications")                        
    cache.delete("admin_dashboard")        
    cache.delete(f"company_dashboard_{application.drive.company_id}")
    cache.delete(f"company_drives_{application.drive.company_id}")  

    return jsonify({"message": "Applied successfully!"}), 201


@student_bp.route("/student/complete_profile", methods=["GET", "PUT"])
@auth_required("token")
@roles_required("student")
def complete_profile():

    if request.method == "GET":
        profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
        return jsonify({
            "name"        : current_user.name,
            "username"    : current_user.username,
            "email"       : current_user.email,
            "college_name": profile.college_name if profile else "",
            "cgpa"        : profile.cgpa         if profile else "",
            "skills"      : profile.skills       if profile else "",
            "resume"      : profile.resume       if profile else "",
            "bio"         : profile.bio          if profile else ""
        }), 200

    if request.method == "PUT":
        name         = request.form.get("name",         "").strip()
        username     = request.form.get("username",     "").strip()
        email        = request.form.get("email",        "").strip()
        password     = request.form.get("password",     "").strip()
        college_name = request.form.get("college_name", "").strip()
        cgpa         = request.form.get("cgpa",         "").strip()
        skills       = request.form.get("skills",       "").strip()
        bio          = request.form.get("bio",          "").strip()

        if name:     current_user.name     = name
        if username: current_user.username = username
        if email:    current_user.email    = email
        if password:
            from flask_security.utils import hash_password
            current_user.password = hash_password(password)

        profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
        if not profile:
            profile = StudentProfile(user_id=current_user.id)
            db.session.add(profile)

        if college_name: profile.college_name = college_name

        if cgpa:
            try:
                cgpa_val = float(cgpa)
                if 0 < cgpa_val <= 10:
                    profile.cgpa = cgpa_val
            except ValueError:
                return make_response(jsonify({"message": "Invalid CGPA"}), 400)

        if skills: profile.skills = skills
        if bio:    profile.bio    = bio

        import os
        resume_file = request.files.get("resume")
        if resume_file:
            filename  = f"resume_{current_user.id}.pdf"
            save_path = os.path.join("static", "resumes", filename)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            resume_file.save(save_path)
            profile.resume = f"/static/resumes/{filename}"

        db.session.commit()
        cache.delete("admin_students") 
        
        return jsonify({"message": "Profile updated successfully"}), 200


@student_bp.route("/student/my_applications", methods=["GET"])
@auth_required("token")
@roles_required("student")
@cache.cached(key_prefix=lambda: f"student_applications_{current_user.id}")
def student_my_applications():
    my_applications = Application.query.filter_by(
        student_id=current_user.id
    ).order_by(Application.apply_date.desc()).all()

    return jsonify({
        "applications": [
            {
                "id"          : a.id,
                "company"     : a.placement_drive.company.name if a.placement_drive and a.placement_drive.company else "N/A",
                "drive"       : a.placement_drive.job_title if a.placement_drive else "N/A",
                "date"        : str(a.apply_date),
                "package"     : a.placement_drive.salary if a.placement_drive else "N/A",
                "status"      : a.status,
                "student_name": current_user.name,
                "email"       : current_user.email,
            } for a in my_applications
        ]
    }), 200


@student_bp.route("/student/application_detail/<int:app_id>", methods=["GET"])
@auth_required("token")
@roles_required("student")
def application_detail(app_id):
    app_data = Application.query.get(app_id)

    if not app_data or app_data.student_id != current_user.id:
        return jsonify({"message": "Application not found"}), 404

    drive = app_data.placement_drive

    return jsonify({
        "id"                : app_data.id,
        "status"            : app_data.status,
        "apply_date"        : str(app_data.apply_date),
        "interview_date"    : str(app_data.interview_date) if app_data.interview_date else "",
        "interview_mode"    : app_data.interview_mode or "N/A",
        "interview_location": app_data.interview_location or "",
        "feedback"          : app_data.feedback or "N/A",
        "offer_letter"      : app_data.offer_letter or "",
        "resume"            : app_data.student.student_profile.resume if app_data.student and app_data.student.student_profile else "",
        "job_title"         : drive.job_title if drive else "N/A",
        "company"           : drive.company.name if drive and drive.company else "N/A",
        "salary"            : drive.salary if drive else "N/A",
        "skills_required"   : drive.skills_required if drive else "N/A",
        "description"       : drive.job_description if drive else "N/A",
        "start_date"        : str(drive.start_date) if drive else "",
        "end_date"          : str(drive.last_date) if drive else ""
    }), 200