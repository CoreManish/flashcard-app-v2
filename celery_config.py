
BROKER_URL = "redis://localhost:6379/1"
CELERY_RESULT_BACKEND = 'redis'
CELERY_RESULT_DBURI = 'redis://localhost:6379/0'


from celery.schedules import crontab
from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'every-minute': {
        'task': 'schedule_job.add',
        'schedule': crontab('*/5','*','*','*','*'),#every hour in 5 minute interval #timedelta(seconds=10)
        'args': (1, 2),
    },
    'SEND-ALERT-TO-REVIEW': {
        'task': 'schedule_job.sendAlertAsync',
        'schedule': crontab('0','1','*','*','*'), #each day 1am
    },
    'SEND-REPORT-IN-EMAIL': {
        'task': 'schedule_job.sendReport',
        'schedule': crontab('0','0','1','*','*'), # each month date=1
    }
}