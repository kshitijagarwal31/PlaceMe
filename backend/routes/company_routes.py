from flask import Blueprint, request, make_response, jsonify 
from flask_security import auth_required, roles_required, current_user
from database import db 
from models import CompanyProfile, PlacementDrive, Application 
from datetime import datetime 

company_bp = Blueprint("company_bp", __name__)


@company_bp.route("/company/dashboard_data", methods=["GET"])
@auth_required("token")
@roles_required("company")
def company_dashboard_data():

    all_drives     = PlacementDrive.query.filter_by(company_id=current_user.id).all()
    active_drives  = [d for d in all_drives if d.status == "Active"]

    drive_ids    = [d.id for d in all_drives]
    applications = Application.query.filter(
        Application.drive_id.in_(drive_ids)
    ).all()

    selected_count = len([a for a in applications if a.status == "Selected"])

    return jsonify({
        "stats": {
            "total_drives":       len(all_drives),
            "active_drives":      len(active_drives),
            "total_applications": len(applications),
            "selected_count":     selected_count,
        },
        "placement_drives": [
            {
                "id":         d.id,
                "job_title":  d.job_title,
                "company":    current_user.name,
                "status":     d.status,
                "start_date": str(d.start_date),
                "end_date":   str(d.last_date)
            } for d in all_drives
        ],
        "applications": [
            {
                "id":           a.id,
                "student_name": a.student.name if a.student else "N/A",
                "drive_title":  a.placement_drive.job_title if a.placement_drive else "N/A",
                "status":       a.status,
                "apply_date":   str(a.apply_date)
            } for a in applications
        ], 
        "company_name":       current_user.name
    }), 200
    
    
@company_bp.route("/company/complete_profile", methods=["GET", "POST"])
@auth_required("token")
@roles_required("company")
def complete_company_profile():

    if request.method == "GET":
        company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
        return jsonify({
            "name":              current_user.name,
            "username":          current_user.username,
            "email":             current_user.email,
            "industry":          company.industry           if company else "",
            "hr_contact_number": company.hr_contact_number  if company else "",
            "address":           company.address            if company else "",
            "description":       company.description        if company else "",
            "website_link":      company.website_link       if company else ""
        }), 200

    data = request.get_json()

    if data.get("name"):
        current_user.name = data.get("name")
    if data.get("username"):
        current_user.username = data.get("username")
    if data.get("email"):
        current_user.email = data.get("email")

    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if not company:
        company = CompanyProfile(
            user_id=current_user.id,
            industry=data.get("industry"),
            description=data.get("description"),
            hr_contact_number=data.get("hr_contact_number"),
            address=data.get("address"),
            website_link=data.get("website_link")
        )
        db.session.add(company)
    else:
        company.industry          = data.get("industry",          company.industry)
        company.description       = data.get("description",       company.description)
        company.hr_contact_number = data.get("hr_contact_number", company.hr_contact_number)
        company.address           = data.get("address",           company.address)
        company.website_link      = data.get("website_link",      company.website_link)

    db.session.commit()
    return jsonify({"message": "Company profile saved successfully"}), 200
    
    
@company_bp.route("/company/create_drive", methods=["POST"])
@auth_required("token")
@roles_required("company")
def create_drive():
    
    company = CompanyProfile.query.filter_by(user_id=current_user.id).first()
    if not company or not company.industry or not company.address or not company.hr_contact_number or not company.website_link:
        return jsonify({"message": "Please complete your profile before creating a drive"}), 403

    data = request.get_json()

    drive = PlacementDrive(
        company_id      = current_user.id,
        job_title       = data.get("job_title"),
        job_description = data.get("job_description"),
        salary          = data.get("salary"),
        skills_required = data.get("skills_required"),
        start_date      = datetime.strptime(data.get("start_date"), "%Y-%m-%d"),
        last_date       = datetime.strptime(data.get("last_date"),  "%Y-%m-%d"),
        status          = "Pending"
    )
    db.session.add(drive)
    db.session.commit()

    return jsonify({"message": "Drive created successfully"}), 201

@company_bp.route("/company/my_drives", methods=["GET"])
@auth_required("token")
@roles_required("company")
def company_my_drives():

    all_drives = PlacementDrive.query.filter_by(company_id=current_user.id).all()

    return jsonify({
        "drives": [
            {
                "id":         d.id,
                "job_title":  d.job_title,
                "salary":     d.salary or "",
                "status":     d.status,
                "start_date": str(d.start_date),
                "end_date":   str(d.last_date)
            } for d in all_drives
        ]
    }), 200


@company_bp.route("/company/drive_detail/<int:drive_id>", methods=["GET"])
@auth_required("token")
@roles_required("company")
def company_drive_detail(drive_id):
    drive = PlacementDrive.query.filter_by(
        id=drive_id,
        company_id=current_user.id
    ).first()

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    apps = drive.applications
    return jsonify({
        "id"               : drive.id,
        "job_title"        : drive.job_title,
        "company_name"     : current_user.name,
        "skills_required"  : drive.skills_required,
        "salary"           : drive.salary,
        "description"      : drive.job_description,
        "start_date"       : str(drive.start_date),
        "end_date"        : str(drive.last_date),
        "status"           : drive.status,
        "total_applications": len(apps),
        "shortlisted"      : len([a for a in apps if a.status == "Shortlisted"]),
        "selected"         : len([a for a in apps if a.status == "Selected"]),
        "rejected"         : len([a for a in apps if a.status == "Rejected"]),
        "applications"     : [
            {
                "id"          : a.id,
                "student_name": a.student.name if a.student else "N/A",
                "apply_date"  : str(a.apply_date),
                "status"      : a.status
            } for a in apps
        ]
    }), 200


@company_bp.route("/company/application_detail/<int:app_id>", methods=["GET"])
@auth_required("token")
@roles_required("company")
def company_application_detail(app_id):
    application = Application.query.get(app_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    if application.placement_drive.company_id != current_user.id:
        return jsonify({"message": "Unauthorized"}), 403

    student = application.student
    drive   = application.placement_drive
    profile = student.student_profile

    return jsonify({
        "id":           application.id,
        "status":       application.status,
        "apply_date":   str(application.apply_date),
        "student_name": student.name if student else "N/A",
        "email":        student.email if student else "N/A",
        "cgpa":         profile.cgpa if profile else "N/A",
        "skills":       profile.skills if profile else "N/A",
        "bio":          profile.bio if profile else "N/A",
        "resume":       profile.resume if profile else None,
        "drive_name":   drive.job_title if drive else "N/A",
        "company_name": current_user.name,
    }), 200
    
    
@company_bp.route("/company/application_update/<int:app_id>", methods=["PATCH"])
@auth_required("token")
@roles_required("company")
def company_application_update(app_id):
    application = Application.query.get(app_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    if application.placement_drive.company_id != current_user.id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()
    application.status = data.get("status", application.status)
    application.feedback = data.get("feedback", application.feedback) 
    db.session.commit()

    return jsonify({"message": f"Application {application.status} successfully"}), 200

