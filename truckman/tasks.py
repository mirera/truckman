from celery import shared_task 
from .utils import send_email, send_email_with_attachment, send_sms, shorten_url
from django.conf import settings
from django.urls import reverse
from trip.models import Trip, Driver


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

@shared_task
def send_sms_task(sender_id, token, phone_number, message):
    # Call the send_sms function
    send_sms(sender_id, token, phone_number, message)

'''
This task sends a message to the driver.
The message contain shortened url prompting 
driver to add a daily entry.
'''
@shared_task
def send_driver_sms_url_task():
    trips = Trip.objects.all() # from this we get driver and vehicle
    print('Task runs as expectededededed')
    for trip in trips:
        vehicles = trip.load.assigned_trucks.all()
        drivers = Driver.objects.filter(assigned_vehicle__in=vehicles)

        for driver, vehicle in zip(drivers, vehicles):
            url = reverse('add_register_entry', args=[trip.id]) 
            ready_url = shorten_url(url) #append the trip.id to url  
            print(f'This is the url:{ready_url}')
            message = f'Hello {driver.last_name}, click this link {ready_url} to mark daily register. Regards, {driver.company.name}'
            send_sms_task.delay(
                sender_id=settings.SMS_SENDER_ID,
                token=settings.SMS_API_TOKEN, 
                phone_number=driver.tel_roam, 
                message=message
            )
    
# -- end --