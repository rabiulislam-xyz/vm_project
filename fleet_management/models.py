import datetime
from django.db import models
from django.conf import settings


class Vehicle(models.Model):
    CATEGORY_CHOICES = (
        ('L', 'Light'),
        ('H', 'Heavy')
    )

    number = models.CharField(max_length=127, unique=True)
    model        = models.CharField(max_length=127)
    joining_date = models.DateField(auto_now_add=True)
    capacity     = models.PositiveIntegerField()
    category     = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.number



class VehicleCondition(models.Model):
    vehicle = models.ForeignKey(Vehicle,
                                on_delete=models.CASCADE,
                                unique_for_date='date',
                                related_name='conditions')

    is_ok = models.BooleanField(default=True)
    date = models.DateField(default=datetime.date.today)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehicle.number


class Route(models.Model):
    CATEGORY_CHOICES = (
        ('L', 'Long Distance'),
        ('S', 'Short Distance')
    )

    name           = models.CharField(max_length=127, unique=True)
    category       = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    branch_manager = models.OneToOneField(settings.AUTH_USER_MODEL,
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          related_name='route',
                                          limit_choices_to={"groups__name": "Branch Manager"})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    vehicle     = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    origin      = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='outgoing_trips')
    destination = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='incoming_trips')
    via         = models.ManyToManyField(Route, blank=True)

    driver      = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    limit_choices_to={"groups__name": "Driver"}
                                    )

    date = models.DateField(default=datetime.date.today)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def via_list(self):
        return ', '.join([v.name for v in self.via.all()])


    def __str__(self):
        return "vehicle no: {}, from:{} to:{}, driver: {}.".format(self.vehicle, self.origin.name, self.destination.name, self.driver.name)


class VehicleInOutInfo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='trip_info')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_info')
    is_arrived = models.BooleanField(default=False)
    is_leaved = models.BooleanField(default=False)
    arrived_at = models.DateTimeField(null=True, blank=True)
    leaved_at = models.DateTimeField(null=True, blank=True)

    date = models.DateField(default=datetime.date.today)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "vehicle no: '{}' trip id: {}, route: {}".format(self.trip.vehicle, self.trip.id, self.route.name)
