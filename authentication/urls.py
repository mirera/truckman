from django.urls import path
from . import views
 

urlpatterns = [ 
    #organization urls
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'), 
    path('logout', views.logout_user, name='logout'),  
    path('verify-email/<str:uid>/<str:token>', views.verify_email, name='verify-email'),
    path('resend_email_token/<str:uid>', views.resend_email_token, name='resend_email_token'), 

    # organization preferences urls
    path('settings', views.global_settings, name='global_settings'), 
    path('sms/<str:pk>', views.update_sms, name='update_sms'),
    path('email/<str:pk>', views.update_email, name='update_email'),
    path('test-email/<str:pk>', views.send_test_email, name='test_email'),
    path('preferences/<str:pk>', views.update_preferences, name='update_preferences'),
    path('disable-2fa/<str:pk>', views.disable_2fa, name='disable_2fa'),
    path('enable-2fa/<str:pk>', views.enable_2fa, name='enable_2fa'),
    path('change_logo', views.change_logo, name='change_logo'), 

    #role urls
    path('add_role', views.add_role, name='add_role'),
    path('list_roles', views.list_roles, name='list_roles'), 
    #path('view_role/<str:pk>', views.view_role, name='view_role'), 
    path('update_role/<str:pk>', views.update_role, name='update_role'), 
    path('remove_role/<str:pk>', views.remove_role, name='remove_role'), 

    #staff urls
    path('add_staff', views.add_staff, name='add_staff'),
    path('list_staffs', views.list_staffs, name='list_staffs'), 
    path('view_staff/<str:pk>', views.view_staff, name='view_staff'), 
    path('update_staff/<str:pk>', views.update_staff, name='update_staff'), 
    path('remove_staff/<str:pk>', views.remove_staff, name='remove_staff'), 

    #user urls
    path('user_profile/<str:pk>', views.user_profile, name='user_profile'), 
    path('update_user_profile/<str:pk>', views.update_user_profile, name='update_user_profile'), 
    

    path('password_reset/<str:pk>/<str:token>', views.password_reset, name='password_reset'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('resetpass_email_send', views.resetpass_email_send, name='resetpass_email_send'),
    path('render_reset_form', views.render_reset_form, name='render_reset_form'), 
]