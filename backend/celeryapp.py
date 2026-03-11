from celery import Celery
# from app import app

celery = Celery(
    'backend',
    broker='redis://localhost:6379/0'
)

celery.conf.update(
    # app.config,
    timezone='Asia/Kolkata',

    beat_schedule={
        
        'send-company-report-every-1-hour': {
            'task': 'task.send_placement_report',
            'schedule': 360.0,
        },
        'interview-reminder-daily': {
        'task': 'task.send_interview_reminders',
        'schedule': 360.0
    }
    }

)



import task