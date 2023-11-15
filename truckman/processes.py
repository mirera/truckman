from django.utils import timezone
from datetime import timedelta
from trip.models import Estimate, Invoice, LoadingList, LoadingListItem, DailyRegister, Load, DailyRegister, Driver, Trip, EstimateItem, InvoiceItem
from django.shortcuts import get_object_or_404
from truckman.utils import get_location_data
from django.db.models import F



#helper function to calculate due date 
# of an invoice based on the customer

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
        loads = Load.objects.filter(estimate=estimate)
        
        # Get all vehicles assigned to loads
        vehicles = []
        for load in loads:
            if load.assigned_truck:
                vehicles.append(load.assigned_truck)

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