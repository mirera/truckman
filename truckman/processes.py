from django.utils import timezone
from datetime import timedelta
from trip.models import Estimate, Invoice, LoadingList, LoadingListItem, DailyRegister, Load, DailyRegister, Driver
from django.shortcuts import get_object_or_404
from truckman.utils import get_location_data

'''
This function is called when a trip has been started
by admin/office. You can also use it to re-generate an 
invoice for a given estimate.
'''
def generate_invoice(estimate): 
        due_date = timezone.now().date() + timedelta(days=30)
        #create instance of a invoice
        invoice = Invoice.objects.create(
            company=estimate.company,
            estimate = estimate,
            route = estimate.route,
            item = estimate.item,
            trucks = estimate.trucks,
            rate = estimate.rate,
            description = estimate.description,
            sub_total = estimate.sub_total,
            discount = estimate.discount,
            tax = estimate.tax,
            total = estimate.total,
            balance = estimate.total,
            invoice_date = timezone.now().date(),
            due_date = due_date,
            note = estimate.company.invoice_payment_details,
        )
        return invoice  #should return a path to the pdf of the invoice
#--ends

'''
This function is called when an estimate has been accepted
by the customer. It creates a loading list 
'''
def generate_loading_list(estimate):
        estimate = get_object_or_404(Estimate, id=estimate.id)
        load = get_object_or_404(Load, estimate=estimate)
        #check if the load is assigned vehicle
        vehicles = load.assigned_trucks.all()

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




