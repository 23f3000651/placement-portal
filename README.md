Backend Setup
cd backend

Create and Activate Virtual Environment
python -m venv penv  

 ./penv/scripts/activate   

Install Dependencies
cd ..
pip install -r requirements.txt
cd backend
python app.py

Celery Background Jobs

This project uses Celery for background task execution.

Start Celery Worker
celery -A celeryapp.celery worker --pool=solo --loglevel=info


Start Celery Beat Scheduler
celery -A celeryapp.celery beat --loglevel=info

Frontend Setup (Vue)

Go to frontendvue directory:

cd frontendvue

Install dependencies:

npm install

Run development server:

npm run himanshu


Notes

Backend runs on Flask API.

Frontend is built using Vue.js.

Celery is used for background tasks and scheduled jobs.