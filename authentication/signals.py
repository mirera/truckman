from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Client, Preference

#setting the profile photo default to 'default.png'
@receiver(pre_save, sender=CustomUser)
def set_default_profile_photo(sender, instance, **kwargs):
    if not instance.profile_photo:
        instance.profile_photo = 'default.png'
# --ends 

#client post_save create preference instance if non exist 
@receiver(post_save, sender=Client)
def create_client_preferences(sender, instance, created, **kwargs): 
    if created:
        #create client preference object
        Preference.objects.create(company=instance)
