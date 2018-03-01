from django.contrib import admin
from .models import Vehicle, VehicleCondition, VehicleInOutInfo, Route, Trip


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('number', 'model', 'joining_date', 'capacity', 'category')
    list_filter = ('model', 'capacity', 'category')

@admin.register(VehicleCondition)
class VehicleConditionAdmin(admin.ModelAdmin):
    list_display = ('vehicle','is_ok','date')
    list_filter = ('date', 'is_ok', 'vehicle')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'branch_manager')
    list_filter = ('category', 'name')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'origin', 'via_list', 'destination', 'driver', 'date')
    list_filter = ('vehicle', 'date', 'origin', 'destination', 'driver')


@admin.register(VehicleInOutInfo)
class VehicleInOutInfoAdmin(admin.ModelAdmin):
    list_display = ('trip', 'route', 'date', 'is_arrived', 'is_leaved')
    list_filter = ('route', 'date', 'is_arrived', 'is_leaved')
