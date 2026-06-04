from flask import Flask
from database import db
from config import LocalDevelopmentConfig
from flask_security import Security
from flask_security.utils import hash_password
from user_datastore import user_datastore 
from flask_cors import CORS
from extensions import cache


from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.student_routes import student_bp
from routes.company_routes import company_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    cache.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(company_bp)
    
    Security(app, user_datastore)

    return app


def init_db(app):
    with app.app_context():
        db.create_all()
        
        admin_role = user_datastore.find_or_create_role(name="admin", description="Admin role")
        company_role = user_datastore.find_or_create_role(name="company", description="Company role")
        student_role = user_datastore.find_or_create_role(name="student", description="Student role")
        
        db.session.commit()
        
        admin_user = user_datastore.find_user(username="admin")
        if not admin_user:
            user_datastore.create_user(
                name="Admin",
                username="admin",
                password=hash_password("admin@123"),
                email="admin@gmail.com",
                roles=[admin_role]  
            )
            
            db.session.commit()
            

app = create_app()


if __name__ == "__main__":
    init_db(app)
    app.run(debug=True)