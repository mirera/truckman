from celery import shared_task 
from .utils import send_email, send_email_with_attachment, send_sms, shorten_url, create_wa_instance, get_wa_qrcode, send_whatsapp_text, send_whatsapp_media, reset_wa_instance, reconnect_wa_instance, reboot_wa_instance
from django.conf import settings
from django.urls import reverse
#from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from trip.models import Trip, Driver
from authentication.models import WhatsappSetting



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

# -- starts -- 
@shared_task
def create_wa_instance_task(access_token):
    create_wa_instance(access_token)
# -- end --

# -- starts --
@shared_task
def get_wa_qrcode_task(access_token, instance_id):
    get_wa_qrcode(access_token, instance_id)
# -- end --

# -- starts --
@shared_task
def send_whatsapp_text_task(instance_id, access_token, phone_no, message):
    send_whatsapp_text(instance_id, access_token, phone_no, message)
# -- end --

# -- starts --
@shared_task
def send_whatsapp_media_task(instance_id, access_token, phone_no, message, media_url):
    send_whatsapp_media(instance_id, access_token, phone_no, message, media_url)
# -- end --

# -- starts --
@shared_task
def reset_wa_instance_task(access_token, instance_id):
    reset_wa_instance(access_token, instance_id)
# -- end --

# -- starts --
@shared_task
def reconnect_wa_instance_task(access_token, instance_id):
    reconnect_wa_instance(access_token, instance_id)
# -- end --

# -- starts --
@shared_task
def reboot_wa_instance_task(access_token, instance_id):
    reboot_wa_instance(access_token, instance_id)
# -- end --

'''
This task sends a message to the driver.
The message contain shortened url prompting 
driver to add a daily entry.
'''
@shared_task
def send_driver_sms_url_task():
    trips = Trip.objects.filter(status='Dispatched') # from this we get driver and vehicle
    for trip in trips:
        vehicles = trip.load.assigned_trucks.all()
        drivers = Driver.objects.filter(assigned_vehicle__in=vehicles)
        for driver, vehicle in zip(drivers, vehicles):
            trip_id = str(trip.id)
            url = reverse('add_register_entry', args=[trip_id]) 
            #current_site = Site.objects.get_current()
            #domain = settings.DEVELOPMENT_DOMAIN 
            domain = settings.PRODUCTION_DOMAIN #change this when pushing to production server
            full_url = f"{domain}{url}"

            ready_url = shorten_url(full_url) #append the trip.id to url  
            message = f'Hello {driver.first_name} {driver.last_name}, click this link {ready_url} to mark daily register. Regards, {driver.company.name}'
            '''
            send_sms_task.delay(
                sender_id=settings.SMS_SENDER_ID,
                token=settings.SMS_API_TOKEN, 
                phone_number=driver.tel_roam, 
                message=message
            )
            '''
            whatsapp_setting = get_object_or_404(WhatsappSetting, company=trip.company )
            access_token = whatsapp_setting.access_token
            instance_id = whatsapp_setting.instance_id
            
            send_whatsapp_text_task(
                instance_id=instance_id,
                access_token=access_token, 
                phone_no=driver.tel_roam, 
                message=message
            )
# -- end --