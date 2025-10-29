
### All the setup steps for Celery Task:

Virtual environment creation and activation

pip install -r requirements.txt

Migrations (python manage.py migrate)

Redis installation and start

Django server start (python manage.py runserver)

Celery worker and Beat start

Cron jobs setup (CRONJOBS entries)

How to test logs in /tmp/

GraphQL “hello” field test


''' Break Down '''


# CRM Celery Beat Report Task

## Overview
This module integrates **Celery** and **Celery Beat** with the CRM system to automatically generate a **weekly performance report**.  
The task queries the GraphQL API to summarize:
- Total number of customers  
- Total number of orders  
- Total revenue  

Each report is logged with a timestamp in `/tmp/crm_report_log.txt`.

---

## Setup Instructions

### 1. Install Dependencies
Ensure Redis and the required Python packages are installed:
```bash
sudo apt install redis-server
pip install -r requirements.txt

Start the Redis service:

sudo systemctl start redis
sudo systemctl enable redis

2. Apply Migrations

Run database migrations to initialize Celery Beat’s scheduler tables:

python manage.py migrate

3. Start Celery Services

Open two separate terminals in your project root and run:

Start Celery Worker

celery -A crm worker -l info


Start Celery Beat Scheduler

celery -A crm beat -l info


Celery Beat will trigger the generate_crm_report task every Monday at 6:00 AM.

4. Verify Logs

After the task executes (or if manually triggered), check:

cat /tmp/crm_report_log.txt


Example output:

2025-10-29 06:00:00 - Report: 12 customers, 24 orders, 1800.00 revenue

5. Manual Trigger (Optional)

You can manually trigger the report from the Django shell:

python manage.py shell
>>> from crm.tasks import generate_crm_report
>>> generate_crm_report.delay()

Summary

This setup ensures automated, scheduled CRM performance monitoring via Celery Beat, providing a reliable and scalable background task execution framework.