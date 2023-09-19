from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required 
from truckman.decorators import permission_required 
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission
from .forms import CustomUserCreationForm, StaffForm, RoleForm, ClientForm
from .models import Client, CustomUser, Role, Preference
from truckman.utils import get_user_company, format_phone_number, deformat_phone_no
from truckman.tasks import send_email_task

#----------------- User Views -------------------------- 
#sign up a user
def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']


            # Create a new client/tenant
            client = Client.objects.create(
                name=company_name,
                email=email,
            )

            # Get all available permissions
            permissions = Permission.objects.filter(
                    content_type__model__in=[
                        'client', 'customuser', 'role', 'vehicle_make',
                        'vehicle_model', 'vehicle', 'driver', 'customer',
                        'consignee', 'shipper', 'load', 'trip', 'estimate',
                        'invoice', 'payment', 'expense', 'expense_category', 'reminder' 
                    ] 
                )

            # Create a superadmin Role i
            role = Role(
                company=client,
                name=client.name +'-admin',
                description='Company admin role.'
            )
            role.save()

            #assign the admin role all permissions
            role.permissions.set(permissions) 

            # Create a new user associated with the client 
            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                company=client,
                role=role
            )
            #assign the created user all the permissions
            user.user_permissions.add(*permissions)

            # activate email token generator
            token_generator = PasswordResetTokenGenerator()
            verify_email_url = request.build_absolute_uri(reverse('verify-email', args=[user.id, token_generator.make_token(user)])) 
            context = {
                'company_name':company_name,
                'user':user.username,
                'verify_email_url':verify_email_url
                }

            #send welcome email 
            send_email_task.delay(
                context=context,
                template_path='authentication/user/company_welcome.html',
                from_name='Loginit',
                from_email=settings.EMAIL_HOST_USER,
                subject='Welcome to Truckman',
                recipient_email=email,
                replyto_email=settings.EMAIL_HOST_USER
            )

            #send email for email verification 
            send_email_task.delay(
                context=context,
                template_path='authentication/user/verify-emailtemplate.html',
                from_name='Loginit',
                from_email=settings.EMAIL_HOST_USER,
                subject='Verify Your Email',
                recipient_email=email,
                replyto_email=settings.EMAIL_HOST_USER
            )
            messages.success(request, 'User created successfully! Please check your email for acount verification.')
            return render(request, 'authentication/user/verify-email.html')
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'authentication/auth-register.html', context)

#--verify email view
def verify_email(request, uid, token):
    # Retrieve the user using the uid
    try:
        user = CustomUser.objects.get(id=uid)
    except CustomUser.DoesNotExist:
        user = None

    if user is not None:
        # Verify the token
        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            # Token is valid
            user.is_verified = True
            user.save()
            messages.success(request, 'Account successfully verified. Please login.')
            # Redirect to the company settings page
            return redirect('global_settings')

        else:
            # Invalid token
            messages.error(request, 'Invalid token! Please try again.')
            return render(request, 'authentication/user/invalid-token.html')
        
    # Invalid user or other error
    context = {
        'user':user,
    }
    messages.error(request, 'Invalid user or other error! Please try again.')
    return render(request, 'authentication/user/invalid-token.html', context=context)
#-- ends

#-- resend email verification token incase it expires
def resend_email_token(request, uid):
    #retrieve the user requesting for resend
    try:
        user = CustomUser.objects.get(id=uid)
    except:
        user = None
    #activate email token generator
    token_generator = PasswordResetTokenGenerator()
    verify_email_url = request.build_absolute_uri(reverse('verify-email', args=[user.id, token_generator.make_token(user)])) 
    context = {
        'user':user.username,
        'verify_email_url':verify_email_url
        }
    #send email for email verification 
    send_email_task.delay(
        context=context,
        template_path='authentication/user/verify-emailtemplate.html',
        from_name='Loginit',
        from_email=settings.EMAIL_HOST_USER,
        subject='Verify Your Email',
        recipient_email=user.email,
        replyto_email=settings.EMAIL_HOST_USER
    )
    messages.success(request, 'Please check your email for account verification.')
    return render(request, 'authentication/user/verify-email.html') 
