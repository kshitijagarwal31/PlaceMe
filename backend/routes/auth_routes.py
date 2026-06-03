from flask import Blueprint, request, make_response, jsonify 
from flask_security import auth_required, roles_required, current_user, utils
from user_datastore import user_datastore
from database import db 
from flask_security.utils import hash_password
from models import StudentProfile, CompanyProfile
from extensions import cache

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    login_cred = request.get_json()
    
    if not login_cred:
        return make_response(jsonify({"message": "Username and Password are required."}), 400)
    
    username = login_cred.get("username")
    password = login_cred.get("password")
    
    if not username:
        return make_response(jsonify({"message": "Username is required."}), 400)
    if not password:
        return make_response(jsonify({"message": "Password is required."}), 400)
    
    user = user_datastore.find_user(username=username)
    if not user:
        return make_response(jsonify({"message": "User not found."}), 404)
    
    if not utils.verify_password(password, user.password):
        return make_response(jsonify({"message": "Invalid credentials."}), 401)
    
    user_roles = [role.name for role in user.roles]
    
    if not user.active:
        if "student" in user_roles:
            return make_response(jsonify({"message": "You are blacklisted. Contact your admin."}), 403)
        elif "company" in user_roles:
            return make_response(jsonify({"message": "You are blacklisted. Contact your admin."}), 403)
        
    if "company" in user_roles and not user.is_approved:
        return make_response(jsonify({"message": "Company not approved by admin yet."}), 403)
    
    auth_token = user.get_auth_token()
    
    profile_complete = False
    if "company" in user_roles:
        profile = CompanyProfile.query.filter_by(user_id=user.id).first()
        profile_complete = bool(profile)
    elif "student" in user_roles:
        profile = StudentProfile.query.filter_by(user_id=user.id).first()
        profile_complete = bool(profile)
        
    return make_response(jsonify({
        "message": "Login Successfully",
        "auth_token": auth_token,
        "profile_complete": profile_complete,
        "user": {
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "roles": user_roles
        }
    }), 200)
    
    
@auth_bp.route("/logout", methods=["POST"])
@auth_required("token")
def logout():
    utils.logout_user()
    return make_response(jsonify({"message": "User logged out successfully."}), 200)


@auth_bp.route("/register/student", methods=["POST"])
def register_student():
    register_cred = request.get_json()
    
    if not register_cred:
        return jsonify({"message": "All fields are required"}), 400
    
    name = register_cred.get("name")
    username = register_cred.get("username")
    password = register_cred.get("password")
    email = register_cred.get("email")
    
    if not name or not username or not password or not email:
        return jsonify({"message": "All fields are required"}), 400
    
    if user_datastore.find_user(username=username):
        return make_response(jsonify({"message": "Username already exist."}), 400)
    if user_datastore.find_user(email=email):
        return make_response(jsonify({"message": "Email already exist."}), 400)
    if len(password) < 6:
        return make_response(jsonify({"message": "Password should be at least 6 characters long."}), 400)
    
    student_role = user_datastore.find_role("student")
    new_user = user_datastore.create_user(
        name=name,
        username=username,
        password=hash_password(password),
        email=email,
        roles=[student_role]
    )
    db.session.commit()
    
    return make_response(jsonify({
        "message": "Student registered successfully.",
        "user": {
            "name": new_user.name,
            "username": new_user.username,
            "email": new_user.email,
            "roles": [role.name for role in new_user.roles],
            "is_approved": True
        }
    }), 201)
    

@auth_bp.route("/register/company", methods=["POST"])
def register_company():
    register_cred = request.get_json()
    
    if not register_cred:
        return jsonify({"message": "All fields are required"}), 400
    
    name = register_cred.get("name")
    username = register_cred.get("username")
    password = register_cred.get("password")
    email = register_cred.get("email")
    
    if not name or not username or not password or not email:
        return jsonify({"message": "All fields are required"}), 400
    
    if user_datastore.find_user(username=username):
        return make_response(jsonify({"message": "Username already exist."}), 400)
    if user_datastore.find_user(email=email):
        return make_response(jsonify({"message": "Email already exist."}), 400)
    if len(password) < 6:
        return make_response(jsonify({"message": "Password should be at least 6 characters long."}), 400)
    
    company_role = user_datastore.find_role("company")
    new_user = user_datastore.create_user(
        name=name,
        username=username,
        password=hash_password(password),
        email=email,
        roles=[company_role]
    )
    db.session.commit()
    
    return make_response(jsonify({
        "message": "Company registered successfully.",
        "user": {
            "name": new_user.name,
            "username": new_user.username,
            "email": new_user.email,
            "roles": [role.name for role in new_user.roles],
            "is_approved": new_user.is_approved
        }
    }), 201)