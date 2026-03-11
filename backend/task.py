from celeryapp import celery
from app import app, db, mail
from model import Student,Company,Interview,Application,PlacementDrive,Role,User
from datetime import datetime, timedelta
from flask_mail import Message
import os
import csv

@celery.task
def send_interview_reminders():
    

    tomorrow = datetime.now() + timedelta(days=1)
    with app.app_context():

        interviews = Interview.query.filter(
            Interview.interview_date >= tomorrow
        ).all()
        print(interviews,'that is list of intervei')

        for i in interviews:
            student_email = i.student.user.email
            body=f""" this remidner that you have interview at {i.interview_date}
"""
            msg = Message(
                subject="intervei reminder",
                recipients=[i.student.user.email],
                body=body
            )
            mail.send(msg)
            print(f"Reminder sent to {student_email} ")

@celery.task
def send_placement_report():
    with app.app_context():
    

        companies = Company.query.all()
        

        for company in companies:

            total_interviews = Interview.query.filter_by(company_id=company.id).count()
            total_placed = Interview.query.filter_by(company_id=company.id, placed=True).count()
            total = 0
           
            for drive in company.drives:
                if drive.applications:
                    total += len(drive.applications)
            if total:
                rate = (total_placed/total)*100 
            else:
                rate=0

            body = f"""
            Placement Report

            Company: {company.company_name}

            Total Applications: {total}
            total interview:{total_interviews}
            total totalplaced:{total_placed}
            placment rate:{rate}
            """

            msg = Message(
                subject="Monthly Placement Report",
                recipients=[company.user.email],
                body=body
            )
            mail.send(msg)

            

            print("Report sent",msg)





@celery.task
def export_application_history(user_id):

    with app.app_context():

        user = User.query.get(user_id)

        os.makedirs("exports", exist_ok=True)

        filename = f"applications_{datetime.now().timestamp()}.csv"
        file_path = os.path.join("exports", filename)

        with open(file_path, "w", newline="") as file:

            writer = csv.writer(file)
            writer.writerow(["ID", "Student", "Company", "Drive", "Status"])

            # STUDENT EXPORT
            if user.role == Role.STUDENT:

                student = user.student

                applications = Application.query.filter_by(
                    student_id=student.id
                ).all()

            # COMPANY EXPORT
            elif user.role == Role.COMPANY:

                company = user.company

                applications = Application.query.join(PlacementDrive)\
                    .filter(PlacementDrive.company_id == company.id)\
                    .all()

            else:
                applications = []

            for app_data in applications:

                writer.writerow([
                    app_data.id,
                    app_data.student.Student_name,
                    app_data.drive.company.company_name,
                    app_data.drive.job_title,
                    app_data.status
                ])

        msg = Message(
            subject="CSV Export Ready",
            recipients=[user.email],
            body="Your export is ready. CSV attached."
        )

        with open(file_path, "rb") as f:
            msg.attach(filename, "text/csv", f.read())

        mail.send(msg)

        try:
            os.remove(file_path)
        except:
            pass

       








# @celery.task
# def send_drive_reminder():
#     with app.app_context():
#         students = Student.query.all()

        
#         msg = Message(
#             subject="Apply for Drive",
#             recipients=["neetiushaseervi911@gmail.com"],
#             body="New placement drives available. Please apply."
#         )
#         # mail.send(msg)

#         print("Reminder Sent")
# @celery.task
# def send_report():
#     with app.app_context():
#         companies = Company.query.all()

#         if not companies:
#             body_text = "No companies found in database."
#         else:
#             body_text = "Company List:\n\n"
#             for company in companies:
#                 body_text += f"ID: {company.id}, Name: {company.company_name}\n"

#         msg = Message(
#             subject="Company Report",
#             recipients=["neetiushaseervi911@gmail.com"],
#             body=body_text
#         )

        