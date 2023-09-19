from celery import shared_task 
from .utils import send_email, send_email_with_attachment

@shared_task
def hello_engima():
    print('Developed by Loginit Engineers!!') 

@shared_task
def send_email_task(context, template_path, from_name, from_email, subject, recipient_email, replyto_email):
    send_email(
        context, 
        template_path, 
        from_name, 
        from_email, 
        subject, 
        recipient_email, 
        replyto_email,
    ) 

@shared_task
def send_email_with_attachment_task(context, template_path, from_name, from_email, subject, recipient_email, replyto_email, attachment_path):
    send_email_with_attachment(
        context, 
        template_path, 
        from_name, 
        from_email, 
        subject, 
        recipient_email, 
        replyto_email,
        attachment_path
    ) 
