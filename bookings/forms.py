from django import forms
from .models import Booking, Passenger, Payment
from flights.models import SeatClass

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['seat_class']
        widgets = {
            'seat_class': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        flight = kwargs.pop('flight', None)
        super().__init__(*args, **kwargs)
        if flight:
            self.fields['seat_class'].queryset = SeatClass.objects.filter(flight=flight)

class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'passport_number', 'nationality']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'})
        }
