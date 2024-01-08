from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
import uuid

#--------------------------Client model-----------------------------------------
#client model
class Client(models.Model): 
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True) 
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=14, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to='companies_logo/')
    date_joined = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    currency = models.CharField(max_length=10, default='USD')
    city = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=30, default='Kenya', null=True)
    phone_code = models.CharField(max_length=12, default='+254')
    invoice_payment_details = models.TextField(null=True) 
    
    def get_localized_datetime(self, datetime_value):
        user_timezone = timezone.pytz.timezone(self.timezone)
        localized_datetime = datetime_value.astimezone(user_timezone)
        return localized_datetime
    
    def __str__(self):
        return self.name
    

#--------------------------Preference model-----------------------------------------
#email setting model
HTTPS_ENCRYPTION = (
    ('tls','TLS'),
    ('ssl', 'SSL'),
    ('none', 'NONE')
)

#client prefereces model
class Preference(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True) 
    company = models.ForeignKey(Client, on_delete=models.CASCADE)


    def __str__(self):
        return self.company.name

#client email setting model
class EmailSetting(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True) 
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    email_from_name = models.CharField(max_length=50, null=True) 
    from_email = models.EmailField(blank=True, null=True)
    smtp_host = models.CharField(max_length=200, blank=True, null=True)
    encryption = models.CharField(max_length=200, choices=HTTPS_ENCRYPTION, default='tls')
    smtp_port = models.IntegerField(blank=True, null=True)
    smtp_username = models.EmailField(blank=True, null=True)
    smtp_password = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.company.name

#----------------------------Role model----------------------------------------------------

#Role model

class Role(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True) 
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission, blank=True)
    description = models.TextField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        # Prevent deletion of the default role
        if '-admin' in self.name:
            return
        super().delete(*args, **kwargs) 
    '''
    def save(self, *args, **kwargs):
        # Check if the instance is being edited and the name contains '-admin'
        if self.id is not None and '-admin' in self.name:
            # Fetch the original instance from the database
            original_instance = Role.objects.get(id=self.id)
            # Update the name with the original name
            self.name = original_instance.name
        super().save(*args, **kwargs)
    '''
    def __str__(self):
        return self.name
    

#---------------------------CustomUser model--------------------------------------

class CustomUser(AbstractUser):
    # Specify a unique related_name for groups and user_permissions
    custom_groups = models.ManyToManyField(
        Group,
        verbose_name='custom groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    custom_user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='custom user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True) 
    company = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True)
    department = models.CharField(max_length=20, null=True)
    designation = models.CharField(max_length=30, null=True)
    dark_mode = models.BooleanField(default=False)


#---------------------------WhatsappSetting model--------------------------------------
class WhatsappSetting(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True) 
    company = models.ForeignKey(Client, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, null=True)
    instance_id = models.CharField(max_length=255, null=True)
    
    
    def __str__(self):
        return self.company.name