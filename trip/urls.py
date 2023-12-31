from django.urls import path
from . import views
 

urlpatterns = [

    #partner/vehicle owner urls
    path('add_partner', views.add_partner, name='add_partner'),
    path('list_partners', views.list_partners, name='list_partners'),
    path('update_partner/<str:pk>', views.update_partner, name='update_partner'),
    path('remove_partner/<str:pk>', views.remove_partner, name='remove_partner'),

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
    path('vehicle_export_to_csv', views.vehicle_export_to_csv, name='vehicle_export_to_csv'),
    #--ends

    #driver urls
    path('add_driver', views.add_driver, name='add_driver'),
    path('update_driver/<str:pk>', views.update_driver, name='update_driver'),
    path('remove_driver/<str:pk>', views.remove_driver, name='remove_driver'),
    path('view_driver/<str:pk>', views.view_driver, name='view_driver'),
    path('list_drivers', views.list_drivers, name='list_drivers'),
    path('driver_export_to_csv', views.driver_export_to_csv, name='driver_export_to_csv'),
    #--ends

    #Customer urls
    path('add_customer', views.add_customer, name='add_customer'),
    path('update_customer/<str:pk>', views.update_customer, name='update_customer'),
    path('remove_customer/<str:pk>', views.remove_customer, name='remove_customer'),
    path('view_customer/<str:pk>', views.view_customer, name='view_customer'),
    path('list_customers', views.list_customers, name='list_customers'),

    path('add_customer_modal', views.add_customer_modal, name='add_customer_modal'),
    path('customer_export_to_csv', views.customer_export_to_csv, name='customer_export_to_csv'),
    #--ends

    #shipper urls
    path('add_shipper', views.add_shipper, name='add_shipper'),
    path('add_shipper_json', views.add_shipper_json, name='add_shipper_json'),
    path('update_shipper/<str:pk>', views.update_shipper, name='update_shipper'),
    path('remove_shipper/<str:pk>', views.remove_shipper, name='remove_shipper'),
    path('view_shipper/<str:pk>', views.view_shipper, name='view_shipper'),
    path('list_shippers', views.list_shippers, name='list_shippers'),
    path('shipper_export_to_csv', views.shipper_export_to_csv, name='shipper_export_to_csv'),
    #--ends

    #Consignee urls
    path('add_consignee', views.add_consignee, name='add_consignee'),
    path('add_consignee_json', views.add_consignee_json, name='add_consignee_json'),
    path('update_consignee/<str:pk>', views.update_consignee, name='update_consignee'),
    path('remove_consignee/<str:pk>', views.remove_consignee, name='remove_consignee'),
    path('view_consignee/<str:pk>', views.view_consignee, name='view_consignee'),
    path('list_consignees', views.list_consignees, name='list_consignees'),

    path('consignee_export_to_csv', views.consignee_export_to_csv, name='consignee_export_to_csv'),
    #--ends

    #load urls
    path('add_load', views.add_load, name='add_load'),
    path('update_load/<str:pk>', views.update_load, name='update_load'),
    path('remove_load/<str:pk>', views.remove_load, name='remove_load'),
    path('view_load/<str:pk>', views.view_load, name='view_load'),
    path('list_loads', views.list_loads, name='list_loads'),
    path('load_export_to_csv', views.load_export_to_csv, name='load_export_to_csv'),
    path('assign_load_trucks/<str:pk>', views.assign_load_trucks, name='assign_load_trucks'),

    path('send_loading_list_customer/<str:pk>', views.send_loading_list_customer, name='send_loading_list_customer'),
    path('download_loading_list_pdf/<str:pk>', views.download_loading_list_pdf, name='download_loading_list_pdf'),
    path('view_loading_list/<str:pk>', views.view_loading_list, name='view_loading_list'),
    #--ends

    #load urls
    path('add_route', views.add_route, name='add_route'),
    path('update_route/<str:pk>', views.update_route, name='update_route'),
    path('remove_route/<str:pk>', views.remove_route, name='remove_route'),
    #path('view_load/<str:pk>', views.view_load, name='view_load'),
    path('list_routes', views.list_routes, name='list_routes'),
    #path('load_export_to_csv', views.load_export_to_csv, name='load_export_to_csv'),
    #--ends

    #trip urls
    path('add_trip', views.add_trip, name='add_trip'),
    path('update_trip/<str:pk>', views.update_trip, name='update_trip'),
    path('remove_trip/<str:pk>', views.remove_trip, name='remove_trip'),
    path('view_trip/<str:pk>', views.view_trip, name='view_trip'),
    path('list_trips', views.list_trips, name='list_trips'),
    path('view_trip/add_payment/<str:pk>', views.add_payment_trip, name='add_payment_trip'),
    path('view_trip/add_expense/<str:pk>', views.add_expense_trip, name='add_expense_trip'),
    path('start_trip/<str:pk>', views.start_trip, name='start_trip'),
    path('get_loading_list/<str:pk>', views.get_loading_list, name='get_loading_list'),

    #send trip doc to shipper url
    path('view_trip/<str:pk>/send_to_shipper', views.send_to_shipper, name='send_to_shipper'),
    path('docs_bulky_action/<str:pk>', views.docs_bulky_action, name='docs_bulky_action'),
    path('trip_export_to_csv', views.trip_export_to_csv, name='trip_export_to_csv'),

    #--ends

    #payment urls
    path('add_payment', views.add_payment, name='add_payment'),
    path('update_payment/<str:pk>', views.update_payment, name='update_payment'),
    path('remove_payment/<str:pk>', views.remove_payment, name='remove_payment'),
    path('view_payment/<str:pk>', views.view_payment, name='view_payment'),
    path('list_payments', views.list_payments, name='list_payments'),
    path('payment_export_to_csv', views.payment_export_to_csv, name='payment_export_to_csv'),
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
    path('expense_export_to_csv', views.expense_export_to_csv, name='expense_export_to_csv'),
    #--ends

    #invoice urls
    #path('add_invoice', views.add_invoice, name='add_invoice'),
    path('update_invoice/<str:pk>', views.update_invoice, name='update_invoice'),
    path('remove_invoice/<str:pk>', views.remove_invoice, name='remove_invoice'),
    path('view_invoice/<str:pk>', views.view_invoice, name='view_invoice'),
    path('list_invoices', views.list_invoices, name='list_invoices'),

    path('send_trip_invoice/<str:pk>', views.send_trip_invoice, name='send_trip_invoice'),
    #path('download_invoice_pdf/<str:pk>', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('get_invoice/<str:pk>', views.get_invoice, name='get_invoice'),
    path('download_invoice_pdf/<str:pk>', views.download_invoice_pdf, name='download_invoice_pdf'),

    #--ends

    #estimate urls
    path('add_estimate', views.add_estimate, name='add_estimate'),
    path('update_estimate/<str:pk>', views.update_estimate, name='update_estimate'),
    path('remove_estimate/<str:pk>', views.remove_estimate, name='remove_estimate'),
    path('view_estimate/<str:pk>', views.view_estimate, name='view_estimate'),
    path('list_estimates', views.list_estimates, name='list_estimates'),

    path('send_estimate/<str:pk>', views.send_estimate, name='send_estimate'),
    path('estimate_negotiate/<str:pk>', views.view_estimate_negotiate_mode, name='view_estimate_negotiate_mode'),
    path('accept_estimate/<str:pk>', views.accept_estimate, name='accept_estimate'),
    path('decline_estimate/<str:pk>', views.decline_estimate, name='decline_estimate'),
    path('generate_associated_invoice/<str:pk>', views.generate_associated_invoice, name='generate_associated_invoice'),
    path('download_estimate_pdf/<str:pk>', views.download_estimate_pdf, name='download_estimate_pdf'),
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

    #-- register entry urls
    path('add_register_entry/<str:pk>/', views.add_register_entry, name='add_register_entry'),

    #-- reports urls
    path('trip_daily_register_report', views.trip_daily_register_report, name='trip_daily_register_report'),
    path('download_daily_report', views.download_daily_report, name='download_daily_report'),
    path('download_day_report/<str:trip_id>', views.download_day_report, name='download_day_report'),#for client

    #-- trip incident urls
    path('add_trip_incident/<str:trip_id>/', views.add_trip_incident, name='add_trip_incident'),
    path('delete_trip_incident/<str:trip_id>/<str:incident_id>/', views.delete_trip_incident, name='delete_trip_incident'),
]