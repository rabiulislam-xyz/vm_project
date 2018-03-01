from django.urls import path, re_path

from .views import (index,
                    vehicle_condition,
                    set_vehicle_condition,
                    available_vehicles,
                    set_trip,
                    set_vehicle_in_out_info)



urlpatterns = [
    path('', index, name='index'),

    # vehicle conditions
    re_path(r'^vehicle-condition/$', vehicle_condition, name='vehicle_condition'),

    re_path(r'^set-condition/$', set_vehicle_condition, name='set_vehicle_condition'),

    # vehicle operations
    re_path(r'^available-vehicles/$', available_vehicles, name='available_vehicles'),
    re_path(r'^set-trip/$', set_trip, name='set_trip'),

    # vehicle in out information
    re_path(r'^vehicle-info/$', set_vehicle_in_out_info, name='vehicle_info'),
]