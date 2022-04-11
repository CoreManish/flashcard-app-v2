from config_celery import mycelery

# define beat configuration for scheduled tasks
from celery.schedules import crontab
mycelery.conf.beat_schedule = {
    'call_add_automatic': {
        'task': 'job.add',
        #'schedule': 5.0, # Runs in every 5 seconds
        #'schedule': crontab(minute=1), # Runs in every 1 minutes
        'schedule': crontab('*/1','*','*','*','*'),#Runs in every 1 minutes
        'args': (5,7) # Run the function with arguments
    },

    'call_send_alert_automatic':{
        'task':'job.send_alert',
        'schedule': crontab('*/1','*','*','*','*')#Runs in every 1 minutes
    },
    
    'call_send_report_automatic':{
        'task':'job.send_report',
        'schedule':crontab('*/1','*','*','*','*') #Runs in every 1 minutes'
    }

}

#--------- DEMO CELERY AUTOMATIC START --------
@mycelery.task()
def add(x, y):
    return x + y
#---------- DEMO CELERY AUTOMATIC END --------


# ----------ALERT USER TO REVIEW START------------
import time
from httplib2 import Http
from json import dumps

@mycelery.task()
def send_alert():
    t = time.time()
    t = int(t*1000)  # timestamp in milliseconds
    review_interval = 24*60*60*1000  # if reviewd 24hr before
    users = User.query.all()
    for user in users:
        if user.webhook_url and user.last_review_time:
            if user.last_review_time < (t-review_interval):
                url = user.webhook_url

                bot_message = {
                    'text': 'Please revise deck and card today!'}

                message_headers = {
                    'Content-Type': 'application/json; charset=UTF-8'}

                http_obj = Http()

                response = http_obj.request(
                    uri=url,
                    method='POST',
                    headers=message_headers,
                    body=dumps(bot_message),
                )
    return "Alert to all user has been sent asynchronously"

# ----------ALERT USER TO REVIEW END------------



# -----------SEND REPORT EMAIL START -------

from models import User, Deck, Card
from jinja2 import Environment, FileSystemLoader

@mycelery.task()
def send_report():
    users = users = User.query.all()
    for user in users:
        recipient = user.email
        subject = "Monthly report flashcard"

        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        template = env.get_template('report.html')
        body = template.render(name=user.name, data=user.cards)

        send_email(recipient, subject, body)
    return "Email has been sent to each user"



from email.message import EmailMessage
import smtplib

SENDER = ""
PASSWORD =""

def send_email(recipient, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SENDER
    msg["To"] = recipient
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SENDER, PASSWORD)
    server.send_message(msg)
    server.quit()

# -------------SEND REPORT EMAIL END ----------



# Run redis database server
  # redis-server #runs automatically in ubuntu on bootup

#Running the celery worker server
 #celery -A celery_batch_job worker --loglevel=info --beat