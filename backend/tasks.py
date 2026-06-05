from celery_worker import celery_app
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv

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

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT)
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