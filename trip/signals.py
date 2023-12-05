from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.utils import timezone
from django.dispatch import receiver
from .models import Driver, Load
from truckman.processes import update_trip_status

#setting the passport photo default to 'default.png'
@receiver(pre_save, sender=Driver)
def set_default_passport_photo(sender, instance, **kwargs):
    if not instance.driver_photo:
        instance.driver_photo = 'default.png'
# --ends

#update trip status when load is saved
@receiver(post_save, sender=Load)
def update_trip_status_on_load_save(sender, instance, **kwargs):
    # Call the function to update trip status when a Load is saved
    update_trip_status(instance)

#update load loaded date when load is saved
@receiver(post_save, sender=Load)
def update_loading_offloading_dates(sender, instance, created, **kwargs):
    if not created:  # Ignore on initial creation
        before_status = instance.status  # Status before saving
        print(f'before_status:{before_status}')
        instance.refresh_from_db()  # Refresh instance from the database
        after_status = instance.status  # Status after saving
        print(f'after_status:{after_status}')
        if before_status == 'Not Loaded' and after_status == 'On Transit':
            instance.date_loaded = timezone.now().date()
            instance.save()
            print(f'instance.date_loaded:{instance.date_loaded}')
        elif before_status == 'On Transit' and after_status == 'Delivered':
            instance.date_offloaded = timezone.now().date()
            instance.save()
            print(f'instance.date_offloaded:{instance.date_offloaded}')







'''
function to generate daily register excel document
'''
'''
def generate_excel_daily_trip_report(request, trip):
    loads = Load.objects.filter(estimate=trip.estimate) # Get trip loads 

    # Create an Excel writer object
    excel_writer = pd.ExcelWriter(f'Trip_{trip.trip_id}_Daily_Report.xlsx', engine='openpyxl')
    
    # Loop through each load and create a sheet for each load
    for load in loads:
        load_sheet = create_load_excel_sheet(load) #excel sheet for each load

        load_entries = get_load_daily_entries(load)
        morning_entry, midday_entry, evening_entry = None, None, None
        morning_sub_time, mid_sub_time, evening_sub_time = None, None, None
        morning_location, midday_location, evening_location = None, None, None
        morning_odemeter_reading, midday_odemeter_reading, evening_odemeter_reading = None, None, None

        # Split the entries into morning, midday, and evening based on submission times
        for entry in load_entries:
            print(f'entry insie second loop:{entry}')
            #get the user timezone from the request session
            user_timezone = request.session.get('user_timezone', 'UTC')

            # Create a timezone object for the user's timezone
            user_tz = pytz.timezone(user_timezone)

            # Convert UTC time to the user's local time
            submission_time = entry.submission_time.astimezone(user_tz) 
            
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

            # Create a DataFrame for the load data
            load_data = {
                '{{ load.assigned_truck.plate_number }}': {}
            }

            days_elapsed = load_days_elapsed(entry)
            for day in range(1, days_elapsed + 1):
                
                day_data = {
                    'Trip Day': [f'Day {day}'],  # included entry date
                    '#': ['Sub-Time', 'Location', 'Odemeter'],
                    'Morning': [morning_sub_time or 'N/A', 
                                getattr(morning_entry, 'morning_location', '') or 'N/A', 
                                getattr(morning_entry, 'morning_odemeter_reading', '') or 'N/A'],
                    'Midday': [mid_sub_time or 'N/A', 
                            getattr(midday_entry, 'midday_location', '') or 'N/A', 
                            getattr(midday_entry, 'midday_odemeter_reading', '') or 'N/A'],
                    'Evening': [evening_sub_time or 'N/A', 
                                getattr(evening_entry, 'evening_location', '') or 'N/A', 
                                getattr(evening_entry, 'evening_odemeter_reading', '') or 'N/A']
                }

                load_data['{{ load.assigned_truck.plate_number }}'][f'Day {day}'] = day_data
        
        
        load_df = pd.DataFrame(load_data)

        # Write the DataFrame to a new sheet in the Excel file
        if load.assigned_truck:
            sheet_name = load.assigned_truck.plate_number
            load_df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

    # Save the Excel file
    excel_writer.save()
'''