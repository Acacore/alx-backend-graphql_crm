# CRM Project Setup Guide

This guide walks you through setting up and running the CRM application, including Redis, database migrations, Celery worker, Celery Beat, and log verification.

---

## Prerequisites

- Python 3.8+
- Redis server
- `pip` (Python package manager)
- Virtual environment (recommended)

---

## 1. Install Redis and Dependencies

### Install Redis
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# On macOS (using Homebrew)
brew install redis

# On CentOS/RHEL
sudo yum install redis
Start and enable Redis:
bashsudo systemctl start redis
sudo systemctl enable redis
Install Python Dependencies
bash# Clone the repository (if applicable)
git clone <your-repo-url>
cd crm

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

Ensure celery, redis, and django are listed in requirements.txt.


2. Run Database Migrations
bashpython manage.py migrate
This applies all database schema changes.

3. Start Celery Worker
In a new terminal (with virtual environment activated):
bashcelery -A crm worker -l info
This starts the background task worker.

4. Start Celery Beat (Scheduler)
In another terminal:
bashcelery -A crm beat -l info
This runs periodic tasks as defined in your app.

5. Verify Logs
Application and task logs are written to:
text/tmp/crm_report_log.txt
Check the log file:
bashtail -f /tmp/crm_report_log.txt
You should see task execution logs, errors, or scheduled job activity here.

Notes

Ensure Redis is running before starting Celery.
Use screen, tmux, or a process manager (like supervisor) in production.
For development, you can combine worker and beat using:
bashcelery -A crm worker --beat -l info



Troubleshooting

Issue,Solution
Connection refused to Redis,Check redis-server is running
Celery tasks not running,Verify broker URL in settings.py
Log file not updating,Check write permissions on /tmp














IssueSolutionConnection refused to RedisCheck redis-server is runningCelery tasks not runningVerify broker URL in settings.pyLog file not updatingCheck write permissions on /tmp