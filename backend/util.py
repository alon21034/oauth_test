from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import time
import hashlib
import smtplib
import sys
import const
import threading

def generateToken():
    sha = hashlib.sha256()
    sha.update(str(time.time()).encode())
    token = sha.hexdigest()
    return token;

def generatePassword(uuid):
    sha = hashlib.sha256()
    sha.update(uuid.encode())
    token = sha.hexdigest()
    return token;

# TODO: need change to async function
def sendEmail(receivers, message):
    thread = threading.Thread(target=_sendEmail, args=(receivers, message))
    thread.daemon = True
    thread.start() 

def _sendEmail(receivers, message):
 
    emails = [elem.strip().split(',') for elem in receivers]

    msg = MIMEText(message, 'html', 'utf-8')
    msg['Subject'] = const.GREETING_MAIL_TITLE
    msg['From'] = const.SMTP_SENDER
    msg['To'] = ','.join(receivers)

    smtp = smtplib.SMTP("smtp.gmail.com:587")
    smtp.ehlo()
    smtp.starttls()
    smtp.login(const.SMTP_SENDER, const.SMTP_TOKEN)

    smtp.sendmail(msg['From'], emails , msg.as_string())
    print('Send mails to {}'.format(msg['To']))
    return

def getWelcomEmailContent(username):
    return const.GREETING_MAIL_TEMPLATE.format(username)