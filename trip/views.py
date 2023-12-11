from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from truckman.decorators import permission_required
from django.utils import timezone
from datetime import datetime
import pytz
import os
import json
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from authentication.models import Preference
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template
from PyPDF2 import PdfMerger, PdfReader
from PIL import Image
import io
from django.conf import settings
from django.urls import reverse
from django.db.models import Sum
from django.http import FileResponse
from io import BytesIO

from . models import (
    CustomUser,
    Vehicle, 
    Vehicle_Make, 
    Vehicle_Model, 
    Driver, Customer, 
    Consignee, 
    Shipper, 
    Load, 
    Trip,
    Expense,
    Payment,
    Invoice,
    Expense_Category,
    Reminder,
    Estimate,
    Vehicle_Owner,
    Route, 
    BorderStop,
    StopPoint,
    DailyRegister,
    LoadingList,
    LoadingListItem,
    TripIncident, 
    EstimateItem,
    InvoiceItem
    
)

from .forms import (
    VehicleMakeForm,
    VehicleModelForm,
    VehicleForm, 
    DriverForm, 
    CustomerForm, 
    ConsigneeForm, 
    ShipperForm, 
    LoadForm, 
    TripForm,
    ExpenseForm,
    PaymentForm, 
    ExpenseCategoryForm,
    ReminderForm,
    InvoiceForm,
    EstimateForm,
    DailyRegisterForm,
    TripIncidentForm, 
    EstimateItemForm
)

from truckman.utils import get_user_company, enerate_invoice_pdf, export_model_data, reverse_geocode, format_coordinates
from truckman.tasks import send_email_task, send_email_with_attachment_task, send_whatsapp_text_task
from truckman.processes import generate_invoice, generate_loading_list, create_daily_register, get_trip_vehicles, create_workbook
from authentication.models import WhatsappSetting


#---------------------------------- Partner Views------------------------------------------
# add partner 
@login_required(login_url='login')
def add_partner(request):
    company = get_user_company(request) #get request user company
    
    if request.method == 'POST':
        #create instance of vehicle make
        partner = Vehicle_Owner.objects.create(
            company=company,
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            phone = request.POST.get('phone'),
            address = request.POST.get('address')
        )
        return JsonResponse({'success': True, 'partner': {'id': partner.id, 'name': partner.name}})
    else:
        return JsonResponse({'success': False})
#--ends

# add partner 
@login_required(login_url='login')
def update_partner(request, pk):
    partner = get_object_or_404(Vehicle_Owner, id=pk)
    if request.method == 'POST':
        partner.name = request.POST.get('name')
        partner.email = request.POST.get('email')
        partner.phone = request.POST.get('phone')
        partner.address = request.POST.get('address')
        partner.save()

        context = {
            'partner':partner
        }
        messages.success(request, 'Partner details updated')
        return render(request, 'trip/partner/update-partner.html', context)

    context = {
        'partner':partner
    }
    return render(request, 'trip/partner/update-partner.html', context)

# list partners 
@login_required(login_url='login')
def list_partners(request):
    partners = Vehicle_Owner.objects.filter(company=get_user_company(request))
    context = {'partners':partners}
    return render(request, 'trip/partner/partners-list.html', context)
#--ends

# remove partners 
@login_required(login_url='login')
def remove_partner(request, pk):
    partner = get_object_or_404(Vehicle_Owner, id=pk)
    context = {'partner':partner}
    return render(request, 'trip/partner/partners-list.html', context)
#--ends

#---------------------------------- Vehicle Make Views------------------------------------------
# add vehicle make
@login_required(login_url='login')
def add_vehicle_make(request):
    company = get_user_company(request) #get request user company
    
    if request.method == 'POST':
        #create instance of vehicle make
        vehicle_make = Vehicle_Make.objects.create(
            company=company,
            name = request.POST.get('name'),
        )
        return JsonResponse({'success': True, 'make': {'id': vehicle_make.id, 'name': vehicle_make.name}})
    else:
        return JsonResponse({'success': False})
#--ends

#---------------------------------- Vehicle Model Views------------------------------------------
# add vehicle model
@login_required(login_url='login')
def add_vehicle_model(request):
    company = get_user_company(request) #get request user company
    #instantiate the two kwargs to be able to access them on the forms.py
    form = VehicleModelForm(request.POST, company=company) 
    if request.method == 'POST':
        make_id = request.POST.get('make')
        make = Vehicle_Make.objects.get(id=make_id)
        #create instance of vehicle make
        vehicle_model = Vehicle_Model.objects.create(
            company=company,
            name = request.POST.get('name'),
            make=make
        )

        return JsonResponse({'success': True, 'model': {'id': vehicle_model.id, 'name': vehicle_model.name}})
    else:
            return JsonResponse({'success': False})

#--ends

#---------------------------------- Vehicle Views------------------------------------------
# add vehicle
@login_required(login_url='login')
@permission_required('trip.add_vehicle')
def add_vehicle(request):
    company = get_user_company(request) #get request user company
    #instantiate the two kwargs to be able to access them on the forms.py
    form = VehicleForm(request.POST, company=company) 
    vehicle_form = VehicleMakeForm(request.POST)
    vehicle_model_form = VehicleModelForm(request.POST, company=company)
    if request.method == 'POST':
        #get post data
        make_id = request.POST.get('make')
        make = Vehicle_Make.objects.get(id=make_id)
        model_id = request.POST.get('model')
        model= Vehicle_Model.objects.get(id=model_id)

        owner_id = request.POST.get('owner')
        owner= Vehicle_Owner.objects.get(id=owner_id)

        #create instance of vehicle
        vehicle = Vehicle.objects.create(
            company=company,
            owner = owner,
            plate_number = request.POST.get('plate_number'),
            trailer_number = request.POST.get('trailer_number'),
            truck_vin = request.POST.get('truck_vin'),
            trailer_vin = request.POST.get('trailer_vin'),
            make=make,
            model=model,
            milage=request.POST.get('milage'),
            color=request.POST.get('color'),
            trailer_color=request.POST.get('trailer_color'),
            milage_unit = request.POST.get('milage_unit'),
            insurance_expiry = request.POST.get('insurance_expiry'),
            manufacture_year = request.POST.get('manufacture_year'),
            purchase_year = request.POST.get('purchase_year'),
            condition = request.POST.get('condition'),
            notes = request.POST.get('notes'),
            truck_image = request.FILES.get('truck_image'),
            trailer_image = request.FILES.get('trailer_image'),
            truck_logbook = request.FILES.get('truck_logbook'),
            trailer_logbook = request.FILES.get('trailer_logbook'),
            good_transit_licence = request.FILES.get('good_transit_licence'),
            tonnage = int(request.POST.get('tonnage')),
            tracking_uri = request.POST.get('tracking_uri'),
        )

        messages.success(request, f'Vehicle {vehicle.plate_number} was added successfully.')
        return redirect('list_vehicles')
    context= {
        'form':form,
        'vehicle_form':vehicle_form,
        'vehicle_model_form':vehicle_model_form
        }
    return render(request, 'trip/vehicle/add-vehicle.html', context)
#--ends

# update vehicle
@login_required(login_url='login')
@permission_required('trip.change_vehicle')
def update_vehicle(request, pk):
    company = get_user_company(request) #get request user company
    vehicle = Vehicle.objects.get(id=pk, company=company)

    if request.method == 'POST':
        #get post data
        make_id = request.POST.get('make')
        make = Vehicle_Make.objects.get(id=make_id)
        model_id = request.POST.get('model')
        model= Vehicle_Model.objects.get(id=model_id)
        owner_id = request.POST.get('owner')
        owner= Vehicle_Owner.objects.get(id=owner_id)

        #update instance 
        vehicle.company=company
        vehicle.owner = owner
        vehicle.plate_number = request.POST.get('plate_number')
        vehicle.trailer_number = request.POST.get('trailer_number')
        vehicle.truck_vin = request.POST.get('truck_vin')
        vehicle.trailer_vin = request.POST.get('trailer_vin')
        vehicle.make=make
        vehicle.model=model
        vehicle.milage=request.POST.get('milage')
        vehicle.color=request.POST.get('color')
        vehicle.trailer_color=request.POST.get('trailer_color')
        vehicle.milage_unit = request.POST.get('milage_unit')
        vehicle.insurance_expiry = request.POST.get('insurance_expiry')
        vehicle.manufacture_year = request.POST.get('manufacture_year')
        vehicle.purchase_year = request.POST.get('purchase_year')
        vehicle.condition = request.POST.get('condition')
        vehicle.notes = request.POST.get('notes')
        vehicle.good_transit_licence = request.FILES.get('good_transit_licence')
        vehicle.tonnage = int(request.POST.get('tonnage'))
        vehicle.tracking_uri = request.POST.get('tracking_uri')

        # Check if new images/files are provided
        if request.FILES.get('truck_image'):
            vehicle.truck_image = request.FILES.get('drivetruck_imager_photo')

        if request.FILES.get('trailer_image'):
            vehicle.trailer_image = request.FILES.get('trailer_image')

        if request.FILES.get('truck_logbook'):
            vehicle.truck_logbook = request.FILES.get('truck_logbook')

        if request.FILES.get('trailer_logbook'):
            vehicle.trailer_logbook = request.FILES.get('trailer_logbook')

        if request.FILES.get('good_transit_licence'):
            vehicle.good_transit_licence = request.FILES.get('good_transit_licence')

        vehicle.save()
        
        messages.success(request, f'Vehicle {vehicle.plate_number} was edited successfully.')
        return redirect('list_vehicles')
    else:
        # prepopulate the form with existing data
        form_data = {
            'owner': vehicle.owner,
            'plate_number': vehicle.plate_number,
            'trailer_number': vehicle.trailer_number,
            'truck_vin': vehicle.truck_vin,
            'trailer_vin': vehicle.trailer_vin,
            'make': vehicle.make,
            'model': vehicle.model,
            'milage': vehicle.milage,
            'color':vehicle.color,
            'trailer_color':vehicle.trailer_color,
            'milage_unit': vehicle.milage_unit,
            'insurance_expiry': vehicle.insurance_expiry,
            'manufacture_year': vehicle.manufacture_year,
            'purchase_year': vehicle.purchase_year,
            'condition': vehicle.condition,
            'notes': vehicle.notes,
            'tonnage': vehicle.tonnage,
            'tracking_uri':vehicle.tracking_uri,
        }

        form = VehicleForm(initial=form_data, company=company )
        vehicle_form = VehicleMakeForm(request.POST)
        vehicle_model_form = VehicleModelForm(request.POST, company=company)

        context= {
            'vehicle':vehicle,
            'form':form,
            'vehicle_form':vehicle_form,
            'vehicle_model_form':vehicle_model_form
        }
        return render(request,'trip/vehicle/update-vehicle.html',context)
#--ends

#vehicle list
@login_required(login_url='login')
@permission_required('trip.view_vehicle')
def list_vehicles(request):
    vehicles = Vehicle.objects.filter(company=get_user_company(request))
    context = {'vehicles':vehicles}
    return render(request, 'trip/vehicle/vehicle-list.html', context)
#--ends

#view vehicle
@login_required(login_url='login')
@permission_required('trip.view_vehicle')
def view_vehicle(request, pk):
    vehicle = Vehicle.objects.get(id=pk)
    

    try:
        driver = Driver.objects.get(assigned_vehicle=vehicle)
    except:
        driver = None

    context={
        'vehicle':vehicle,
        'driver':driver
        }
    return render(request, 'trip/vehicle/view-vehicle.html', context)
