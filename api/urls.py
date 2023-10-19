from django.urls import path
from . import views
 

urlpatterns = [

    #get register entries for day
    path('get_entries_for_day/<str:trip_id>/<str:day_number>', views.get_entries_for_day, name='get_entries_for_day'),
]