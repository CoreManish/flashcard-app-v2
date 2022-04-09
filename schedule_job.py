from models import User, Deck, Card
from jinja2 import Environment, FileSystemLoader
from unicodedata import name
from httplib2 import Http
from json import dumps
import time
from email import message
import imp
from celery import Celery
from flask import render_template
celery = Celery('tasks')
celery.config_from_object('celery_config')

# --------Demo celery task START -----
@celery.task
def add(x, y):
    return x + y
# --------Demo celery task END --------

# ----------ALERT USER TO REVIEW START------------
@celery.task
def sendAlertAsync():
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
#!/usr/bin/env python


@celery.task
def sendReport():
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

SENDER = "21f1006597@student.onlinedegree.iitm.ac.in"
PASSWORD ="mypassword"

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



# make sure celery is running
# run celery
# celery -A schedule_job worker --loglevel=info --beat
# because we are using redis as celery queue and celery result backend
# run redis server (however redis-server is always in run mode)
# redis-server