#-- ends 
    
#login a user
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home') 
            else:
                # Handle inactive user case
                messages.error(request, 'User is inactive!')
                return render(request, 'authentication/auth-login.html')
        else:
            # Handle invalid login case
            messages.error(request, 'Wrong email or password!')
            return render(request, 'authentication/auth-login.html')

    return render(request, 'authentication/auth-login.html') 

#logout a user
def logout_user(request):
    logout(request)
    return redirect('login')

#----------------- Role Views ---------------------------
#add role view
@login_required(login_url='login')
@permission_required('authentication.add_role')
def add_role(request):
    if request.method == 'POST':
        # Get all available permissions
        permissions = Permission.objects.filter(
                content_type__model__in=[
                    'client', 'customuser', 'role', 'vehicle_make',
                    'vehicle_model', 'vehicle', 'driver', 'customer',
                    'consignee', 'shipper', 'load', 'trip', 'estimate',
                    'invoice', 'payment', 'expense', 'expense_category', 'reminder' 
                ] 
            )
        company = get_user_company(request) 

        # Create a Role instance with form data
        role = Role(
            company=company,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        role.save()

        # Get the selected permissions from form 
        selected_permissions = request.POST.getlist('permissions')
        role.permissions.set(selected_permissions)  # Set the selected permissions to the ManyToManyField

        messages.success(request, 'Role created successfully')
        return redirect('list_roles')
    return render(request, 'authentication/role/roles-list.html')

# update role  view
@login_required(login_url='login')
@permission_required('authentication.change_role')
def update_role(request, pk):
    role = Role.objects.get(id=pk)
    if request.method == 'POST':
        company = get_user_company(request)

        #extract form data
        role.name = request.POST.get('name')
        role.description = request.POST.get('description')
        role.save()
        selected_permissions = request.POST.getlist('permissions')

        # Set the selected permissions
        role.permissions.set(selected_permissions) 

        #get role permissions
        permissions = role.permissions.all() 

        #get all users with this role
        users = CustomUser.objects.filter(company=company, role=role)

        #update all users with the updated role permissions
        for user in users:
            user.user_permissions.set(permissions)
            user.save()
 
        messages.success(request, 'Role updated successfully')
        return redirect('list_roles')

    form_data = {
            'name':role.name,
            'description': role.description,
        }
    
    form = RoleForm(initial=form_data)
    context = {
        'form':form,
        'role':role,
    }
    return render(request, 'authentication/role/update-role.html', context)

# role list view
@login_required(login_url='login')
@permission_required('authentication.view_role')
def list_roles(request):
    company = get_user_company(request)
    roles = Role.objects.filter(company=company)
    form = RoleForm(request.POST)
    context = {
        'roles':roles,
        'form':form
    }
    return render(request, 'authentication/role/roles-list.html', context)


#  remove role
@login_required(login_url='login')
@permission_required('authentication.delete_role')
def remove_role(request, pk):
    company = get_user_company(request) 
    role = Role.objects.get(id=pk, company=company)    
    if request.method == 'POST':
        if '-admin' in role.name:
            messages.error(request, "Cannot delete the default role.")
            return redirect('list_roles')
        else:
            role.delete()
            messages.success(request, 'Role deleted successfully!')
            return redirect('list_roles') 

    #context = {'role': role}
    #return render(request, 'authentication/role/roles-list.html', context)
    return redirect('list_roles')

#----------------- Staff Views ---------------------------
#add staff view
@login_required(login_url='login')
@permission_required('authentication.add_customuser')
def add_staff(request):
    company=get_user_company(request)
    form = StaffForm(request.POST, company=company)
    if request.method == 'POST':

        role_id = request.POST.get('role')
        role = Role.objects.get(company=company, id=role_id)

        #retrieve all permissions assigned to a role
        permissions = role.permissions.all() 

        #create instance of a staff
        staff = CustomUser.objects.create(
            company=company,
            username = request.POST.get('email').lower(),
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            email = request.POST.get('email').lower(),
            password = make_password(request.POST.get('password')),
            role = role,
            phone = request.POST.get('phone'),
            designation = request.POST.get('designation'),
            department = request.POST.get('department'),
            date_joined = request.POST.get('date_joined'),
            profile_photo = request.FILES.get('profile_photo'),
        )
        #assign staff role permissions
        staff.user_permissions.add(*permissions)

        #send email
        context = {
            'first_name':staff.first_name,
            'last_name':staff.last_name,
            'username':staff.username,
            'passcode':request.POST.get('password'),
            'company_name':staff.company.name,
            'role':staff.role.name
            }
        preference = Preference.objects.get(company=company)
        send_email_task.delay(
                context=context,
                template_path='authentication/user/staff-welcome.html',
                from_name=preference.email_from_name,
                from_email=preference.from_email,  
                subject=f'Staff Credentials',
                recipient_email=staff.email,
                replyto_email=preference.from_email 
            )

        messages.success(request, f'{staff.first_name} added as staff.')
        return redirect('list_staffs')
    context= {
        'form':form,
    }
    return render(request, 'authentication/staff/staffs-list.html', context)

# update staff  view
@login_required(login_url='login')
@permission_required('authentication.change_customuser')
def update_staff(request, pk):
    company = get_user_company(request) 
    staff = CustomUser.objects.get(id=pk, company=company)
    
    if request.method == 'POST':
        
        role_id = request.POST.get('role')
        role = Role.objects.get(id=role_id, company=company)

        #retrieve all permissions assigned to a role
        permissions = role.permissions.all() 

        staff.company= company
        staff.email = request.POST.get('email').lower()
        staff.username = request.POST.get('email').lower()
        staff.first_name = request.POST.get('first_name')
        staff.last_name = request.POST.get('last_name')
        staff.phone = request.POST.get('phone')
        staff.department = request.POST.get('department')
        staff.designation = request.POST.get('designation')
        staff.profile_photo = request.FILES.get('profile_photo')
        staff.role = role
        staff.save()

        #assign staff role permissions
        staff.user_permissions.add(*permissions)
        
        messages.success(request, 'Staff details updated')

        return redirect('list_staffs')
    else:
        form_data = {
            'email':staff.email,
            'first_name': staff.first_name,
            'last_name': staff.last_name,
            'phone': staff.phone, 
            'department':staff.department,
            'designation':staff.designation,
            'profile_photo':staff.profile_photo,
            'role':staff.role,
        }
    
        form = StaffForm(initial=form_data, company=company)

        context = {
            'form':form, 
            'staff':staff
        }

        return render(request,'authentication/staff/update-staff.html', context )
# -- ends 

# staff list view
@login_required(login_url='login')
@permission_required('authentication.view_customuser')
def list_staffs(request):
    company = get_user_company(request)
    staffs = CustomUser.objects.filter(company=company)
    form = StaffForm(request.POST, company=company)
    context = {
        'staffs':staffs,
        'form':form
    }
    return render(request, 'authentication/staff/staffs-list.html', context)

#  view staff
@login_required(login_url='login')
@permission_required('authentication.view_customuser')
def view_staff(request, pk):
    company = get_user_company(request)
    staff = CustomUser.objects.get(id=pk, company=company)
    context = {
        'staff':staff,
    }
    return render(request, 'authentication/staff/view-staff.html', context)

#remove staff
@login_required(login_url='login')
@permission_required('authentication.delete_customuser')
def remove_staff(request, pk):
    company = get_user_company(request) 
    staff = CustomUser.objects.get(id=pk, company=company)    
    if request.method == 'POST':
        if '-admin' in staff.role.name:
            messages.error(request, "Cannot delete the default admin.")
            return redirect('list_staffs')
        else:
            staff.delete()
            messages.success(request, 'Staff deleted successfully!')
            return redirect('list_staffs') 

    return redirect('list_staffs')

#----------------- User Views ---------------------------
# user profile
@login_required(login_url='login')
def user_profile(request, pk):
    company = get_user_company(request)
    user = CustomUser.objects.get(id=pk)
    
    form_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user.phone
        }
    
    form = StaffForm(initial=form_data, company=company)

    context = {
        'form':form, 
        'user':user    
        }
    return render(request, 'authentication/user/user-profile.html', context)

