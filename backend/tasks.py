from celery_worker import celery_app
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import smtplib
import os
import csv
import io


load_dotenv()

SERVER_SMTP_HOST = "smtp.gmail.com"
SERVER_SMTP_PORT = 587
SENDER_ADDRESS   = os.getenv("SENDER_ADDRESS")
SENDER_PASSWORD  = os.getenv("SENDER_PASSWORD")


def send_email(to_address, subject, message, content="text", attachment=None):
    msg            = MIMEMultipart()
    msg['To']      = to_address
    msg['From']    = SENDER_ADDRESS
    msg['Subject'] = subject

    if content == "html":
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        with open(attachment, "rb") as a:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment}")
        msg.attach(part)

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=587)
    s.starttls()
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True


@celery_app.task()
def send_interview_reminder(
    student_email,
    student_name,
    job_title,
    company_name,
    interview_date,
    interview_time,
    interview_location
):
    message = f"""Hello {student_name},

Your interview has been scheduled!

Company  : {company_name}
Role     : {job_title}
Date     : {interview_date}
Time     : {interview_time}
Location : {interview_location}

Best of luck!"""

    send_email(
        to_address = student_email,
        subject    = "Interview Scheduled",
        message    = message
    )
    
    
@celery_app.task()
def send_shortlisted_notification(
    student_email,
    student_name,
    job_title,
    company_name
):
    message = f"""Hello {student_name},

Congratulations! You have been Shortlisted!

Company : {company_name}
Role    : {job_title}

Please wait for further updates regarding your interview schedule.

Best of luck!"""

    send_email(
        to_address=student_email,
        subject="Application Shortlisted",
        message=message
    )


@celery_app.task()
def send_selected_notification(
    student_email,
    student_name,
    job_title,
    company_name
):
    message = f"""Hello {student_name},

Congratulations! You have been Selected!

Company : {company_name}
Role    : {job_title}

The company will contact you soon with further details.

Best regards!"""

    send_email(
        to_address=student_email,
        subject="Congratulations - You are Selected!",
        message=message
    )


@celery_app.task()
def send_rejected_notification(
    student_email,
    student_name,
    job_title,
    company_name
):
    message = f"""Hello {student_name},

Thank you for applying for {job_title} at {company_name}.

After careful consideration, we regret to inform you that your application has been Rejected.

Do not be discouraged, keep applying!

Best regards!"""

    send_email(
        to_address=student_email,
        subject="Application Update",
        message=message
    )
    

@celery_app.task()
def export_student_applications_csv(student_email, student_name, student_id):
    from app import create_app
    from models import Application

    app = create_app()
    with app.app_context():
        applications = Application.query.filter_by(student_id=student_id).all()

        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(["Sr No", "Company", "Role", "Status", "Applied Date"])

        # Data
        for i, application in enumerate(applications, start=1):
            writer.writerow([
                i,
                application.placement_drive.company.name,
                application.placement_drive.job_title,
                application.status,
                application.apply_date
            ])

        filepath = f"exports/student_{student_id}_applications.csv"
        os.makedirs("exports", exist_ok=True)
        with open(filepath, "w", newline="") as f:
            f.write(output.getvalue())

        send_email(
            to_address=student_email,
            subject="Your Applications Export",
            message=f"Hello {student_name},\n\nPlease find your applications data attached.\n\nBest regards!",
            attachment=filepath
        )
        

@celery_app.task()
def export_company_drives_csv(company_email, company_name, company_id):
    from app import create_app
    from models import PlacementDrive

    app = create_app()
    with app.app_context():
        drives = PlacementDrive.query.filter_by(company_id=company_id).all()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["Sr No", "Drive Name", "Start Date", "Last Date", "Status"])

        for i, drive in enumerate(drives, start=1):
            writer.writerow([
                i,
                drive.job_title,
                drive.start_date.strftime("%d-%m-%Y") if drive.start_date else "N/A",
                drive.last_date.strftime("%d-%m-%Y") if drive.last_date else "N/A",
                drive.status
            ])

        filepath = f"exports/company_{company_id}_drives.csv"
        os.makedirs("exports", exist_ok=True)
        with open(filepath, "w", newline="") as f:
            f.write(output.getvalue())

        send_email(
            to_address=company_email,
            subject="Your Placement Drives Export",
            message=f"Hello {company_name},\n\nPlease find your placement drives data attached.\n\nBest regards!",
            attachment=filepath
        )
        
        
@celery_app.task()
def send_company_approval_email(company_email, company_name, is_approved):
    from app import create_app
    app = create_app()
    with app.app_context():
        if is_approved:
            send_email(
                to_address=company_email,
                subject="Your Account Has Been Approved!",
                message=f"Hello {company_name},\n\nCongratulations! Your account has been approved by the admin.\n\nYou can now login and create placement drives.\n\nBest regards!"
            )
        else:
            send_email(
                to_address=company_email,
                subject="Your Account Has Been Rejected",
                message=f"Hello {company_name},\n\nWe regret to inform you that your account request has been rejected by the admin.\n\nBest regards!"
            )
            

@celery_app.task()
def send_drive_approval_email(company_email, company_name, drive_name, is_approved):
    from app import create_app
    app = create_app()
    with app.app_context():
        if is_approved:
            send_email(
                to_address=company_email,
                subject="Your Placement Drive Has Been Approved!",
                message=f"Hello {company_name},\n\nCongratulations! Your placement drive '{drive_name}' has been approved by the admin.\n\nStudents can now apply for this drive.\n\nBest regards!"
            )
        else:
            send_email(
                to_address=company_email,
                subject="Your Placement Drive Has Been Rejected",
                message=f"Hello {company_name},\n\nWe regret to inform you that your placement drive '{drive_name}' has been rejected by the admin.\n\nBest regards!"
            )