from email.message import EmailMessage
import os
from django.core.mail import EmailMessage
class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FORM'),
            to=[data['to_email']]
        )
        email.send()