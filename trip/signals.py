from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from .models import Driver, Load, Trip
from truckman.processes import update_trip_status#, send_trip_vehicle_tURI

#setting the passport photo default to 'default.png'
@receiver(pre_save, sender=Driver)
def set_default_passport_photo(sender, instance, **kwargs):
    if not instance.driver_photo:
        instance.driver_photo = 'default.png'
# --ends

#update trip status when load is saved
@receiver(post_save, sender=Load)
def update_trip_status_on_load_save(sender, instance, **kwargs):
    # Call the function to update trip status when a Load is saved
    update_trip_status(instance)

#update load loaded date when load is saved
@receiver(post_save, sender=Load)
def update_loading_offloading_dates(sender, instance, created, **kwargs):
    if not created:  # Ignore on initial creation
        before_status = instance.status  # Status before saving
        instance.refresh_from_db()  # Refresh instance from the database
        after_status = instance.status  # Status after saving
        if before_status == 'Not Loaded' and after_status == 'On Transit':
            instance.date_loaded = timezone.now().date()
            instance.save()
        elif before_status == 'On Transit' and after_status == 'Delivered':
            instance.date_offloaded = timezone.now().date()
            instance.save()

#send vehicle tacking uris to client when trip status changes to "Dispatched"
@receiver(post_save, sender=Trip)
def send_vehicle_tracking_uri(sender, instance, **kwargs):
    send_trip_vehicle_tURI(Trip)
    