# update user profile
@login_required(login_url='login')
def update_user_profile(request, pk):
    company = get_user_company(request)
    user = CustomUser.objects.get(id=pk)
    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.save()

        messages.success(request, 'Profile updated succesfully.')

    return redirect('user_profile', user.id)
    #return render(request, 'authentication/user/user-profile.html', context)

#-- prompt user to enter email for resetting password
def forgot_password(request):
    return render(request,'authentication/user/reset-password.html')
#--ends

# Password reset token generator
token_generator = PasswordResetTokenGenerator()

#-- send change password instructions and link.
def resetpass_email_send(request):
    #get the user email from the POST request
    if request.method == 'POST':
        email = request.POST.get('email').lower()

        #raise email/username do not exist in our database error
        try:
            user = CustomUser.objects.get(email=email)
        except:
            user = None
            messages.error(request, 'This email does not exist in our database!')
        if user is not None:
            # Generate the password reset URL parameter user_id and token
            reset_url = request.build_absolute_uri(reverse('password_reset', args=[user.id, token_generator.make_token(user)])) 

            #send the user an email with instruction how to change password and a link 
            context = {
                "user":user.username,
                "reset_url": reset_url
                       }
            send_email_task.delay(
                context=context,
                template_path='authentication/user/reset-instructions.html',
                from_name='Loginit',
                from_email=settings.EMAIL_HOST_USER,
                subject='Loginit Password Reset',
                recipient_email=user.email,
                replyto_email=settings.EMAIL_HOST_USER
            )
            messages.success(request, 'Your request for a password reset has been received. Kindly check your email for further instructions.')
    return render(request,'authentication/user/reset-password.html')
