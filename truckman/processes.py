from django.utils import timezone
from datetime import timedelta
from trip.models import Estimate, Invoice, LoadingList, LoadingListItem, DailyRegister, Load, DailyRegister, Driver, Trip, EstimateItem, InvoiceItem
from django.shortcuts import get_object_or_404
from truckman.utils import get_location_data
from django.db.models import F
import pandas as pd
from openpyxl import Workbook
import pytz


'''
Function to get a trip vehicle(s)
'''
def get_trip_vehicles(trip):
    loads = Load.objects.filter(estimate=trip.estimate)

    # Get all vehicles assigned to loads
    vehicles = []
    for load in loads:
        if load.assigned_truck:
            vehicles.append(load.assigned_truck) 
    return vehicles

'''
#helper function to calculate due date 
of an invoice based on the customer
'''
def get_invoice_due_date(customer, trip):
    payment_terms = {
        '2 Days': 2,
        '7 Days': 7,
        '10 Days': 10,
        '15 Days': 15,
        '30 Days': 30,
        'Cash on Delivery': None,  # No need to calculate a due date for Cash on Delivery
    }

    payment_term = customer.payment_term
    if payment_term in payment_terms:
        days = payment_terms[payment_term]
        if days is not None:
            due_date = trip.start_time.date() + timedelta(days=days)
        else:
            due_date = trip.end_time.date()  # For 'Cash on Delivery'
    else:
        # Handle cases where payment term is not recognized
        due_date = None  

    return due_date

'''
This function is called when a estimate has been acceptes
by client. You can also use it to re-generate an 
invoice for a given estimate.
'''
def generate_invoice(estimate): 
        trip = Trip.objects.get(estimate=estimate)
        due_date = get_invoice_due_date(estimate.customer, trip)

        #get estimate items
        estimate_items = EstimateItem.objects.filter(estimate=estimate)

        #create invoice instance from estimate data
        invoice = Invoice.objects.create(
            company=estimate.company,
            estimate = estimate,
            sub_total = estimate.sub_total,
            discount = estimate.discount,
            tax = estimate.tax,
            total = estimate.total,
            balance = estimate.total,
            invoice_date = timezone.now().date(),
            due_date = due_date,
            note = estimate.company.invoice_payment_details,
        )

        #create invoice items from estimate items
        invoice_items = []

        for item in estimate_items:
            invoice_item = InvoiceItem.objects.create(
                    company=estimate.company,
                    invoice=invoice,
                    route = item.route,
                    item_type = item.item_type,
                    trucks = item.trucks,
                    rate = item.rate,
                    amount = item.amount,
                    description = item.description,
                )
            invoice_items.append(invoice_item)
    
        return invoice       
#--ends

'''
This function is called when a loas has been assigned a truck
It creates a loading list 
'''
def generate_loading_list(estimate):
        # Get all vehicles assigned to loads
        trip = Trip.objects.filter(estimate=estimate)
        vehicles = get_trip_vehicles(trip)
        
        #create instance of a loading list
        loading_list = LoadingList.objects.create(
            company=estimate.company,
            estimate = estimate,    
        )

        # Create an instance of a loading list item for each vehicle
        loading_list_items = []
        for vehicle in vehicles:
            driver = get_object_or_404(Driver, assigned_vehicle=vehicle)
            
            loading_list_item = LoadingListItem.objects.create(
                company=estimate.company,
                loading_list=loading_list,
                vehicle=vehicle,
                driver=driver,
            )
            loading_list_items.append(loading_list_item)

        return loading_list
#--ends     

'''
funtion to create a daily register instant
'''
def create_daily_register(request, company, trip, vehicle, driver, coordinates, user_timezone, datetime_field):
    # Get user sublocality, city, and country
    nearest_town, country = get_location_data(coordinates)

    # Create a DailyRegister object
    return DailyRegister.objects.create(
        company=company,
        trip=trip,
        vehicle=vehicle,
        driver=driver,
        **{
            f'{datetime_field}_location': nearest_town,
            'country': country,
            f'{datetime_field}_odemeter_reading': request.POST.get(f'{datetime_field}_odemeter_reading'),
            'vehicle_status': request.POST.get('vehicle_status'),
            'reason_parked': request.POST.get('reason_parked'),
        }
    )

#--end

'''
Function to get register entries of a day
i.e morning, midday and evening
'''
def get_driver_day_entries(trip, driver, target_date):
    day_entries = DailyRegister.objects.filter(
        driver=driver,
        trip=trip,
        submission_time__date=target_date
    )
    return day_entries
#--ends

'''
Function to get register daily entries
all entries of a load/vehicle on a trip
'''
def get_load_daily_entries(load):
    trip = Trip.objects.get(estimate=load.estimate) 
    load_entries = DailyRegister.objects.filter(
        trip=trip,
        vehicle=load.assigned_truck
    )
    return load_entries
#--ends

'''
Get days elapsed since the load status changed to load.date_loaded
'''
def load_days_elapsed(day_entry):
    days_elapsed = 3 # to be changed
    return days_elapsed
#--ends

