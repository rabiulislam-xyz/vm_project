from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.timezone import now
from datetime import datetime

from accounts.models import User
from .models import Vehicle, VehicleInOutInfo, VehicleCondition, Trip, Route
from .forms import TripForm


@login_required
def index(request):
    total_vehicles = Vehicle.objects.all().count()
    total_routes = Route.objects.all().count()
    total_trips = Trip.objects.all().count()
    total_staffs = User.objects.all().count()

    total = {
        'vehicles': total_vehicles,
        'routes': total_routes,
        'trips': total_trips,
        'staffs': total_staffs
    }
    context = {'total':total}
    return render(request, 'fleet_management/index.html', context)


# views for vehicle manager
@login_required
def vehicle_condition(request):
    # date would be current date if no specific date
    # provided via get parameters
    d = request.GET.get('date')
    d = datetime.strptime(d, '%Y-%m-%d') if d else now().today()
    context = {'date': d.strftime('%Y-%m-%d')}

    # set new conditions for new date or update existing conditions
    conditions = VehicleCondition.objects.filter(date=d)
    if not conditions.exists():
        context['vehicle_conditions_not_added'] = True
    else:
        context['conditions'] = conditions

    return render(request, 'fleet_management/vehicle_conditions.html', context)


@login_required
@permission_required('fleet_management.add_vehiclecondition')
def set_vehicle_condition(request):
    # date would be current date if no specific date
    # provided via get parameters
    d = request.GET.get('date')
    d = datetime.strptime(d, '%Y-%m-%d') if d else now().today()
    context = {'date': d.strftime('%Y-%m-%d')}

    conditions = VehicleCondition.objects.filter(date=d)

    if request.method == 'POST':
        # set conditions for every vehicle for every date
        vehicles = Vehicle.objects.all()
        for v in vehicles:
            condition, created = VehicleCondition.objects.get_or_create(vehicle=v, date=d)
            # if condition is ok then reverse it, otherwise reverse it!
            condition.is_ok = True if request.POST.get(str(v.number)) else False
            condition.save()
        messages.success(request, 'Vehicle Conditions for {} has been Set Successfully'.format(d.strftime('%Y-%m-%d')))
        return redirect("{}?date={}".format(reverse(vehicle_condition), d.strftime('%Y-%m-%d')))
    else:
        if not conditions.exists():
            vehicles = Vehicle.objects.all()
            context['vehicles'] = vehicles
            context['vehicle_conditions_not_added'] = True
        else:
            context['conditions'] = conditions

    return render(request, 'fleet_management/vehicle_condition_form.html', context)


# views for operation manager
@login_required
def available_vehicles(request):
    # date would be current date if no specific date
    # provided via get parameters
    d = request.GET.get('date')
    d = datetime.strptime(d, '%Y-%m-%d') if d else now().today()
    context = {'date': d.strftime('%Y-%m-%d')}

    # only those vehicles will be in list of available vehicles
    # which are good conditions and not confirmed for any trip for
    # this date!
    trips = Trip.objects.filter(date=d).select_related('vehicle').all()
    context['trips'] = trips

    vehicles_condition = VehicleCondition.objects.filter(date=d).filter(is_ok=True).select_related('vehicles').all()
    trips_vehicles = [trip.vehicle for trip in trips]

    vehicles = vehicles_condition.exclude(vehicle__in=trips_vehicles)
    context['vehicles'] = vehicles

    return render(request, 'fleet_management/available_vehicles.html', context)


@login_required
@permission_required('fleet_management.add_trip')
def set_trip(request):
    # date would be current date if no specific date
    # provided via get parameters
    d = request.GET.get('date')
    d = datetime.strptime(d, '%Y-%m-%d') if d else now().today()
    context = {'date': d.strftime('%Y-%m-%d')}

    if request.method == 'POST':
        trip_form = TripForm(request.POST)
        context['trip_form'] = trip_form
        if trip_form.is_valid():
            trip_form.save()
            messages.success(request, 'Trip has been Set Successfully')
            return redirect(reverse('available_vehicles'))
        else:
            messages.error(request, 'Trip setting not Successfull')
    else:
        trip_form = TripForm(initial={'date': d.strftime('%Y-%m-%d')})
        context['trip_form'] = trip_form
    return render(request, 'fleet_management/trip_form.html', context)


@login_required
@permission_required('fleet_management.add_vehicleinoutinfo')
def set_vehicle_in_out_info(request):
    # date would be current date if no specific date
    # provided via get parameters
    d = request.GET.get('date')
    d = datetime.strptime(d, '%Y-%m-%d') if d else now().today()
    context = {'date': d.strftime('%Y-%m-%d')}

    trips = Trip.objects.filter(date=d)

    if request.method == 'POST':
        trip_id, route_id, method = request.POST.get('change_info').split()
        trip = get_object_or_404(VehicleInOutInfo, id=trip_id)
        if method == 'is_leaved':
            trip.is_leaved = not trip.is_leaved
            trip.leaved_at = now()
        elif method == 'is_arrived':
            trip.is_arrived = not trip.is_arrived
            trip.arrived_at = now()
        trip.save()
        messages.success(request, 'Vehicle info Updated Successfully')

    # We have to differentiate trips to comment easily
    # about its leave/arrival information.
    trips_will_leave = trips.filter(origin__branch_manager=request.user)
    trips_will_arrive = trips.filter(destination__branch_manager=request.user)
    trips_via = trips.filter(via__branch_manager=request.user)

    vehicles_will_leave = []
    for trip in trips_will_leave:
        vehicles_will_leave.append(VehicleInOutInfo.objects.get_or_create(trip=trip, route=request.user.route)[0])

    vehicles_will_arrive = []
    for trip in trips_will_arrive:
        vehicles_will_arrive.append(VehicleInOutInfo.objects.get_or_create(trip=trip, route=request.user.route)[0])

    vehicles_via = []
    for trip in trips_via:
        vehicles_via.append(VehicleInOutInfo.objects.get_or_create(trip=trip, route=request.user.route)[0])

    context['vehicles_will_arrive'] = vehicles_will_arrive
    context['vehicles_will_leave'] = vehicles_will_leave
    context['vehicles_via'] = vehicles_via

    return render(request, 'fleet_management/vehicle_in_out_info_form.html', context)