#-- ends

# reset password form
def render_reset_form(request):
    return render(request, 'authentication/user/reset-form.html')
#-- ends

# change password 
def password_reset(request, pk, token):
    # Retrieve user based on id
    try:
        user = CustomUser.objects.get(id=pk)
    except CustomUser.DoesNotExist:
        user=None

    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != password2:
                messages.error(request, 'The passwords do not match! Try again.')
            else:
                # Check password strength
                if len(password1) < 8:
                    messages.error(request, 'Your password must be at least 8 characters long.')
                elif password1.isdigit():
                    messages.error(request, 'Your password must contain at least one letter.')
                elif password1.isalpha():
                    messages.error(request, 'Your password must contain at least one digit.')
                else:
                    # Hash the new password
                    password = make_password(password1)
                    user.password = password
                    user.save()

                    #send email to notify user their password was changed recently
                    forgot_password_url = request.build_absolute_uri(reverse('forgot_password')) 
                    context = {
                        "user":user.username,
                        "forgot_password_url": forgot_password_url
                            }
                    send_email_task.delay(
                        context=context,
                        template_path='authentication/user/reset-success-email.html',
                        from_name='Loginit',
                        from_email=settings.EMAIL_HOST_USER,
                        subject='Your Loginit Truckman password has been updated',
                        recipient_email=user.email,
                        replyto_email=settings.EMAIL_HOST_USER
                    )
                    messages.success(request, 'Your password has been successfully reset.')
                    return redirect('home')           
    else:
        messages.error(request, 'Invalid token!')
        return redirect('forgot_password') 
    context = {
        "user":user,
        "token":token
    }
    return render(request, 'authentication/user/password-reset-form.html', context)
    
#-- ends

