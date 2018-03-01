from django import forms

from .models import VehicleCondition, Trip, Vehicle


class VehicleConditionForm(forms.ModelForm):
    class Meta:
        model = VehicleCondition
        fields = '__all__'

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'origin': forms.Select(attrs={'class': 'form-control'}),
            'destination': forms.Select(attrs={'class': 'form-control'}),
            'via': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'driver': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'data-toggle':"datepicker"}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        vehicle = self.cleaned_data.get('vehicle')

        vehicles_condition = VehicleCondition.objects.filter(date=date).filter(is_ok=True)
        print(vehicles_condition)

        available_vehicles = [condition.vehicle for condition in vehicles_condition]
        print(available_vehicles)
        if vehicle not in available_vehicles:
            print('not availabe')
            raise forms.ValidationError("Vehicle '{}' is Not Available in this Date!".format(vehicle.number))

        trip = Trip.objects.filter(date=date, vehicle=vehicle).select_related('vehicle').all()
        if trip.exists():
            print('confirmed')
            raise forms.ValidationError("Vehicle '{}' is Confirmed for a Trip in This Date!".format(vehicle.number))
        return date