#--ends

# remove vehicle
@login_required(login_url='login')
@permission_required('trip.delete_vehicle')
def remove_vehicle(request, pk):
    if request.method == 'POST':
        vehicle = Vehicle.objects.get(id=pk, company=get_user_company(request))
        vehicle.delete()
        messages.success(request, f'Vehicle {vehicle.plate_number} removed')
        return redirect('list_vehicles')
#--ends

# export vehicle as csv
@login_required(login_url='login')
@permission_required('trip.view_vehicle')
def vehicle_export_to_csv(request):
    header = ['owner','plate_number', 'truck_vin', 'color',  
              'make', 'model', 'milage_unit', 'milage', 
              'trailer_number', 'trailer_vin', 'trailer_color', 
              'insurance_expiry' ,'manufacture_year', 'purchase_year']
    response = export_model_data(request, Vehicle, header)
    return response 


#---------------------------------- Driver views------------------------------------------

# add driver
@login_required(login_url='login')
@permission_required('trip.add_driver')
def add_driver(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = DriverForm(request.POST, company=company) 
    if request.method == 'POST':
        assigned_driver_id  = request.POST.get('assigned_vehicle')
        assigned_vehicle = Vehicle.objects.get(id=assigned_driver_id, company=get_user_company(request))

        #create instance of a driver
        driver = Driver.objects.create(
            #personal data
            company=company,
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            id_no = request.POST.get('id_no'),
            tel_home = request.POST.get('tel_home'),
            tel_roam = request.POST.get('tel_roam'),
            date_hired = request.POST.get('date_hired'),
            driver_photo = request.FILES.get('driver_photo'),
            id_img = request.FILES.get('id_img'),
            #passport and dl data
            dl_no = request.POST.get('dl_no'),
            dl_issuing_authority = request.POST.get('dl_issuing_authority'),
            dl_front_img = request.FILES.get('dl_front_img'),
            dl_back_img = request.FILES.get('dl_back_img'),
            passport_number = request.POST.get('passport_number'),
            passport_image = request.FILES.get('passport_image'),
            #next of kin
            emergency_contact_person = request.POST.get('emergency_contact_person'),
            emergency_contact_person_rlshp = request.POST.get('emergency_contact_person_rlshp'),
            emergency_contact_no = request.POST.get('emergency_contact_no'),

            emergency_contact_person_two = request.POST.get('emergency_contact_person_two'),
            emergency_contact_person_two_rlshp = request.POST.get('emergency_contact_person_two_rlshp'),
            emergency_contact_no_two = request.POST.get('emergency_contact_no_two'),

            emergency_contact_person_three = request.POST.get('emergency_contact_person_three'),
            emergency_contact_person_three_rlshp = request.POST.get('emergency_contact_person_three_rlshp'),
            emergency_contact_no_three = request.POST.get('emergency_contact_no_three'),

            assigned_vehicle = assigned_vehicle,
            status = request.POST.get('status'),
        )

        messages.success(request, f'Driver was added successfully.')
        return redirect('list_drivers')

    context= {'form':form}
    return render(request, 'trip/driver/add-driver.html', context)
#--ends

# update driver
@login_required(login_url='login')
@permission_required('trip.change_driver')
def update_driver(request, pk):
    company = get_user_company(request) #get request user company
    driver = get_object_or_404(Driver, id=pk)
    if request.method == 'POST':
        assigned_vehicle_id  = request.POST.get('assigned_vehicle')
        vehicle = get_object_or_404(Vehicle, id=assigned_vehicle_id)
        #update instance 
        driver.company=company
        driver.first_name = request.POST.get('first_name')
        driver.last_name = request.POST.get('last_name')
        driver.id_no = request.POST.get('id_no')
        driver.tel_home = request.POST.get('tel_home')
        driver.tel_roam = request.POST.get('tel_roam')
        driver.date_hired = request.POST.get('date_hired')

        driver.dl_no = request.POST.get('dl_no')
        driver.passport_number = request.POST.get('passport_number')
        driver.dl_issuing_authority = request.POST.get('dl_issuing_authority')
        
        driver.emergency_contact_person = request.POST.get('emergency_contact_person')
        driver.emergency_contact_person_rlshp = request.POST.get('emergency_contact_person_rlshp')
        driver.emergency_contact_no = request.POST.get('emergency_contact_no')

        driver.emergency_contact_person_two = request.POST.get('emergency_contact_person_two')
        driver.emergency_contact_person_two_rlshp = request.POST.get('emergency_contact_person_two_rlshp')
        driver.emergency_contact_no_two = request.POST.get('emergency_contact_no_two')

        driver.emergency_contact_person_three = request.POST.get('emergency_contact_person_three')
        driver.emergency_contact_person_three_rlshp = request.POST.get('emergency_contact_person_three_rlshp')
        driver.emergency_contact_no_three = request.POST.get('emergency_contact_no_three')
        driver.status = request.POST.get('status')

        driver.assigned_vehicle = vehicle
        vehicle.is_assigned_driver = True
        vehicle.save()
        

        # Check if new images/files are provided
        if request.FILES.get('driver_photo'):
            driver.driver_photo = request.FILES.get('driver_photo')

        if request.FILES.get('id_img'):
            driver.id_img = request.FILES.get('id_img')

        if request.FILES.get('dl_front_img'):
            driver.dl_front_img = request.FILES.get('dl_front_img')

        if request.FILES.get('dl_back_img'):
            driver.dl_back_img = request.FILES.get('dl_back_img')

        if request.FILES.get('passport_image'):
            driver.passport_image = request.FILES.get('passport_image')

        driver.save()
        
        messages.success(request, f'Driver details edited successfully.')
        return redirect('list_drivers')
    else:
        # prepopulate the form with existing data
        form_data = {
            'first_name': driver.first_name,
            'last_name': driver.last_name,
            'id_no': driver.id_no,
            'tel_home': driver.tel_home,
            'tel_roam': driver.tel_roam,
            'date_hired': driver.date_hired,
            'dl_no': driver.dl_no,
            'passport_number': driver.passport_number,
            'dl_issuing_authority': driver.dl_issuing_authority,

            'emergency_contact_person': driver.emergency_contact_person,
            'emergency_contact_person_rlshp': driver.emergency_contact_person_rlshp,
            'emergency_contact_no': driver.emergency_contact_no,

            'emergency_contact_person_two': driver.emergency_contact_person_two,
            'emergency_contact_person_two_rlshp': driver.emergency_contact_person_two_rlshp,
            'emergency_contact_no_two': driver.emergency_contact_no_two,
            
            'emergency_contact_person_three': driver.emergency_contact_person_three,
            'emergency_contact_person_three_rlshp': driver.emergency_contact_person_three_rlshp,
            'emergency_contact_no_three': driver.emergency_contact_no_three,

            'assigned_vehicle': driver.assigned_vehicle,
            'status':driver.status
        }

        form = DriverForm(initial=form_data, company=company )
        context = {
            'driver':driver,
            'form':form
        }
        return render(request,'trip/driver/update-driver.html', context)
#--ends

#drivers list
@login_required(login_url='login')
@permission_required('trip.view_driver')
def list_drivers(request):
    drivers = Driver.objects.filter(company=get_user_company(request))
    number_of_driver = drivers.count()
    context = {
        'drivers':drivers,
        'number_of_driver':number_of_driver
    }
    return render(request, 'trip/driver/drivers-list.html', context)
#--ends

#view driver
@login_required(login_url='login')
@permission_required('trip.view_driver')
def view_driver(request, pk):
    driver = Driver.objects.get(id=pk, company=get_user_company(request))
    context={'driver':driver}
    return render(request, 'trip/driver/view-driver.html', context)
#--ends

# remove driver
@login_required(login_url='login')
@permission_required('trip.delete_driver')
def remove_driver(request, pk):
    if request.method == 'POST':
        driver = Driver.objects.get(id=pk, company=get_user_company(request))
        vehicle = driver.assigned_vehicle

        #free the associated vehicle
        if vehicle:
            vehicle.is_assigned_driver = False
        driver.delete()
        
        messages.success(request, f'Driver {driver.first_name} {driver.last_name} removed')
        return redirect('list_drivers')
#--ends

# export driver as csv
@login_required(login_url='login')
@permission_required('trip.view_driver')
def driver_export_to_csv(request):
    header = ['first_name', 'last_name', 'tel_home', 'tel_roam', 'id_no', 'passport_number', 
              'dl_no', 'dl_issuing_authority', 'status', 'date_hired', 'date_terminated', 
              'emergency_contact_person' ,'emergency_contact_person_rlshp', 'emergency_contact_no',
              'emergency_contact_person_two', 'emergency_contact_person_two_rlshp', 'emergency_contact_no_two',
              'emergency_contact_person_three', 'emergency_contact_person_three_rlshp', 'emergency_contact_no_three',
              'assigned_vehicle' ]
    response = export_model_data(request, Driver, header)
    return response 

#---------------------------------- Customer views------------------------------------------

# add customer
@login_required(login_url='login')
@permission_required('trip.add_customer')
def add_customer(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = CustomerForm(request.POST) 
    if request.method == 'POST':
        #create instance of a customer
        customer = Customer.objects.create(
            company=company,
            name = request.POST.get('name'),
            contact_person = request.POST.get('contact_person'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            address_one = request.POST.get('address_one'),
            address_two = request.POST.get('address_two'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            website = request.POST.get('website'),
            credit_limit = request.POST.get('credit_limit'),
            payment_term = request.POST.get('payment_term'),
            logo = request.FILES.get('logo'),
            tin = request.POST.get('tin'),
            brn = request.POST.get('brn'),
        )

        messages.success(request, f'Customer was added successfully.')
        return redirect('list_customers')

    context= {'form':form}
    return render(request, 'trip/customer/add-customer.html', context)
#--ends

# add customer view for modals
@login_required(login_url='login')
def add_customer_modal(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = CustomerForm(request.POST) 
    if request.method == 'POST':
        #create instance of a customer
        customer = Customer.objects.create(
            company=company,
            name = request.POST.get('name'),
            contact_person = request.POST.get('contact_person'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            address_one = request.POST.get('address_one'),
            address_two = request.POST.get('address_two'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            website = request.POST.get('website'),
            credit_limit = request.POST.get('credit_limit'),
            payment_term = request.POST.get('payment_term'),
            logo = request.FILES.get('logo'),
            tin = request.POST.get('tin'),
            brn = request.POST.get('brn'),
        )
        return JsonResponse({'success': True, 'customer': {'id': customer.id, 'name': customer.name}})
    else:
        return JsonResponse({'success': False})
#--ends

# update customer
@login_required(login_url='login')
@permission_required('trip.change_customer')
def update_customer(request, pk):
    company = get_user_company(request) #get request user company
    customer = Customer.objects.get(id=pk, company=company)
    if request.method == 'POST':
        #update instance 
        customer.company=company
        customer.name = request.POST.get('name')
        customer.contact_person = request.POST.get('contact_person')
        customer.phone = request.POST.get('phone')
        customer.email = request.POST.get('email')
        customer.address_one = request.POST.get('address_one')
        customer.address_two = request.POST.get('address_two')
        customer.country = request.POST.get('country')
        customer.city = request.POST.get('city')
        customer.website = request.POST.get('website')
        customer.credit_limit = request.POST.get('credit_limit')
        customer.payment_term = request.POST.get('payment_term')
        customer.tin = request.POST.get('tin')
        customer.brn = request.POST.get('brn')

        # Check if new images/files are provided
        if request.FILES.get('logo'):
            customer.logo = request.FILES.get('logo')

        customer.save()
        
        messages.success(request, f'Customer details edited successfully.')
        return redirect('list_customers')
    else:
        # prepopulate the form with existing data
        form_data = {
            'name': customer.name,
            'contact_person': customer.contact_person,
            'phone': customer.phone,
            'email': customer.email,
            'address_one': customer.address_one,
            'address_two': customer.address_two,
            'country': customer.country,
            'city': customer.city,
            'website': customer.website,
            'credit_limit': customer.credit_limit,
            'payment_term': customer.payment_term,
            'tin':customer.tin,
            'brn':customer.brn
        }

        form = CustomerForm(initial=form_data)
        context = {
            'customer':customer,
            'form':form
        }
        return render(request,'trip/customer/update-customer.html', context)
#--ends

#customers list
@login_required(login_url='login')
@permission_required('trip.view_customer')
def list_customers(request):
    customers = Customer.objects.filter(company=get_user_company(request))
    number_of_customers = customers.count()
    context = {
        'customers':customers,
        'number_of_customers':number_of_customers
    }
    return render(request, 'trip/customer/customers-list.html', context)
#--ends

#view customer
@login_required(login_url='login')
@permission_required('trip.view_customer')
def view_customer(request, pk):
    customer = Customer.objects.get(id=pk, company=get_user_company(request))
    context={'customer':customer}
    return render(request, 'trip/customer/view-customer.html', context)
#--ends

# remove customer
@login_required(login_url='login')
@permission_required('trip.delete_customer')
def remove_customer(request, pk):
    if request.method == 'POST':
        customer = Customer.objects.get(id=pk, company=get_user_company(request))
        customer.delete()
        messages.success(request, f'Customer {customer.name} removed')
        return redirect('list_customers')
#--ends

# export customer as csv
@login_required(login_url='login')
@permission_required('trip.view_customer')
def customer_export_to_csv(request):
    header = ['customer_id','name', 'contact_person', 'phone',  
              'email', 'address_one', 'address_two', 'country', 
              'city', 'payment_term', 
              'credit_limit' ,'date_added', 'website']
    response = export_model_data(request, Customer, header)
    return response 

#---------------------------------- Consignee views------------------------------------------
# add consignee
@login_required(login_url='login')
@permission_required('trip.add_consignee')
def add_consignee(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ConsigneeForm(request.POST) 
    if request.method == 'POST':
        #create instance of a driver
        consignee = Consignee.objects.create(
            company=company,
            name = request.POST.get('name'),
            contact_person = request.POST.get('contact_person'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            address_one = request.POST.get('address_one'),
            address_two = request.POST.get('address_two'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            website = request.POST.get('website'),
            logo = request.FILES.get('logo'),
        )

        messages.success(request, f'Consignee was added successfully.')
        return redirect('list_consignees') #redirect a user to add load

    context= {'form':form}
    return render(request, 'trip/consignee/add-consignee.html', context)
#--ends

# add shipper view, used within adding/updating load
@login_required(login_url='login')
def add_consignee_json(request):
    company = get_user_company(request) #get request user company
    
    if request.method == 'POST':
        #create instance of a consignee
        consignee = Consignee.objects.create(
            company=company,
            name = request.POST.get('name'),
            contact_person = request.POST.get('contact_person'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            address_one = request.POST.get('address_one'),
            address_two = request.POST.get('address_two'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            website = request.POST.get('website'),
            logo = request.FILES.get('logo'),
        )
        return JsonResponse({'success': True, 'consignee': {'id': consignee.id, 'name': consignee.name}})
    else:
        return JsonResponse({'success': False})
#--ends

# update consignee
@login_required(login_url='login')
@permission_required('trip.change_consignee')
def update_consignee(request, pk):
    company = get_user_company(request) #get request user company
    consignee = Consignee.objects.get(id=pk, company=company)
    if request.method == 'POST':
        #update instance 
        consignee.company=company
        consignee.name = request.POST.get('name')
        consignee.contact_person = request.POST.get('contact_person')
        consignee.phone = request.POST.get('phone')
        consignee.email = request.POST.get('email')
        consignee.address_one = request.POST.get('address_one')
        consignee.address_two = request.POST.get('address_two')
        consignee.country = request.POST.get('country')
        consignee.city = request.POST.get('city')
        consignee.website = request.POST.get('website')

        # Check if new images/files are provided
        if request.FILES.get('logo'):
            consignee.logo = request.FILES.get('logo')

        consignee.save()
        
        messages.success(request, f'Consignee details updated successfully.')
        return redirect('list_consignees')
    else:
        # prepopulate the form with existing data
        form_data = {
            'name': consignee.name,
            'contact_person': consignee.contact_person,
            'phone': consignee.phone,
            'email': consignee.email,
            'address_one': consignee.address_one,
            'address_two': consignee.address_two,
            'country': consignee.country,
            'city': consignee.city,
            'website': consignee.website,
        }

        form = ConsigneeForm(initial=form_data )
        context = {
            'consignee':consignee,
            'form':form
        }
        return render(request,'trip/consignee/update-consignee.html', context)
#--ends

#consignees list
@login_required(login_url='login')
@permission_required('trip.view_consignee')
def list_consignees(request):
    consignees = Consignee.objects.filter(company=get_user_company(request))
    number_of_consignees = consignees.count()
    context = {
        'consignees':consignees,
        'number_of_consignees':number_of_consignees
    }
    return render(request, 'trip/consignee/consignees-list.html', context)
#--ends

#view consignee
@login_required(login_url='login')
@permission_required('trip.view_consignee')
def view_consignee(request, pk):
    consignee = Consignee.objects.get(id=pk, company=get_user_company(request))
    context={'consignee':consignee}
    return render(request, 'trip/consignee/view-consignee.html', context)
#--ends

# remove consignee
@login_required(login_url='login')
@permission_required('trip.delete_consignee')
def remove_consignee(request, pk):
    if request.method == 'POST':
        consignee = Consignee.objects.get(id=pk, company=get_user_company(request))
        consignee.delete()
        messages.success(request, f'Consignee {consignee.name} removed')
        return redirect('list_consignees')
#--ends

# export consignee as csv
@login_required(login_url='login')
@permission_required('trip.view_consignee')
def consignee_export_to_csv(request):
    header = ['consignee_id','name', 'contact_person', 'phone',  
              'email', 'address_one', 'address_two', 'country', 
              'city', 'date_added', 'website']
    response = export_model_data(request, Consignee, header)
    return response 

#ends

#---------------------------------- Shipper views------------------------------------------
# add shipper
@login_required(login_url='login')
@permission_required('trip.add_shipper')
def add_shipper(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ShipperForm(request.POST) 
    if request.method == 'POST':
        #create instance of a shipper
        shipper = Shipper.objects.create(
            company=company,
            name = request.POST.get('name'),
            contact_person = request.POST.get('contact_person'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            address_one = request.POST.get('address_one'),
            address_two = request.POST.get('address_two'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            website = request.POST.get('website'),
            logo = request.FILES.get('logo'),
        )

        messages.success(request, f'Shipper was added successfully.')
        return redirect('list_shippers') #redirect a user to add consignee

    context= {'form':form}
    return render(request, 'trip/shipper/add-shipper.html', context)
#--ends

# add shipper view, used within adding/updating load
@login_required(login_url='login')
def add_shipper_json(request):
    company = get_user_company(request) #get request user company
    
    if request.method == 'POST':
        #create instance of a shipper
        shipper = Shipper.objects.create(
            company=company,
            name = request.POST.get('name'),
            contact_person = request.POST.get('contact_person'),
            phone = request.POST.get('phone'),
            email = request.POST.get('email'),
            address_one = request.POST.get('address_one'),
            address_two = request.POST.get('address_two'),
            country = request.POST.get('country'),
            city = request.POST.get('city'),
            website = request.POST.get('website'),
            logo = request.FILES.get('logo'),
        )
        return JsonResponse({'success': True, 'shipper': {'id': shipper.id, 'name': shipper.name}})
    else:
        return JsonResponse({'success': False})
#--ends

# update shipper
@login_required(login_url='login')
@permission_required('trip.change_shipper')
def update_shipper(request, pk):
    company = get_user_company(request) #get request user company
    shipper = Shipper.objects.get(id=pk, company=company)
    if request.method == 'POST':
        #update instance 
        shipper.company=company
        shipper.name = request.POST.get('name')
        shipper.contact_person = request.POST.get('contact_person')
        shipper.phone = request.POST.get('phone')
        shipper.email = request.POST.get('email')
        shipper.address_one = request.POST.get('address_one')
        shipper.address_two = request.POST.get('address_two')
        shipper.country = request.POST.get('country')
        shipper.city = request.POST.get('city')
        shipper.website = request.POST.get('website')

        # Check if new images/files are provided
        if request.FILES.get('logo'):
            shipper.logo = request.FILES.get('logo')

        shipper.save()
        
        messages.success(request, f'Shipper details updated successfully.')
        return redirect('list_shippers')
    else:
        # prepopulate the form with existing data
        form_data = {
            'name': shipper.name,
            'contact_person': shipper.contact_person,
            'phone': shipper.phone,
            'email': shipper.email,
            'address_one': shipper.address_one,
            'address_two': shipper.address_two,
            'country': shipper.country,
            'city': shipper.city,
            'website': shipper.website,
        }

        form = ShipperForm(initial=form_data )
        context = {
            'shipper':shipper,
            'form':form
        }
        return render(request,'trip/shipper/update-shipper.html', context)
#--ends

#shippers list
@login_required(login_url='login')
@permission_required('trip.view_shipper')
def list_shippers(request):
    shippers = Shipper.objects.filter(company=get_user_company(request))
    number_of_shippers = shippers.count()
    context = {
        'shippers':shippers,
        'number_of_shippers':number_of_shippers
    }
    return render(request, 'trip/shipper/shippers-list.html', context)
#--ends

#view shipper
@login_required(login_url='login')
@permission_required('trip.view_shipper')
def view_shipper(request, pk):
    shipper = Shipper.objects.get(id=pk, company=get_user_company(request))
    context={'shipper':shipper}
    return render(request, 'trip/shipper/view-shipper.html', context)
#--ends

# remove shipper
@login_required(login_url='login')
@permission_required('trip.delete_shipper')
def remove_shipper(request, pk):
    if request.method == 'POST':
        shipper = Shipper.objects.get(id=pk, company=get_user_company(request))
        shipper.delete()
        messages.success(request, f'Shipper {shipper.name} removed')
        return redirect('list_shippers')
#--ends

# export shipper as csv
@login_required(login_url='login')
@permission_required('trip.view_shipper')
def shipper_export_to_csv(request):
    header = ['shipper_id','name', 'contact_person', 'phone',  
              'email', 'address_one', 'address_two', 'country', 
              'city','date_added', 'website']
    response = export_model_data(request, Shipper, header)
    return response 

#---------------------------------- Load views------------------------------------------
# add load
@login_required(login_url='login')
@permission_required('trip.add_load')
def add_load(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = LoadForm(request.POST, company=company) 
    if request.method == 'POST':
        
        shipper_id = request.POST.get('shipper')
        shipper = Shipper.objects.get(company=company, id=shipper_id)

        consignee_id = request.POST.get('consignee')
        consignee = Consignee.objects.get(company=company, id=consignee_id)

        estimate_id = request.POST.get('estimate')
        estimate = Estimate.objects.get(company=company, id=estimate_id)

        #create instance of a load
        load = Load.objects.create(
            company=company,
            shipper = shipper,
            consignee = consignee,
            estimate = estimate,
            quantity = request.POST.get('quantity'),
            quantity_type = request.POST.get('quantity_type'),
            commodity = request.POST.get('commodity'),
            weight = request.POST.get('weight'),
            quote_amount = request.POST.get('quoteAmount'),
            pickup_date = request.POST.get('pickup_date'),
            delivery_date = request.POST.get('delivery_date'),
            driver_instructions = request.POST.get('driver_instructions'),
            legal_disclaimer = request.POST.get('legal_disclaimer'),
            notes = request.POST.get('notes'),
        )

        messages.success(request, f'Load was added successfully.You can now add a Trip here.')
        return redirect('add_trip')

    context= {'form':form}
    return render(request, 'trip/load/add-load.html', context)
#--ends

# update load
@login_required(login_url='login')
@permission_required('trip.change_load')
def update_load(request, pk):
    company = get_user_company(request) #get request user company
    load = Load.objects.get(id=pk, company=company)
    if request.method == 'POST':

        shipper_id = request.POST.get('shipper')
        shipper = Shipper.objects.get(company=company, id=shipper_id)

        consignee_id = request.POST.get('consignee')
        consignee = Consignee.objects.get(company=company, id=consignee_id)

        #update instance 
        load.company = company
        load.shipper = shipper
        load.consignee = consignee
        load.status = request.POST.get('status')
        load.pickup_date = request.POST.get('pickup_date')
        load.weight = request.POST.get('weight')
        load.delivery_date = request.POST.get('delivery_date')
        load.quantity = request.POST.get('quantity')
        load.quantity_type = request.POST.get('quantity_type')
        load.commodity = request.POST.get('commodity')
        load.driver_instructions = request.POST.get('driver_instructions')
        load.legal_disclaimer = request.POST.get('legal_disclaimer')
        load.notes = request.POST.get('notes')
        
        load.save()
        
        messages.success(request, f'Load details updated successfully.')
        return redirect('view_load', load.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'estimate': load.estimate,
            'shipper': load.shipper,
            'consignee': load.consignee,
            'pickup_date': load.pickup_date,
            'weight': load.weight,
            'delivery_date': load.delivery_date,
            'quantity': load.quantity,
            'quantity_type': load.quantity_type,
            'driver_instructions': load.driver_instructions,
            'commodity': load.commodity,
            'legal_disclaimer': load.legal_disclaimer,
            'notes': load.notes,
            'status': load.status
            
        }

        form = LoadForm(initial=form_data, company=company )
        shipper_form = ShipperForm()
        consignee_form = ConsigneeForm()
        context = {
            'load':load,
            'form':form,
            'shipper_form': shipper_form,
            consignee_form:consignee_form
        }
        return render(request,'trip/load/update-load.html', context)
#--ends

#loads list
@login_required(login_url='login')
@permission_required('trip.view_load')
def list_loads(request):
    company = get_user_company(request)
    loads = Load.objects.filter(company=company)
    number_of_loads = loads.count()
    vehicles = Vehicle.objects.filter(company=company, is_available=True)

    
    context = {
        'loads':loads,
        'number_of_loads':number_of_loads, 
        'vehicles':vehicles,
    }
    return render(request, 'trip/load/loads-list.html', context)
#--ends

#view load
@login_required(login_url='login')
@permission_required('trip.view_load')
def view_load(request, pk):
    load = Load.objects.get(id=pk, company=get_user_company(request))
    try:
        loading_list = LoadingList.objects.get(estimate=load.estimate)
        loading_list_items = loading_list.loadinglistitem_set.all()
    except:
        loading_list, loading_list_items = None, None
    context={
        'load':load,
        'loading_list':loading_list,
        'loading_list_items':loading_list_items
        }
    return render(request, 'trip/load/view-load.html', context)
#--ends

# remove load
@login_required(login_url='login')
@permission_required('trip.delete_load')
def remove_load(request, pk):
    if request.method == 'POST':
        load = Load.objects.get(id=pk, company=get_user_company(request))
        load.delete()
        messages.success(request, f'Load of ID: {load.load_id} removed')
        return redirect('list_loads')
#--ends

# export load as csv
@login_required(login_url='login')
@permission_required('trip.view_load')
def load_export_to_csv(request):
    header = ['load_id','shipper', 'consignee', 'quantity',  
              'quantity_type', 'weight', 'commodity', 'pickup_date', 
              'delivery_date', 'quote_amount', 
              'date_added']
    response = export_model_data(request, Load, header)
    return response 
#--ends

#assign truck to a load
def assign_load_trucks(request, pk):
    load = get_object_or_404(Load, id=pk)
    if request.method == 'POST':
        vehicle_id = request.POST.get('selected_vehicle') 
        vehicle = Vehicle.objects.get(pk=vehicle_id) 

        # Assign the selected vehicle to the load
        load.assigned_truck = vehicle
        load.save()

        #set loaded vehicle's available status to 'False'
        vehicle.is_available = False
        vehicle.save()

        # send whatsapp notifications to drivers to load 
        driver = get_object_or_404(Driver, assigned_vehicle=vehicle)
        whatsapp_setting = get_object_or_404(WhatsappSetting, company=load.company )
        
        message = f'Hello {driver.first_name} {driver.last_name}, your truck {vehicle.plate_number} has been assigned a load {load.load_id} of this trip.'
        send_whatsapp_text_task.delay(
            instance_id=whatsapp_setting.instance_id, 
            access_token=whatsapp_setting.access_token, 
            phone_no=driver.tel_roam, 
            message=message
        )

        messages.success(request, 'Load assigned a truck successfully ')
        return redirect('view_load', load.id)

    context = {
        'load':load
       }
    
    return render(request, 'trip/load/loads-list.html' , context)
#--ends

def get_loading_list(request, pk):
    trip = get_object_or_404(Trip, id=pk)  
    print(f'Trip:{trip}')
    estimate = trip.estimate
    print(f'Estimate:{estimate}')
    # Get all the estimate/trip related loads
    loads = Load.objects.filter(estimate=estimate)
    print(f'Count:{loads.count()}')
    # Check if all the loads are assigned trucks
    if all(load.assigned_truck for load in loads):
        # Generate loading list here using `generate_loading_list` function 
        loading_list = generate_loading_list(estimate)
        messages.success(request, 'Loading List generated successfully')
        return redirect('view_trip', trip.id)
    else:
        messages.error(request, 'One or more loads have not been assigned a truck/vehicle. Assign trucks to all trip loads then generate loading list.')
        return redirect('view_trip', trip.id)

#view loading list
def view_loading_list(request, pk):
    loading_list = get_object_or_404(LoadingList, id=pk)
    loading_list_items = loading_list.loadinglistitem_set.all()
    
    
    context = {
        'company':loading_list.company,
        'loading_list_items':loading_list_items,
        'loading_list':loading_list
    }  
    return render(request, 'trip/load/loading-list-template.html', context)

'''
download loading list pdf
'''
def download_loading_list_pdf(request, pk):
    loading_list = get_object_or_404(LoadingList, id=pk)
    loading_list_items = loading_list.loadinglistitem_set.all()

    # Path to  HTML template.
    template_path = 'trip/load/loading-list-template-download.html'

    # Load the HTML template using Django's get_template method.
    template = get_template(template_path)
    context = {
        'company':loading_list.company,
        'loading_list_items':loading_list_items
    }  

    # Render the template with the context data.
    html = template.render(context)

    # Create a response object with PDF content type.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{loading_list.loading_list_id}.pdf"'

    # Create a PDF object using xhtml2pdf's pisa.CreatePDF.
    pdf = pisa.CreatePDF(html, dest=response)

    # Check if PDF generation was successful.
    if not pdf.err:
        return response

    # If PDF generation failed, return an error message.
    return HttpResponse('PDF generation failed: %s' % pdf.err)


#---------------------------------- Route views------------------------------------------
# add route
@login_required(login_url='login')
def add_route(request):
    company = get_user_company(request) #get request user company
    
    if request.method == 'POST':
        distance = int(request.POST.get('distance'))
        estimated_duration = distance // 65 #65 is the average speed of a truck
        #create instance of route
        route = Route.objects.create(
            company=company,
            name = request.POST.get('name'),
            start_point = request.POST.get('start_point'),
            end_point = request.POST.get('end_point'),
            distance = distance,
            duration = estimated_duration,
            description = request.POST.get('description'),
            
        )
        # Add selected border stops and stop points to the route
        selected_border_stops = request.POST.getlist('border_stops')
        selected_stop_points = request.POST.getlist('stop_points')
        
        for stop_id in selected_border_stops:
            border_stop = BorderStop.objects.get(id=stop_id)
            route.border_stops.add(border_stop)
        
        for point_id in selected_stop_points:
            stop_point = StopPoint.objects.get(id=point_id)
            route.stop_points.add(stop_point)

        return JsonResponse({'success': True, 'route': {'id': route.id, 'name': route.name}})
    else:
        return JsonResponse({'success': False})
#--ends

# update route
@login_required(login_url='login')
def update_route(request, pk):
    route = get_object_or_404(Route, id=pk)
    company = get_user_company(request)
    stop_points = StopPoint.objects.filter(company=company)
    border_points = BorderStop.objects.filter(company=company)

    if request.method == 'POST':
        route.name = request.POST.get('name')
        route.start_point = request.POST.get('start_point')
        route.end_point = request.POST.get('end_point')
        route.distance = request.POST.get('distance')
        route.description = request.POST.get('description')
        route.save()

        # Add selected border stops and stop points to the route
        selected_border_stops = request.POST.getlist('border_stops')
        selected_stop_points = request.POST.getlist('stop_points')
        
        for stop_id in selected_border_stops:
            border_stop = BorderStop.objects.get(id=stop_id)
            route.border_stops.add(border_stop)
        
        for point_id in selected_stop_points:
            stop_point = StopPoint.objects.get(id=point_id)
            route.stop_points.add(stop_point)

        context = {
            'route':route,
            
        }
        messages.success(request, 'Route details updated successfully.')
        return render(request, 'trip/route/update-route.html', context)
    
    context = {
        'route':route,
        'border_points':border_points,
        'stop_points':stop_points
    }
    return render(request, 'trip/route/update-route.html', context)

# list routes
@login_required(login_url='login')
def list_routes(request):
    routes = Route.objects.filter(company=get_user_company(request))
    context = {
        'routes':routes
    }
    return render(request,'trip/route/route-list.html', context)

# delete route
@login_required(login_url='login')
def remove_route(request, pk):
    route = get_object_or_404(Route, id=pk)
    route.delete()
    messages.success(request, 'Route deleted successfully')
    return redirect('list_routes')

#---------------------------------- Trip views------------------------------------------
# add trip
@login_required(login_url='login')
@permission_required('trip.add_trip')
def add_trip(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = TripForm(request.POST, company=company)
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        distance = int(request.POST.get('distance')) + 50 #use this to estimate the trip cost.

        #create instance of a trip
        trip = Trip.objects.create(
            company=company,
            load = load,
            driver_accesory_pay = request.POST.get('driver_accesory_pay'),
            #vehicle_odemeter = request.POST.get('vehicle_odemeter'),
            driver_advance = request.POST.get('driver_advance'),
            driver_milage = request.POST.get('driver_advance'),
            pick_up_location = request.POST.get('pick_up_location'),
            drop_off_location = request.POST.get('drop_off_location'),
            distance = distance,
        )
        '''
        description = f"Transport of {trip.load.commodity} from {trip.pick_up_location} to {trip.drop_off_location}, ({trip.distance}kms)"
        invoice_date = timezone.now().date()
        payment_term_days = load.estimate.customer.payment_term
        if payment_term_days == '2 DAYS':
            due_date = invoice_date + timedelta(days=2)
        elif payment_term_days == '7 DAYS' or payment_term_days == 'Cash on Delivery':
            due_date = invoice_date + timedelta(days=7)
        elif payment_term_days == '10 DAYS':
            due_date = invoice_date + timedelta(days=10)
        elif payment_term_days == '15 DAYS':
            due_date = invoice_date + timedelta(days=15)
        elif payment_term_days == '30 DAYS':
            due_date = invoice_date + timedelta(days=30)
        
        downpaymnet = load.estimate.customer.credit_limit / 100 * load.estimate.total
        
        #invoice note based on customer's credit limit and company payment details
        note = f'Downpayment of {load.estimate.customer.credit_limit}% (${downpaymnet}). Pay to:{load.company.invoice_payment_details}'
        #generate a invoice instance
        invoice = Invoice.objects.create(
            company=company,
            trip = trip,
            item = load.estimate.item,
            quantity = load.estimate.quantity,
            unit_price = load.estimate.unit_price,
            description = description,
            sub_total = load.estimate.sub_total,
            tax = load.estimate.tax,
            discount = load.estimate.discount,
            total = load.estimate.total,
            balance = load.estimate.total,
            invoice_date = invoice_date,
            due_date = due_date,
            status = 'Unpaid',
            note = note,

        )
        '''
        messages.success(request, f'Trip was added successfully.')
        return redirect('view_trip', trip.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/trip/add-trip.html', context)
#--ends

# update trip
@login_required(login_url='login')
@permission_required('trip.change_trip')
def update_trip(request, pk):
    company = get_user_company(request) #get request user company
    trip = Trip.objects.get(id=pk, company=company)
    if request.method == 'POST':

        #update instance 
        trip.driver_accesory_pay = request.POST.get('driver_accesory_pay')
        
        trip.driver_advance = request.POST.get('driver_advance')
        trip.driver_milage = request.POST.get('driver_milage')
        trip.save()
        
        messages.success(request, f'Trip details updated successfully.')
        return redirect('view_trip', trip.id)
    else:
        # prepopulate the form with existing data
        form_data = {

            'driver_accesory_pay': trip.driver_accesory_pay,
            
            'driver_advance': trip.driver_advance,
            'driver_milage': trip.driver_milage,
        }

        form = TripForm(initial=form_data, company=company )
        context = {
            'trip':trip,
            'form':form
        }
        return render(request,'trip/trip/update-trip.html', context)
#--ends

#trip list
@login_required(login_url='login')
@permission_required('trip.view_trip')
def list_trips(request):
    trips = Trip.objects.filter(company=get_user_company(request))
    total_trips = trips.count()
    completed_trips = trips.filter(status='Completed').count()
    trips_on_transit = trips.filter(status='Dispatched').count()
    trip_not_started = trips.filter(status='Not Started').count()

    context = {
        'trips':trips,
        'total_trips':total_trips,
        'completed_trips':completed_trips,
        'trips_on_transit':trips_on_transit,
        'trip_not_started':trip_not_started
    }
    return render(request, 'trip/trip/trips-list.html', context)
#--ends

#view trip
@login_required(login_url='login')
@permission_required('trip.view_trip')
def view_trip(request, pk):
    company=get_user_company(request)
    trip = get_object_or_404(Trip, id=pk)

    expenses = Expense.objects.filter(company=company, trip=trip)
    loads = Load.objects.filter(estimate=trip.estimate)

    loaded_loads = loads.filter(status__in=['On Transit', 'Delivered']).count()
    delivered_loads = loads.filter(status='Delivered').count()

    try:
        loading_list = LoadingList.objects.get(estimate=trip.estimate)
        loading_list_items = loading_list.loadinglistitem_set.all()
    except:
        loading_list, loading_list_items = None, None

    try:
        invoice = Invoice.objects.get(estimate=trip.estimate)
    except:
        invoice = None

    invoice_items = InvoiceItem.objects.filter(invoice=invoice)
    

    try:
        payments = Payment.objects.filter(company=company, invoice=invoice) #invoice in invoices associated with the trip 
        documents = ''
    except:
        payments, documents = None, None

    form = ExpenseForm(request.POST, company=company) # for expense modal
    category_form = ExpenseCategoryForm(request.POST) # for expense category modal
    payment_form = PaymentForm(request.POST, company=company) # for payment modal
    
    trip_incidents = TripIncident.objects.filter(trip=trip) 
    incident_form = TripIncidentForm(request.POST, company=company)  
        
    context={
        'company':company,
        'trip':trip,
        'expenses':expenses,
        'invoice':invoice,
        'invoice_items':invoice_items,
        'payments':payments,
        'form':form,
        'category_form':category_form,
        'payment_form':payment_form,
        'documents':documents,
        'trip_incidents':trip_incidents,
        'incident_form':incident_form,
        'loading_list':loading_list,
        'loading_list_items':loading_list_items,
        'loads':loads,
        'loaded_loads':loaded_loads,
        'delivered_loads':delivered_loads,

    }
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

#send all trip document to shipper
@login_required(login_url='login')
@permission_required('trip.view_trip')
def send_to_shipper(request, pk):
    company = get_user_company(request)
    trip = Trip.objects.get(id=pk, company=company)
    shipper = trip.load.shipper
    vehicle = trip.vehicle
    driver = Driver.objects.get(assigned_vehicle=vehicle)

    # Create a PDF file with all trip documents
    merger = PdfMerger()

    all_trip_documents = [
        trip.vehicle.truck_logbook,
        trip.vehicle.trailer_logbook,
        trip.vehicle.truck_image,
        trip.vehicle.trailer_image, 
        trip.vehicle.good_transit_licence,
        driver.driver_photo,
        driver.id_img,
        driver.dl_front_img,
        driver.dl_back_img,
        driver.passport_image
    ]

    for document in all_trip_documents:
        # Check the file extension to determine the document type
        file_extension = os.path.splitext(document.name)[1].lower()

        if file_extension == ".pdf":
            # If the document is already a PDF, add it directly to the merger
            pdf_reader = PdfReader(open(document.path, 'rb'))
            merger.append(pdf_reader)
        elif file_extension in (".png", ".jpg", ".jpeg"):
            # If the document is an image (PNG or JPG), convert it to PDF using PIL
            image = Image.open(document.path)
            pdf_buffer = io.BytesIO()
            image.save(pdf_buffer, "PDF")
            pdf_buffer.seek(0)

            # Create a temporary PDF file for the converted image
            temp_pdf_path = f"temp_image.pdf"
            with open(temp_pdf_path, "wb") as temp_pdf_file:
                temp_pdf_file.write(pdf_buffer.read())

            # Open the temporary PDF and add it to the merger
            pdf_reader = PdfReader(open(temp_pdf_path, 'rb'))
            merger.append(pdf_reader)
            
            # Remove the temporary PDF file
            os.remove(temp_pdf_path)

    # Save the merged PDF to a file or send it by email
    merged_pdf_path = f"trip_docs/merged_trip_documents.pdf"
    merger.write(open(merged_pdf_path, 'wb'))
    merger.close()

    #send email
    context = {
        'company':company.name,
        'shipper':shipper.name,
        
    }
    send_email_with_attachment_task(
        context=context, 
        template_path='trip/trip/trip-docs-email.html', 
        from_name=company.name, 
        from_email=company.email, 
        subject="All Trip Documents", 
        recipient_email=shipper.email, 
        replyto_email=company.email,
        attachment_path=merged_pdf_path,  # Attach the merged PDF doc
    )

    messages.success(request, 'Documents sent to the shipper successfully')
    return redirect('view_trip', trip.id)

#trip docs bulky action view 
def docs_bulky_action(request, pk):
    company=get_user_company(request)
    if request.method == 'POST':
        print('Its a post request')
        # Retrieve the selected option from the form data
        bulk_action = request.POST.get('bulk-action')
        print(f'This is the sellected bulk action{bulk_action}')
        selected_ids = request.POST.getlist('selected_ids')
        selected_docs = []
        trip = Trip.objects.get(id=pk)

        if bulk_action == 'share':
            #send as email to provided email
            pdf_documents = []
            context = {
                'company':company.name,
                'pdf_documents':pdf_documents
            }
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            send_email_task(
                context=context, 
                template_path='trip/trip/share-doc-email.html', 
                from_name=company.name, 
                from_email=company.email, 
                subject=subject, 
                recipient_email=email, 
                replyto_email=company.email
            )
            messages.success(request, 'Messages sent.')
            return redirect('view_trip', trip.id)

        elif bulk_action == 'send':
            #send selected docs to shipper
            messages.success(request, 'Sent to shipper.')
            return redirect('view_trip', trip.id)
        
        elif bulk_action == 'download':
            #download selected docs
            messages.success(request, 'Documents downloading...')
            return redirect('view_trip', trip.id)

    return redirect('view_trip', trip.id)

# remove trip
@login_required(login_url='login')
@permission_required('trip.delete_trip')
def remove_trip(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

# export trip as csv
@login_required(login_url='login')
@permission_required('trip.view_trip')
def trip_export_to_csv(request):
    header = ['trip_id','load', 'pick_up_location', 'drop_off_location',  
              'distance', 'status', 'start_time', 'end_time', 'date_added']
    response = export_model_data(request, Trip, header)
    return response 

#start trip view
@login_required(login_url='login')
@permission_required('trip.view_trip')
def start_trip(request, pk):
    company = get_user_company(request)
    trip = get_object_or_404(Trip, id=pk)
    if trip.status == 'Not Started' and trip.load.assigned_trucks.all() :
        trip.status = 'Dispatched'
        trip.save()

        #generate invoice form estimate 
        invoice = generate_invoice(trip.load.estimate)
        preference = get_object_or_404(Preference, company=company) 

        invoice_url = request.build_absolute_uri(reverse('view_invoice', args=[invoice.id]))

        context = {
            'customer_name': trip.load.estimate.customer.name,
            'invoice_url' : invoice_url,
            'company_name':company.name
        }

        send_email_task.delay(
            context=context,  
            template_path='trip/invoice/trip-invoice.html', 
            from_name=preference.email_from_name, 
            from_email=preference.from_email, 
            subject=f'Trip Started - Trip Invoice:{invoice.invoice_id}', 
            recipient_email=trip.load.estimate.customer.email, 
            replyto_email=company.email,
        )

        '''
        send_email_with_attachment_task.delay(
            context=context,  
            template_path='trip/invoice/trip-invoice.html', 
            from_name=preference.email_from_name, 
            from_email=preference.from_email, 
            subject=f'Trip Started - Trip Invoice:{invoice.invoice_id}', 
            recipient_email=trip.load.estimate.customer.email, 
            replyto_email=company.email,
            attachment_path=invoice_path
        )
        '''

        messages.success(request, 'Trip started successfully.')
    elif trip.status == 'Dispatched':
        messages.info(request, 'Trip already dispatched.')
    else:
        messages.info(request, 'Trip already completed.')
    return redirect('view_trip', trip.id )

#---------------------------------- Payment views------------------------------------------

# add payment
@login_required(login_url='login')
@permission_required('trip.add_payment')
def add_payment(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = PaymentForm(request.POST, company=company) 
    if request.method == 'POST':

        invoice_id = request.POST.get('invoice')
        invoice = Invoice.objects.get(company=company, id=invoice_id)
        amount = int(request.POST.get('amount'))

        #create instance of a payment
        payment = Payment.objects.create(
            company=company,
            transaction_id = request.POST.get('transaction_id'),
            invoice = invoice,
            amount = amount,
            paid_on = request.POST.get('paid_on'),
            payment_method = request.POST.get('payment_method'),
            remark = request.POST.get('remark'),
        )

        #update invoice balance
        invoice.balance = invoice.balance - amount

        # Update invoice status
        if invoice.balance <= 0:
            invoice.status = 'Paid'
        elif invoice.balance == invoice.total:
            invoice.status = 'Unpaid'
        else:
            invoice.status = 'Partially Paid'
        invoice.save()
  
        #send email to client

        messages.success(request, f'Payment was added and receipt sent to the customer successfuly.')
        return redirect('view_invoice', invoice.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/payment/payment-list.html', context)
#--ends

# add payment inside a trip
@login_required(login_url='login')
@permission_required('trip.add_payment')
def add_payment_trip(request, pk):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = PaymentForm(request.POST, company=company) 
    if request.method == 'POST':

        trip = Trip.objects.get(id=pk)
        invoice = Invoice.objects.get(estimate=trip.load.estimate) 
        amount = float(request.POST.get('amount'))

        #create instance of a payment
        payment = Payment.objects.create(
            company=company,
            transaction_id = request.POST.get('transaction_id'),
            invoice = invoice,
            amount = amount,
            paid_on = request.POST.get('paid_on'),
            payment_method = request.POST.get('payment_method'),
            remark = request.POST.get('remark'),
        )

        #update invoice balance
        invoice.balance = invoice.balance - amount

        # Update invoice status
        if invoice.balance <= 0:
            invoice.status = 'Paid'
        elif invoice.balance == invoice.total:
            invoice.status = 'Unpaid'
        else:
            invoice.status = 'Partially Paid'
        invoice.save()
  
        #send email to client

        messages.success(request, f'Payment was added and receipt sent to the customer successfuly.')
        return redirect('view_trip', trip.id)

    context= {
        'form':form,
    }
    return render(request, 'trip/payment/payment-list.html', context)
#--ends

# update trip
@login_required(login_url='login')
@permission_required('trip.change_payment')
def update_payment(request, pk):
    company = get_user_company(request) #get request user company
    trip = Trip.objects.get(id=pk, company=company)
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        #update instance 
        trip.company = company
        trip.load = load
        trip.driver_accesory_pay = request.POST.get('driver_accesory_pay')
        trip.driver_advance = request.POST.get('driver_advance')
        trip.save()
        
        messages.success(request, f'Trip details updated successfully.')
        return redirect('view_trip', trip.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'load': trip.load,
            'driver_accesory_pay': trip.driver_accesory_pay,
            'driver_advance': trip.driver_advance
        }

        form = TripForm(initial=form_data, company=company )
        context = {
            'trip':trip,
            'form':form
        }
        return render(request,'trip/trip/update-trip.html', context)
#--ends

#trip list
@login_required(login_url='login')
@permission_required('trip.view_payment')
def list_payments(request):
    payments = Payment.objects.filter(company=get_user_company(request))
    form = PaymentForm(request.POST, company=get_user_company(request)) 
    context = {
        'payments':payments,
        'form':form,
    }
    return render(request, 'trip/payment/payment-list.html', context)
#--ends

#view trip
@login_required(login_url='login')
@permission_required('trip.view_payment')
def view_payment(request, pk):
    trip = Trip.objects.get(id=pk, company=get_user_company(request))
    context={'trip':trip}
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
@login_required(login_url='login')
@permission_required('trip.delete_payment')
def remove_payment(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

# export payment as csv
@login_required(login_url='login')
@permission_required('trip.view_trip')
def payment_export_to_csv(request):
    header = ['payment_id', 'transaction_id', 'invoice', 'amount',  
              'paid_on', 'payment_method', 'remark']
    response = export_model_data(request, Payment, header)
    return response 

#---------------------------------- Expense Category views------------------------------------------

# add expense category
@login_required(login_url='login')
@permission_required('trip.add_expense_category')
def add_expense_category(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ExpenseCategoryForm(request.POST) 
    if request.method == 'POST':

        #create instance of a driver
        category = Expense_Category.objects.create(
            company=company,
            name = request.POST.get('name')
        )

        return JsonResponse({'success': True, 'category': {'id': category.id, 'name': category.name}})
    else:
        return JsonResponse({'success': False})

#--ends


#expense category list
@login_required(login_url='login')
@permission_required('trip.view_expense_category')
def list_expenses_categories(request):
    expenses = Expense.objects.filter(company=get_user_company(request))
    form = ExpenseForm(request.POST, company=get_user_company(request)) 
    category_form = ExpenseCategoryForm(request.POST)
    context = {
        'expenses':expenses,
        'form':form,
        'category_form':category_form
       }
    return render(request, 'trip/expense/expense-list.html', context)
#--ends

# remove expense category
@login_required(login_url='login')
@permission_required('trip.delete_expense_category')
def remove_expense_category(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#---------------------------------- Expense views--------------------------------------------------

# add expense
@login_required(login_url='login')
@permission_required('trip.add_expense')
def add_expense(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ExpenseForm(request.POST, company=company) 
    if request.method == 'POST':

        trip_id = request.POST.get('trip')
        trip = Trip.objects.get(company=company, id=trip_id)

        expense_category_id = request.POST.get('expense_category')
        expense_category = Expense_Category.objects.get(company=company, id=expense_category_id)

        #create instance of a driver
        expense = Expense.objects.create(
            company=company,
            trip = trip,
            expense_category = expense_category,
            amount = request.POST.get('amount'),
            date_paid = request.POST.get('date_paid'),
            paid_to = request.POST.get('paid_to'),
            receipt = request.FILES.get('receipt'),
        )

        messages.success(request, f'Expense was added successfully.')
        return redirect('list_expenses')

    context= {
        'form':form,
    }
    return render(request, 'trip/expense/expense-list.html', context)
#--ends

# add expense inside a trip 
@login_required(login_url='login')
@permission_required('trip.add_expense')
def add_expense_trip(request, pk):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ExpenseForm(request.POST, company=company) 
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk)

        expense_category_id = request.POST.get('expense_category')
        expense_category = Expense_Category.objects.get(company=company, id=expense_category_id)

        #create instance of a driver
        expense = Expense.objects.create(
            company=company,
            trip = trip,
            expense_category = expense_category,
            amount = request.POST.get('amount'),
            date_paid = request.POST.get('date_paid'),
            paid_to = request.POST.get('paid_to'),
            receipt = request.FILES.get('receipt'),
        )

        messages.success(request, f'Expense was added successfully.')
        return redirect('view_trip', trip.id )

    context= {
        'form':form,
    }
    return render(request, 'trip/expense/expense-list.html', context)
#--ends

# update trip
@login_required(login_url='login')
@permission_required('trip.change_expense')
def update_expense(request, pk):
    company = get_user_company(request) #get request user company
    trip = Trip.objects.get(id=pk, company=company)
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        driver_id = request.POST.get('driver')
        driver = Driver.objects.get(company=company, id=driver_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)
        #update instance 
        trip.company = company
        trip.driver = driver
        trip.load = load
        trip.vehicle = vehicle
        trip.driver_accesory_pay = request.POST.get('driver_accesory_pay')
        trip.vehicle_odemeter = request.POST.get('vehicle_odemeter')
        trip.driver_advance = request.POST.get('driver_advance')
        trip.save()
        
        messages.success(request, f'Trip details updated successfully.')
        return redirect('view_trip', trip.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'driver': trip.driver,
            'load': trip.load,
            'vehicle': trip.vehicle,
            'driver_accesory_pay': trip.driver_accesory_pay,
            'vehicle_odemeter': trip.vehicle_odemeter,
            'driver_advance': trip.driver_advance
        }

        form = TripForm(initial=form_data, company=company )
        context = {
            'trip':trip,
            'form':form
        }
        return render(request,'trip/trip/update-trip.html', context)
#--ends

#trip list
@login_required(login_url='login')
@permission_required('trip.view_expense')
def list_expenses(request):
    expenses = Expense.objects.filter(company=get_user_company(request)) 
    form = ExpenseForm(request.POST, company=get_user_company(request)) 
    category_form = ExpenseCategoryForm(request.POST)
    context = {
        'expenses':expenses,
        'form':form,
        'category_form':category_form
       }
    return render(request, 'trip/expense/expense-list.html', context)
#--ends

#view trip
@login_required(login_url='login')
@permission_required('trip.view_expense')
def view_expense(request, pk):
    trip = Trip.objects.get(id=pk, company=get_user_company(request))
    context={'trip':trip}
    return render(request, 'trip/trip/view-trip.html', context)
#--ends

# remove trip
@login_required(login_url='login')
@permission_required('trip.delete_expense')
def remove_expense(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

# export payment as csv
@login_required(login_url='login')
@permission_required('trip.view_expense')
def expense_export_to_csv(request):
    header = ['expense_id', 'expense_category', 'vehicle', 'trip', 'amount',  
              'paid_to', 'date_paid']
    response = export_model_data(request, Expense, header)
    return response 


#---------------------------------- Invoice views------------------------------------------
# add invoice
'''
@login_required(login_url='login')
@permission_required('trip.add_invoice')
def add_invoice(request, pk):
    company = get_user_company(request)
    estimate = Estimate.objects.get(id=pk) 
    if request.method == 'POST':
        #invoice = generate_invoice(estimate)
        messages.success(request, f'Invoice was added successfully.')
        return redirect('view_invoice', invoice.id)

    return render(request, 'trip/invoice/add-invoice.html', context)
#--ends
'''
#generate an invoice given estimate
@login_required(login_url='login')
def get_invoice(request, pk):
    trip = get_object_or_404(Trip, id=pk)
    if trip.status in ['Dispatched', 'Completed']:
        invoice = generate_invoice(trip.estimate)
        messages.success(request, 'Invoice generated successfully.')
        return redirect('view_trip', trip.id)
    else:
        messages.error(request, 'One or more Load(s) must be of status "loaded" to generate an invoice.')
        return redirect('view_trip', trip.id)

# update trip
@login_required(login_url='login')
@permission_required('trip.change_invoice')
def update_invoice(request, pk):
    company = get_user_company(request) #get request user company
    trip = Trip.objects.get(id=pk, company=company)
    if request.method == 'POST':

        load_id = request.POST.get('load')
        load = Load.objects.get(company=company, id=load_id)

        driver_id = request.POST.get('driver')
        driver = Driver.objects.get(company=company, id=driver_id)

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)
        #update instance 
        trip.company = company
        trip.driver = driver
        trip.load = load
        trip.vehicle = vehicle
        trip.driver_accesory_pay = request.POST.get('driver_accesory_pay')
        trip.vehicle_odemeter = request.POST.get('vehicle_odemeter')
        trip.driver_advance = request.POST.get('driver_advance')
        trip.save()
        
        messages.success(request, f'Trip details updated successfully.')
        return redirect('view_trip', trip.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'driver': trip.driver,
            'load': trip.load,
            'vehicle': trip.vehicle,
            'driver_accesory_pay': trip.driver_accesory_pay,
            'vehicle_odemeter': trip.vehicle_odemeter,
            'driver_advance': trip.driver_advance
        }

        form = TripForm(initial=form_data, company=company )
        context = {
            'trip':trip,
            'form':form
        }
        return render(request,'trip/trip/update-trip.html', context)
#--ends

#trip list
@login_required(login_url='login')
@permission_required('trip.view_invoice')
def list_invoices(request):
    invoices = Invoice.objects.filter(company=get_user_company(request))
    context = {
        'invoices':invoices,
    }
    return render(request, 'trip/invoice/invoices-list.html', context)
#--ends

#view trip
@login_required(login_url='login')
@permission_required('trip.view_invoice')
def view_invoice(request, pk):
    company = get_user_company(request)
    invoice = Invoice.objects.get(id=pk, company=get_user_company(request))
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)

    context={
        'invoice':invoice,
        'company':company,
        'invoice_items':invoice_items
    }
    return render(request, 'trip/invoice/view-invoice.html', context)
#--ends

# remove trip
@login_required(login_url='login')
@permission_required('trip.delete_invoice')
def remove_invoice(request, pk):
    if request.method == 'POST':
        trip = Trip.objects.get(id=pk, company=get_user_company(request))
        trip.delete()
        messages.success(request, f'Trip of id : {trip.trip_id} removed')
        return redirect('list_trips')
#--ends

#send trip invoice
@login_required(login_url='login')
@permission_required('trip.view_invoice') 
def send_trip_invoice(request, pk):
    company = get_user_company(request)
    trip = get_object_or_404(Trip, id=pk, company=company)
    invoice = Invoice.objects.get(trip=trip)
    preference = Preference.objects.get(company=company)

    #having this context because delay() need model serialzation
    context = {
        'customer_name': trip.load.estimate.customer.name,
    }

    pdf_invoice = enerate_invoice_pdf(trip)

    send_email_with_attachment_task.delay(
        context=context,  
        template_path='trip/invoice/trip-invoice.html', 
        from_name=preference.email_from_name, 
        from_email=preference.from_email, 
        subject=f'Trip Invoice:{invoice.invoice_id}', 
        recipient_email=trip.load.estimate.customer.email, 
        replyto_email=company.email,
        attachment_path=invoice_path
    )

    messages.success(request, 'Invoice sent to customer.')
    return redirect('view_trip', trip.id)

# generate invoice pdf view 
def generate_invoice_pdf(request, pk):
    company = get_user_company(request)
    trip = Trip.objects.get(id=pk, company=company)
    invoice = Invoice.objects.get(estimate=trip.estimate)
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)

    #enerate_invoice_pdf(invoice, invoice_items)

    # Path to your HTML template.
    template_path = 'trip/invoice/invoice-template.html'

    # Load the HTML template using Django's get_template method.
    template = get_template(template_path)
    context = {
        'company':company,
        'invoice':invoice,
        'invoice_items':invoice_items
    }  # You can pass context data here if needed

    # Render the template with the context data.
    html = template.render(context)

    '''
    # Create a response object with PDF content type.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_id}.pdf"'
    '''
    pdf_buffer = generate_invoice_pdf(invoice, invoice_items)
    # Prepare the response for file download
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoice.invoice_id}.pdf"'
    
    return response
    '''
    # Create a PDF object using xhtml2pdf's pisa.CreatePDF.
    #pdf = pisa.CreatePDF(html, dest=response)
    

    # Check if PDF generation was successful.
    if not pdf.err:
        return response

    # If PDF generation failed, return an error message.
    return HttpResponse('PDF generation failed: %s' % pdf.err)
    '''

#---------------------------------- Estimate/Quotations views------------------------------------------

# add estimate
@login_required(login_url='login')
@permission_required('trip.add_estimate')
def add_estimate(request):
    company = get_user_company(request) 
    
    #instantiate the two kwargs to be able to access them on the forms.py
    stop_points = StopPoint.objects.filter(company=company)
    border_points = BorderStop.objects.filter(company=company)
    form = EstimateForm(request.POST, company=company)  
    customer_form = CustomerForm(request.POST)
    item_form = EstimateItemForm(request.POST, company=company)   

    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        customer = Customer.objects.get(company=company, id=customer_id)

        #create instance of a invoice
        estimate = Estimate.objects.create(
            company=company,
            customer = customer,
            valid_till = request.POST.get('valid_till'),
            sub_total = request.POST.get('sub_total'),
            discount = request.POST.get('discount'),
            tax = request.POST.get('tax'),
            total = request.POST.get('total'),
            note = request.POST.get('note'),
        )

        
        # get the items added original and added/cloned
        quotation_items_json = request.POST.get('quotation_items')
        quotation_items = json.loads(quotation_items_json)

        for key, item_data in quotation_items.items():
            route_id = item_data['route']
            route = get_object_or_404(Route, id=route_id)
            estimate_item = EstimateItem.objects.create(
                company=estimate.company,
                estimate=estimate,
                item_type=item_data['item_type'],
                route=route,
                trucks=int(item_data['trucks']),
                rate=int(item_data['rate']),
                amount=float(item_data['amount']),
                description = route.description
            )

            

        messages.success(request, f'Estimate was added successfully.')
        return redirect('view_estimate', estimate.id)

    context= {
        'form':form,
        'customer_form':customer_form,
        'item_form':item_form,
        'stop_points':stop_points,
        'border_points':border_points

    }
    return render(request, 'trip/estimate/add-estimate.html', context)
#--ends

# update estimate
@login_required(login_url='login')
@permission_required('trip.change_estimate')
def update_estimate(request, pk):
    company = get_user_company(request) #get request user company
    estimate = get_object_or_404(Estimate, id=pk)
    estimate_items = EstimateItem.objects.filter(estimate=estimate)
    if request.method == 'POST':
        # block updates on accepted quotes
        if estimate.status != 'Accepted':

            customer_id = request.POST.get('customer')
            customer = Customer.objects.get(company=company, id=customer_id)

            #update instance 
            estimate.company = company
            estimate.customer = customer
            estimate.valid_till = request.POST.get('valid_till')
            estimate.sub_total = request.POST.get('sub_total')
            estimate.discount = request.POST.get('discount')
            estimate.tax = request.POST.get('tax')
            estimate.total = request.POST.get('total')
            estimate.note = request.POST.get('note')
            estimate.status = request.POST.get('status')
            estimate.save()
            
            messages.success(request, f'Estimate details updated successfully.')
            return redirect('view_estimate', estimate.id)
        else:
            messages.error(request, f'Accepted quotations can not be edited!')
            return redirect('view_estimate', estimate.id)
    else:
        # prepopulate the form with existing data
        form_data = {
            'customer': estimate.customer,
            'valid_till': estimate.valid_till,
            'sub_total': estimate.sub_total,
            'tax': estimate.tax,
            'total': estimate.total,
            'note': estimate.note, 
            'status':estimate.status,
                    
        }

        form = EstimateForm(initial=form_data, company=company )
        context = {
            'estimate':estimate,
            'form':form,
            'estimate_items':estimate_items  
        }
        return render(request,'trip/estimate/update-estimate.html', context)
#--ends

#estimate list
@login_required(login_url='login')
@permission_required('trip.view_estimate')
def list_estimates(request):
    estimates = Estimate.objects.filter(company=get_user_company(request))
    number_of_estimates = estimates.count()
    context = {
        'estimates':estimates,
        'number_of_estimates':number_of_estimates
    }
    return render(request, 'trip/estimate/estimates-list.html', context)
#--ends

#view estimate
@login_required(login_url='login')
@permission_required('trip.view_estimate')
def view_estimate(request, pk):
    estimate = get_object_or_404(Estimate, id=pk) 
    estimate_items = EstimateItem.objects.filter(estimate=estimate)

    # check if invoice associated with the estimate exists
    #it will only exist is the estimate has been accepted.
    try:
        invoice = Invoice.objects.get(estimate=estimate)
    except:
        invoice = None

    context={
        'estimate':estimate,
        'estimate_items':estimate_items,
        'company':get_user_company(request), 
        'invoice':invoice,
        }
    return render(request, 'trip/estimate/view-estimate.html', context)
#--ends

# remove estimate
@login_required(login_url='login')
@permission_required('trip.delete_estimate')
def remove_estimate(request, pk):
    if request.method == 'POST':
        estimate = Estimate.objects.get(id=pk, company=get_user_company(request))
        estimate.delete()
        messages.success(request, f'Estimate of id : {estimate.estimate_id} removed')
        return redirect('list_estimates')
#--ends

#send estimate to client via email
@login_required(login_url='login')
@permission_required('trip.view_estimate') 
def send_estimate(request, pk):
    company = get_user_company(request)
    estimate = get_object_or_404(Estimate, id=pk)
    preference = get_object_or_404(Preference, company=company)

    estimate_url = request.build_absolute_uri(reverse('view_estimate', args=[estimate.id]))
    #having this context because delay() need model serialzation
    context = {
        'customer_name': estimate.customer.name,
        'estimate_url': estimate_url,
        'company_name': company.name
    }

    send_email_task.delay(
        context=context, 
        template_path='trip/estimate/load-estimate.html', 
        from_name='Loginit Truckman', #revert back to this preference.email_from_name
        from_email=settings.EMAIL_HOST_USER, #revert back to this preference.from_email
        subject='Quotation', 
        recipient_email=estimate.customer.email, 
        replyto_email=company.email
    )

    messages.success(request, 'Estimate sent to customer.')
    return redirect('view_estimate', estimate.id)

#accept estimate
def accept_estimate(request, pk):
    estimate = get_object_or_404(Estimate, id=pk)
    estimate.status = 'Accepted'
    estimate.save()

    #create a trip instance, to be used later.
    trip = Trip.objects.create(
        company = estimate.company,
        estimate = estimate
    )

    estimate_items = EstimateItem.objects.filter(estimate=estimate)
    
    # Calculate the total number of trucks for all estimate items
    total_trucks = estimate_items.aggregate(total_trucks=Sum('trucks'))['total_trucks'] or 0
    
    # instatiate load instances based on the number of trucks 
    while int(total_trucks) > 0:
        Load.objects.create(
            company = estimate.company,
            estimate = estimate
        )
        total_trucks -= 1

    # send whatsapp notifications to indicate creation of Trip and loads. 
    user = request.user
    whatsapp_setting = get_object_or_404(WhatsappSetting, company=user.company )
    trip_url = request.build_absolute_uri(reverse('view_trip', args=[trip.id]))
    message = f'Hello {user.first_name} {user.last_name}, a trip {trip.trip_id} has been created. Click the link below to view and edit associated loads {trip_url}'
    send_whatsapp_text_task.delay(
        instance_id=whatsapp_setting.instance_id, 
        access_token=whatsapp_setting.access_token, 
        phone_no=user.phone, 
        message=message
    )
    #send email to admin notify them about 
    #the acceptance and assign trucks to the load link.

    estimate_url = request.build_absolute_uri(reverse('view_estimate', args=[pk]))
    estimate_id = estimate.estimate_id
    context = {
        'estimate':estimate_id,
        'estimate_url' : estimate_url,
    }
    
    send_email_task.delay(
        context=context, 
        template_path='trip/estimate/estimate-accepted.html', 
        from_name='Loginit Truckman', 
        from_email=settings.EMAIL_HOST_USER, 
        subject='Estimate Accepted', 
        recipient_email=estimate.company.email, 
        replyto_email=settings.EMAIL_HOST_USER
    )
    messages.success(request, 'Quotation accepted successfully.')
    return redirect('view_estimate_negotiate_mode', estimate.id )

#decline estimate
def decline_estimate(request, pk):
    estimate = Estimate.objects.get(id=pk)
    estimate.status = 'Declined'
    estimate.save()

    #send email to admin notify them about the rejection
    estimate_url = request.build_absolute_uri(reverse('view_estimate', args=[pk]))
    context = {
        'estimate':estimate.id, 
        'estimate_url' : estimate_url
    }
    send_email_task.delay(
        context=context, 
        template_path='trip/estimate/estimate-declined.html', 
        from_name='Loginit Truckman', 
        from_email=settings.EMAIL_HOST_USER, 
        subject='Estimate Declined', 
        recipient_email=estimate.company.email, 
        replyto_email=settings.EMAIL_HOST_USER
    )
    messages.info(request, 'Quotation declined successfully.')
    return redirect('view_estimate_negotiate_mode', estimate.id )

#share estimate uri with customer
def view_estimate_negotiate_mode(request, pk):
    estimate = Estimate.objects.get(id=pk)
    estimate_items = EstimateItem.objects.filter(estimate=estimate)
    company = estimate.company
    context={
        'estimate':estimate,
        'company':company,
        'estimate_items':estimate_items
        }
    return render(request, 'trip/estimate/view-estimate-nego-mode.html', context)
#--ends

def negotiate_estimate(request):
    if request.method == 'POST':
        pass
        #get response from post

#This view generates an invoice of an associated estimate
def generate_associated_invoice(request, pk):
    estimate = Estimate.objects.get(id=pk)
    invoice = generate_invoice(estimate)
    messages.success(request, 'Invoice has been generated sucessfully.')
    return render('view_invoice', invoice.id)
    
#---------------------------------- Reminder views------------------------------------------

# add reminder
@login_required(login_url='login')
@permission_required('trip.add_reminder')
def add_reminder(request):
    company = get_user_company(request) 
    #instantiate the two kwargs to be able to access them on the forms.py
    form = ReminderForm(request.POST, company=company) 
    if request.method == 'POST':

        vehicle_id = request.POST.get('vehicle')
        vehicle = Vehicle.objects.get(company=company, id=vehicle_id)

        current_date = timezone.now().date()
        next_date_str = request.POST.get('next_date')

        # Convert the next_date string to a datetime.date object
        next_date = datetime.strptime(next_date_str, '%Y-%m-%d').date()

        if next_date < current_date:
            status = 'Overdue'
        else:
            status = 'Active'

        #create instance of a reminder
        reminder = Reminder.objects.create(
            company=company,
            vehicle = vehicle,
            name = request.POST.get('name'),
            frequency = request.POST.get('frequency'),
            status = status,
            last_date = request.POST.get('last_date'),
            next_date = request.POST.get('next_date'),
        )

        messages.success(request, f'Reminder was set.')
        return redirect('list_reminders')

    context= {
        'form':form,
    }
    return render(request, 'trip/reminder/reminders-list.html', context)
#--ends

#reminder list
@login_required(login_url='login')
@permission_required('trip.view_reminder')
def list_reminders(request):
    company = get_user_company(request)
    reminders = Reminder.objects.filter(company=company)
    number_of_reminders = reminders.count()
    reminder_form = ReminderForm(request.POST, company=company) 
    context = {
        'reminders':reminders,
        'number_of_reminders':number_of_reminders,
        'reminder_form':reminder_form
    }
    return render(request, 'trip/reminder/reminders-list.html', context)
#--ends

# remove reminder
@login_required(login_url='login')
@permission_required('trip.delete_reminder')
def remove_reminder(request, pk):
    #if request.method == 'POST':
    reminder = Reminder.objects.get(id=pk, company=get_user_company(request))
    reminder.delete()
    messages.success(request, 'Reminder removed')
    return redirect('list_reminders')
#--ends

#---------------------------------- Reminder views------------------------------------------



#---------------------------------- front end endpoint views -------------------------------------------------------------------------


# view to get trip info when adding an invoice
@login_required(login_url='login')
def get_trip_info(request, trip_id):
    company = get_user_company(request)
    try:
        trip = Trip.objects.get(id=trip_id, company=company)  # Fetch the Trip object based on the trip_id
        trip_info = {
            'vehicle': trip.vehicle.plate_number,
            'customer': trip.load.customer.name,
        }
        return JsonResponse(trip_info)
    except Trip.DoesNotExist:
        return JsonResponse({'error': 'Trip not found'}, status=404)
    
#--------------------------- vehicle info ____________________________________________

# view to get load info when adding a trip
@login_required(login_url='login')
def get_vehicle_info(request, vehicle_id):
    company = get_user_company(request)
    try:
        vehicle = Vehicle.objects.get(id=vehicle_id, company=company)
        try:
            driver = Driver.objects.get(assigned_vehicle=vehicle, company=company)
        except Driver.DoesNotExist:
            driver = None

        vehicle_info = {
            'trailer': vehicle.trailer_number,
            'driver': driver.first_name + ' ' + driver.last_name ,
        }
        return JsonResponse(vehicle_info)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)

#--------------------------- load info ____________________________________________

#view to get load info when adding an trip
@login_required(login_url='login')
def get_load_info(request, load_id):
    company = get_user_company(request)
    try:
        load = Load.objects.get(id=load_id, company=company)
        load_info = {
            'customer': load.estimate.customer.name,
            'commodity': load.commodity,
        }
        return JsonResponse(load_info)
    except Load.DoesNotExist:
        return JsonResponse({'error': 'Load not found'}, status=404)
    
#--------------------------- estimate info ____________________________________________

#view to get estimate info when adding an load
@login_required(login_url='login')
def get_estimate_info(request, estimate_id):
    company = get_user_company(request)
    try:
        estimate = Estimate.objects.get(id=estimate_id, company=company)
        estimate_info = {
            'amount': estimate.total,
            'item': estimate.item,
            'quantity': estimate.quantity,
            'customer': estimate.customer.name,
        }
        return JsonResponse(estimate_info)
    except Estimate.DoesNotExist:
        return JsonResponse({'error': 'Estimate not found'}, status=404)



#--------------------------- daily register views _________________________________________________

def add_register_entry(request, pk):
    company = get_user_company(request)
    form = DailyRegisterForm(request.POST, company=company)
    trip = Trip.objects.get(id=pk)

    # Get all vehicles assigned to loads
    vehicles = get_trip_vehicles(trip)
    
    #get drivers
    drivers = Driver.objects.filter(assigned_vehicle__in=vehicles)

    if request.method == 'POST':
        general_coordinates = format_coordinates(request.POST.get('general_coordinates'))

        location_data = reverse_geocode(general_coordinates) 
        user_timezone = location_data.get('timezone')

        user_tz = pytz.timezone(user_timezone)
        current_datetime = timezone.now()
        current_time = current_datetime.astimezone(user_tz).time()

        # Determine the datetime field based on the current time
        if 5 <= current_time.hour < 11:
            datetime_field = 'morning'
        elif 12 <= current_time.hour < 16:
            datetime_field = 'midday' 
        elif 17 <= current_time.hour < 21:
            datetime_field = 'evening'
        else:
            context = {
                'trip': trip,
                'form': form
            }
            messages.error(request, 'Wrong entry time!')
            return render(request, 'trip/daily-register/add-daily-register.html', context)

        for driver, vehicle in zip(drivers, vehicles):
            coordinates = request.POST.get(f'{datetime_field}_location')
            
            create_daily_register(request, company, trip, vehicle, driver, coordinates, user_timezone, datetime_field)

        messages.success(request, 'Entry recorded successfully')
        return render(request,'trip/daily-register/success.html')

    context = {
       'trip': trip,
       'form': form
    }
    return render(request, 'trip/daily-register/add-daily-register.html', context)

#---ends

#view to render daily trip register report
@login_required(login_url='login')
def trip_daily_register_report(request):
    company = get_user_company(request)
    form = DailyRegisterForm(company=company)
    
    if request.method == 'POST':
        #get the trip id 
        trip_id = request.POST.get('trip')
        trip = Trip.objects.get(id=trip_id)

        # Calculate the number of days elapsed since the trip started
        start_date = trip.start_time.date()
        current_date = datetime.now().date()
        elapsed_days = (current_date - start_date).days + 1  # +1 to include the current day

        # Create a list of day numbers
        day_numbers = list(range(1, elapsed_days + 1))

        context = {
            'trip': trip,
            'day_numbers': day_numbers, 
        }
        return render(request, 'trip/reports/daily-register-report.html', context )
    
    context = {
        'form':form
    }
    return render(request, 'trip/reports/daily-register-select-trip.html', context)
#ends

#View to download daily report for staff
def download_daily_report(request):
    trip_id = request.POST.get('selected_trip_id')
    trip = get_object_or_404(Trip, id=trip_id)
    
    # Create the workbook
    workbook = create_workbook(request, trip)
    
    # Save the workbook to a BytesIO buffer
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    
    # Prepare the response for file download
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{trip.trip_id} Daily Report.xlsx"'
    
    return response

#download day report for clients
def download_day_report(request, trip_id):#for client
    trip = get_object_or_404(Trip, id=trip_id)
    
    # Create the workbook
    workbook = create_workbook(request, trip)
    
    # Save the workbook to a BytesIO buffer
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    
    # Prepare the response for file download
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{trip.trip_id} Daily Report.xlsx"'
    
    return response
#--ends

#--------------------------- Trip incident views _________________________________________________

#-- add trip incident
def add_trip_incident(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == 'POST':
        #get vehicle
        vehicle_id = request.POST.get('vehicle')
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        #create the trip incident object
        TripIncident.objects.create(
            company = get_user_company(request),
            trip = trip,
            description = request.POST.get('description'),
            vehicle = vehicle, 
            added_by = request.user
        )
        messages.success(request, 'Trip incident added successfuly.')
        return redirect('view_trip', trip.id)
    return redirect('view_trip', trip.id)
#-- ends

#-- delete trip incident view 
def delete_trip_incident(request, trip_id, incident_id):
    trip = get_object_or_404(Trip, id=trip_id)
    incident = get_object_or_404(TripIncident, id=incident_id)
    incident.delete()
    messages.success(request, 'Incident deleted!')
    return redirect('view_trip', trip.id)
#ends