#---------------------------------------- client settings views --------------------------------
# client global settings view
@login_required(login_url='login')
@permission_required('authentication.view_client')
def global_settings(request):
    company = get_user_company(request)
    preferences = Preference.objects.get(company=company)

    #old_phone_code = organization.phone_code

    if request.method == 'POST':
        phone_no = request.POST.get('phone_no') 
        phone_code = request.POST.get('phone_code') 
        formatted_phone = format_phone_number(phone_no, phone_code)
        #update company details
        company.name = request.POST.get('name')
        company.email = request.POST.get('email')
        company.phone_no = formatted_phone
        company.country = request.POST.get('country')
        company.city = request.POST.get('city')
        company.logo = request.FILES.get('logo')
        company.address = request.POST.get('address')
        company.invoice_payment_details = request.POST.get('invoice_payment_details')
        company.currency = request.POST.get('currency')
        company.timezone = request.POST.get('timezone')
        company.phone_code = request.POST.get('phone_code')
        company.save()

        
        messages.success(request, 'Preferences updated successfully')
        return redirect('global_settings')
    else:
        # prepopulate the form with existing data
        
        #deformat phone number when displying on form
        deheaded_phone = deformat_phone_no(company.phone_no, company.phone_code)
        form_data = {
            'name': company.name,
            'email': company.email,
            'country': company.country,
            'city': company.city,
            'phone_no': deheaded_phone, 
            'logo': company.logo, 
            'address': company.address,
            'invoice_payment_details': company.invoice_payment_details,
            'currency': company.currency,
            'timezone': company.timezone,
            'phone_code': company.phone_code,
        }
        '''
        # prefill the sms form 
        form_data_sms = {
            'sender_id': sms_setting.sender_id,
            'api_token': sms_setting.api_token,
        }
        # prefill the mpesa form 
        form_data_mpesa = {
            'shortcode': mpesa_setting.shortcode,
            'app_consumer_key': mpesa_setting.app_consumer_key,
            'app_consumer_secret': mpesa_setting.app_consumer_secret,
            'online_passkey': mpesa_setting.online_passkey,
            'username': mpesa_setting.username
        }
        # prefill the email form 
        form_data_email = {
            'from_name': email_setting.from_name,
            'from_email': email_setting.from_email,
            'smtp_host': email_setting.smtp_host,
            'encryption': email_setting.encryption,
            'smtp_port': email_setting.smtp_port,
            'smtp_username': email_setting.smtp_username,
            'smtp_password': email_setting.smtp_password
        }
        # prefill the system preference form 
        form_data_preferences = {
            'is_auto_disburse': preferences.is_auto_disburse,
            'is_send_sms': preferences.is_send_sms,
            'is_send_email': preferences.is_send_email,
            'on_joining': preferences.on_joining,
            'loan_pending': preferences.loan_pending,
            'before_due_date': preferences.before_due_date,
            'missed_payment': preferences.missed_payment,
            'loan_rejected': preferences.loan_rejected,
            'monthly_loan_statement': preferences.monthly_loan_statement,
            'new_loan_products': preferences.new_loan_products,
            'monthly_portfolio_performance': preferences.monthly_portfolio_performance,
        }
       '''
        #form_preferences = PreferenceForm(initial=form_data_preferences)
        #form_email = EmailSettingForm(initial=form_data_email)
        #form_mpesa = MpesaSettingForm(initial=form_data_mpesa)
        #form_sms = SmsForm(initial=form_data_sms)
        form = ClientForm(initial=form_data)
        context = {
            'form':form,
            #'form_sms':form_sms,
            #'form_mpesa':form_mpesa,
            #'form_email':form_email,
            #'form_preferences':form_preferences,
            'company':company,

        }
    return render(request, 'authentication/settings/settings.html', context)

#change logo
def change_logo(request): 
    company = get_user_company(request)
    if request.method == 'POST':
        logo = request.FILES.get('logo')
        company.logo = logo
        company.save()
        return redirect('global_settings')
    
    return redirect('global_settings')
    
def update_sms(request, pk):
    pass

def update_email(request, pk):
    pass

def send_test_email(request, pk):
    pass

def update_preferences(request, pk):
    pass

def disable_2fa(request, pk):
    pass

def enable_2fa(request, pk):
    pass

