from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Driver, Load
from truckman.processes import update_trip_status

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
