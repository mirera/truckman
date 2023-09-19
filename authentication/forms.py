
from django import forms
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError  
from .models import CustomUser, Client, Role
from django.forms.widgets import CheckboxSelectMultiple
from pytz import all_timezones
from iso4217 import Currency
import pycountry
from truckman.utils import phone_codes

#-------------------- Client form -------------------------------------------------------------------
class ClientForm(forms.ModelForm):
    all_currencies = [currency.code for currency in Currency] 


    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in all_timezones],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    currency = forms.ChoiceField(
        choices=[(curr, curr) for curr in all_currencies],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    country = forms.ChoiceField(
        choices=[(country.alpha_2, country.name) for country in pycountry.countries],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    phone_code = forms.ChoiceField(
        choices=phone_codes,
        widget=forms.Select(attrs={'class': 'form-control ', 'style':'background-color:#ebeef2;'})
    )
 
    class Meta:
        model = Client
        fields = '__all__'
        

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enigma Trucks'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'info@loginit.co.ke'}),
                'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0731733333'}),
                'date_joined': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Some address'}),
                'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Sesom'}),
                'invoice_payment_details': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Payment details...'}),
                'logo': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
            }    

#--------------------CustomUser form ---------------------------------------------
class CustomUserCreationForm(forms.Form): 
    company_name = forms.CharField(label='Enter Company Name')
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_company_name(self):
        company_name = self.cleaned_data['company_name'].lower()
        r = Client.objects.filter(name=company_name) 
        if r.count():
            raise  ValidationError("Company name already exists")
        return company_name

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = CustomUser.objects.filter(email=email)
        l = Client.objects.filter(email=email)
        if r.count() or l.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2
    '''
    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            #self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
    '''

#-------------------- Staff form ---------------------------------------------
class StaffForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.filter(company=company) 
    
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude =['company']

        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enigma'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Sesom'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'info@loginit.co.ke'}),
                'password': forms.PasswordInput(attrs={'class': 'form-control'}),
                'role': forms.Select(attrs={'class': 'form-select js-select2'}), 
                'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'254706000000'}),
                'date_joined': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Enigma'}),
                'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Sesom'}),
                'profile_photo': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
            }    

#-------------------- Staff form ---------------------------------------------
class RoleForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    # Move the queryset to the __init__ method
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)

        # Import Permission here to ensure it's loaded at runtime
        from django.contrib.auth.models import Permission

        # Define the queryset based on the loaded Permission model
        self.fields['permissions'] = forms.ModelMultipleChoiceField(
            label='Permissions',
            queryset=Permission.objects.filter(
                content_type__model__in=[
                    'client', 'customuser', 'role', 'vehicle_make',
                    'vehicle_model', 'vehicle', 'driver', 'customer',
                    'consignee', 'shipper', 'load', 'trip', 'estimate',
                    'invoice', 'payment', 'expense', 'expense_category', 'reminder'
                ]
            ),
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-class d-inline'}),
        )

    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control form-control-sm'}),
    )

    def label_from_permission(self, obj):
        return obj.name

   