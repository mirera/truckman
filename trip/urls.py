from django.urls import path
from . import views
 

urlpatterns = [

    #vehicle make urls
    path('add_vehicle_make', views.add_vehicle_make, name='add_vehicle_make'),
    
    #--ends

    #vehicle model urls
    path('add_vehicle_model', views.add_vehicle_model, name='add_vehicle_model'),
    
    #--ends

    #vehicle urls
    path('add_vehicle', views.add_vehicle, name='add_vehicle'),
    path('update_vehicle/<str:pk>', views.update_vehicle, name='update_vehicle'),
    path('remove_vehicle/<str:pk>', views.remove_vehicle, name='remove_vehicle'),
    path('view_vehicle/<str:pk>', views.view_vehicle, name='view_vehicle'),
    path('list_vehicles', views.list_vehicles, name='list_vehicles'),
    #--ends

    #driver urls
    path('add_driver', views.add_driver, name='add_driver'),
    path('update_driver/<str:pk>', views.update_driver, name='update_driver'),
    path('remove_driver/<str:pk>', views.remove_driver, name='remove_driver'),
    path('view_driver/<str:pk>', views.view_driver, name='view_driver'),
    path('list_drivers', views.list_drivers, name='list_drivers'),
    #--ends

    #Customer urls
    path('add_customer', views.add_customer, name='add_customer'),
    path('update_customer/<str:pk>', views.update_customer, name='update_customer'),
    path('remove_customer/<str:pk>', views.remove_customer, name='remove_customer'),
    path('view_customer/<str:pk>', views.view_customer, name='view_customer'),
    path('list_customers', views.list_customers, name='list_customers'),

    path('add_customer_modal', views.add_customer_modal, name='add_customer_modal'),
    #--ends

    #shipper urls
    path('add_shipper', views.add_shipper, name='add_shipper'),
    path('update_shipper/<str:pk>', views.update_shipper, name='update_shipper'),
    path('remove_shipper/<str:pk>', views.remove_shipper, name='remove_shipper'),
    path('view_shipper/<str:pk>', views.view_shipper, name='view_shipper'),
    path('list_shippers', views.list_shippers, name='list_shippers'),
    #--ends

    #Consignee urls
    path('add_consignee', views.add_consignee, name='add_consignee'),
    path('update_consignee/<str:pk>', views.update_consignee, name='update_consignee'),
    path('remove_consignee/<str:pk>', views.remove_consignee, name='remove_consignee'),
    path('view_consignee/<str:pk>', views.view_consignee, name='view_consignee'),
    path('list_consignees', views.list_consignees, name='list_consignees'),
    #--ends

    #load urls
    path('add_load', views.add_load, name='add_load'),
    path('update_load/<str:pk>', views.update_load, name='update_load'),
    path('remove_load/<str:pk>', views.remove_load, name='remove_load'),
    path('view_load/<str:pk>', views.view_load, name='view_load'),
    path('list_loads', views.list_loads, name='list_loads'),
    #--ends

    #trip urls
    path('add_trip', views.add_trip, name='add_trip'),
    path('update_trip/<str:pk>', views.update_trip, name='update_trip'),
    path('remove_trip/<str:pk>', views.remove_trip, name='remove_trip'),
    path('view_trip/<str:pk>', views.view_trip, name='view_trip'),
    path('list_trips', views.list_trips, name='list_trips'),
    path('view_trip/add_payment/<str:pk>', views.add_payment_trip, name='add_payment_trip'),
    path('view_trip/add_expense/<str:pk>', views.add_expense_trip, name='add_expense_trip'),

    #send trip doc to shipper url
    path('view_trip/<str:pk>/send_to_shipper', views.send_to_shipper, name='send_to_shipper'),
    path('docs_bulky_action/<str:pk>', views.docs_bulky_action, name='docs_bulky_action'),

    #--ends

    #payment urls
    path('add_payment', views.add_payment, name='add_payment'),
    path('update_payment/<str:pk>', views.update_payment, name='update_payment'),
    path('remove_payment/<str:pk>', views.remove_payment, name='remove_payment'),
    path('view_payment/<str:pk>', views.view_payment, name='view_payment'),
    path('list_payments', views.list_payments, name='list_payments'),
    #--ends

    #expense category urls
    path('add_expense_category', views.add_expense_category, name='add_expense_category'),
    path('remove_expense_category/<str:pk>', views.remove_expense_category, name='remove_expense_category'),
    path('list_expenses_categories', views.list_expenses_categories, name='list_expenses_categories'),
    #--ends

    #expense urls
    path('add_expense', views.add_expense, name='add_expense'),
    path('update_expense/<str:pk>', views.update_expense, name='update_expense'),
    path('remove_expense/<str:pk>', views.remove_expense, name='remove_expense'),
    path('view_expense/<str:pk>', views.view_expense, name='view_expense'),
    path('list_expenses', views.list_expenses, name='list_expenses'),
    #--ends

    #invoice urls
    path('add_invoice', views.add_invoice, name='add_invoice'),
    path('update_invoice/<str:pk>', views.update_invoice, name='update_invoice'),
    path('remove_invoice/<str:pk>', views.remove_invoice, name='remove_invoice'),
    path('view_invoice/<str:pk>', views.view_invoice, name='view_invoice'),
    path('list_invoices', views.list_invoices, name='list_invoices'),

    path('send_trip_invoice/<str:pk>', views.send_trip_invoice, name='send_trip_invoice'),
    path('generate_invoice_pdf/<str:pk>', views.generate_invoice_pdf, name='generate_invoice_pdf'),

    #--ends

    #estimate urls
    path('add_estimate', views.add_estimate, name='add_estimate'),
    path('update_estimate/<str:pk>', views.update_estimate, name='update_estimate'),
    path('remove_estimate/<str:pk>', views.remove_estimate, name='remove_estimate'),
    path('view_estimate/<str:pk>', views.view_estimate, name='view_estimate'),
    path('list_estimates', views.list_estimates, name='list_estimates'),

    path('send_estimate/<str:pk>', views.send_estimate, name='send_estimate'),
    path('estimate_negotiate/<str:estimate_id>', views.view_estimate_negotiate_mode, name='view_estimate_negotiate_mode'),
    path('accept_estimate/<str:pk>', views.accept_estimate, name='accept_estimate'),
    path('decline_estimate/<str:pk>', views.decline_estimate, name='decline_estimate'),
    #--ends

    #reminder urls
    path('add_reminder', views.add_reminder, name='add_reminder'),
    path('remove_reminder/<str:pk>', views.remove_reminder, name='remove_reminder'),
    path('list_reminders', views.list_reminders, name='list_reminders'),
    #--ends

    #-- frontend request urls
    path('get_trip_info/<str:trip_id>/', views.get_trip_info, name='get_trip_info'),
    path('get_vehicle_info/<str:vehicle_id>/', views.get_vehicle_info, name='get_vehicle_info'),
    path('get_load_info/<str:load_id>/', views.get_load_info, name='get_load_info'),
    path('get_estimate_info/<str:estimate_id>/', views.get_estimate_info, name='get_estimate_info'),

]