'''
Split the entries into morning, midday, and evening based on submission times
'''
def split_day_entry(entry, request):
    user_timezone = request.session.get('user_timezone', 'UTC') #get user timezone 
    user_tz = pytz.timezone(user_timezone)# Create a timezone object
    submission_time = entry.submission_time.astimezone(user_tz) # Convert UTC time to the user's local time
    morning_entry, midday_entry, evening_entry = None, None, None
    morning_sub_time, mid_sub_time, evening_sub_time = None, None, None
    
    if 5 <= submission_time.hour < 11:
        # Convert sub_time UTC time to the user's local time format to HMS
        morning_sub_time = entry.submission_time.astimezone(user_tz).strftime('%H:%M:%S')
        morning_entry = entry
    elif 12 <= submission_time.hour < 16:
        mid_sub_time = entry.submission_time.astimezone(user_tz).strftime('%H:%M:%S')
        midday_entry = entry
    elif 17 <= submission_time.hour < 21:
        evening_sub_time = entry.submission_time.astimezone(user_tz).strftime('%H:%M:%S')
        evening_entry = entry

    return morning_entry, midday_entry, evening_entry, morning_sub_time, mid_sub_time, evening_sub_time
#--ends

'''
Number of days since a load.date_loaded 
and date_offloaded
'''
def load_trip_days(load):
    load_days = load.date_offloaded - load.date_loaded 
    return load_days
#--ends


'''
Function to generate daily register Excel workbook 
'''
def generate_excel_daily_trip_report(trip, request):
    loads = Load.objects.filter(estimate=trip.estimate) # Get trip loads 
    # Create an Excel writer object
    excel_writer = pd.ExcelWriter(f'Trip_{trip.trip_id}_Daily_Report.xlsx', engine='openpyxl')
    for load in loads: # Loop through each load 
        load_excel_sheet = create_load_excel_sheet(load, excel_writer, request) #create a sheet for each load 
        print(f'load_excel_sheet:{load_excel_sheet}')
    trip_excel_workbook = excel_writer.save() # Save the Excel file
    return trip_excel_workbook  
#--ends

def create_sheetdata(request, worksheet, vehicle, day, n, m, p, q):
    load = get_object_or_404(Load, assigned_truck=vehicle)
    entries = get_load_daily_entries(load) #get load's all entries

    for entry in entries:
        #split a day's entry into morning, mid and evening
        morning_entry, midday_entry, evening_entry, morning_sub_time, mid_sub_time, evening_sub_time = split_day_entry(entry, request)

        #Create rows/columns and insert sheet data
        worksheet['A1'] = f'{vehicle.plate_number} Report'
        worksheet[f'A{n}'] = f'Trip Day {day} | {entry.submission_time.date()}' #
        worksheet[f'B{n}'] = "#"
        worksheet[f'C{n}'] = "Morning"
        worksheet[f'D{n}'] = "Midday"
        worksheet[f'E{n}'] = "Evening"
        worksheet[f'B{m}'] = "Submission Time"
        worksheet[f'B{p}'] = "Location"
        worksheet[f'B{q}'] = "Odemeter"
        worksheet[f'C{m}'] = 'morning_sub_time' #morning entry subtime
        worksheet[f'C{p}'] = 'morning_entry.morning_location '#morning entry location
        worksheet[f'C{q}'] = 'morning_entry.morning_odemeter_reading' #morning odemeter reading
        worksheet[f'D{m}'] = mid_sub_time#midday entry subtime
        worksheet[f'D{p}'] = midday_entry.midday_location #midday entry location
        worksheet[f'D{q}'] = midday_entry.midday_odemeter_reading #midday odemeter reading
        worksheet[f'E{m}'] = 'evening_sub_time' #evening entry subtime
        worksheet[f'E{p}'] = 'evening_entry.evening_location' #evening entry location
        worksheet[f'E{q}'] = 'evening_entry.evening_odemeter_reading '#evening odemeter reading
 
#--ends 

def create_workbook(request, trip):
    '''
    Function to create a workbook
    '''
    workbook = Workbook()
    #create a worksheets for each vehicle on the trip
    for vehicle in get_trip_vehicles(trip):
        worksheet = workbook.create_sheet(title=f"{trip.trip_id} {vehicle.plate_number} Report")
        #worksheet content
        load = get_object_or_404(Load, assigned_truck=vehicle)
        days = load_trip_days(load)
        print(f'load_trip_days:{days}')
        days = [1,2,3] 
        
        n,m,p,q = 2,3,4,5 # these variables dynamically help write on excel vertically
        for day in days:
            create_sheetdata(request, worksheet, vehicle, day, n, m, p, q)
            n += 5
            m += 5
            p += 5
            q += 5

    # Save the file
    workbook.save(f'{trip.trip_id} Daily Report.xlsx') 
#--ends 

 
'''
Generate single day daily report for client sharing
'''
def generate_client_daily_report(trip, path_to_workbook):
    trip_workbook = create_workbook(path_to_workbook)#create an Excel workbook
    worksheet = create_worksheet(path_to_workbook, trip)#create worksheet
    create_sheetdata(path_to_workbook, trip) #write or load data into to the worksheet
    return trip_workbook #this should be a path to the workbook


'''
This updates trip status to dispatched or completed dep
depening on load status
'''
def update_trip_status(load):
    trip = Trip.objects.get(estimate=load.estimate)
    
    if trip:
        # Retrieve all loads associated with the trip
        associated_loads = Load.objects.filter(estimate=load.estimate)
        
        # Check if any load status is 'On Transit'
        if associated_loads.filter(status='On Transit').exists():
            trip.status = 'Dispatched'
            trip.start_time = timezone.now()
            trip.save()
        
        # Check if all loads' status are 'Delivered'
        if associated_loads.exclude(status='Delivered').exists():
            # Not all loads are delivered
            return
        
        # All loads are delivered
        trip.status = 'Completed'
        trip.end_time = timezone.now()
        trip.save()

        # Change all vehicle is_available to True
        vehicles = []
        for load in associated_loads:
            if load.assigned_truck:
                vehicles.append(load.assigned_truck)

        for vehicle in vehicles:
            vehicle.is_available = True
            vehicle.save()
#--ends


