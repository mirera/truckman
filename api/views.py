from django.http import JsonResponse
from datetime import timedelta, datetime
from django.shortcuts import render
from truckman.processes import get_driver_day_entries
from trip.models import Driver, Trip, Load
from django.forms.models import model_to_dict
import pytz



def get_entries_for_day(request, trip_id, day_number):
    # Create a list to accumulate results for each driver
    driver_results = []
    trip = Trip.objects.get(id=trip_id)

    loads = Load.objects.filter(estimate=trip.estimate)
    vehicles = []

    for load in loads:
        if load.assigned_truck:
            vehicle = load.assigned_truck
            vehicles.append(vehicle)

    drivers = Driver.objects.filter(assigned_vehicle__in=vehicles)

    for driver in drivers:
        # Calculate the target date
        #target_date = trip.date_added + timedelta(days=int(day_number) - 1)
        target_date = trip.start_time.date()
        entries = get_driver_day_entries(trip, driver, target_date)
        morning_entry = None
        midday_entry = None
        evening_entry = None
        sub_time = None
        mid_sub_time = None
        evening_sub_time = None
        
        

        # Split the entries into morning, midday, and evening based on submission times
        for entry in entries:
            #get the user timezone from the request session
            user_timezone = request.session.get('user_timezone', 'UTC')

            # Create a timezone object for the user's timezone
            user_tz = pytz.timezone(user_timezone)

            # Convert UTC time to the user's local time
            submission_time = entry.submission_time.astimezone(user_tz) 
            

            if 5 <= submission_time.hour < 11:
                # Convert sub_time UTC time to the user's local time format to HMS
                sub_time = entry.submission_time.astimezone(user_tz).strftime('%H:%M:%S')
                morning_entry = model_to_dict(entry)
            elif 12 <= submission_time.hour < 16:
                mid_sub_time = entry.submission_time.astimezone(user_tz).strftime('%H:%M:%S')
                midday_entry = model_to_dict(entry)
            elif 17 <= submission_time.hour < 21:
                evening_sub_time = entry.submission_time.astimezone(user_tz).strftime('%H:%M:%S')
                evening_entry = model_to_dict(entry)
             


        distance_covered = (evening_entry['evening_odometer_reading'] - morning_entry['morning_odometer_reading']) if evening_entry and morning_entry else None
        sleeping_location = evening_entry['evening_location'] if evening_entry else None
        trip_status = evening_entry['vehicle_status'] if evening_entry else None


        # Accumulate the results for this driver
        driver_results.append({
            'driver_name': f'{driver.first_name} {driver.last_name}',
            'morning_entry': morning_entry,
            'midday_entry': midday_entry,
            'evening_entry': evening_entry,
            'distance_covered': distance_covered,
            'sleeping_location': sleeping_location,
            'trip_status': trip_status,
            'sub_time':sub_time, 
            'mid_sub_time':mid_sub_time,
            'evening_sub_time':evening_sub_time
        })

    # Return the results for all drivers in a JSON response
    return JsonResponse({'drivers': driver_results})
