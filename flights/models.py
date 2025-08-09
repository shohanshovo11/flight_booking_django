from django.db import models
from decimal import Decimal

class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)  # IATA code
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Airline(models.Model):
    code = models.CharField(max_length=3, unique=True)  # IATA code
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='airlines/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Aircraft(models.Model):
    model = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    capacity = models.IntegerField()
    
    def __str__(self):
        return f"{self.manufacturer} {self.model}"

class Flight(models.Model):
    FLIGHT_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('departed', 'Departed'),
        ('arrived', 'Arrived'),
        ('cancelled', 'Cancelled'),
        ('delayed', 'Delayed'),
    ]
    
    flight_number = models.CharField(max_length=10)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(Airport, related_name='departing_flights', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(Airport, related_name='arriving_flights', on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    duration = models.DurationField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=FLIGHT_STATUS_CHOICES, default='scheduled')
    available_seats = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['flight_number', 'departure_time']
    
    def __str__(self):
        return f"{self.airline.code}{self.flight_number} - {self.departure_airport.code} to {self.arrival_airport.code}"

class SeatClass(models.Model):
    CLASS_TYPES = [
        ('economy', 'Economy'),
        ('premium_economy', 'Premium Economy'),
        ('business', 'Business'),
        ('first', 'First Class'),
    ]
    
    flight = models.ForeignKey(Flight, related_name='seat_classes', on_delete=models.CASCADE)
    class_type = models.CharField(max_length=20, choices=CLASS_TYPES)
    price_multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('1.00'))
    available_seats = models.IntegerField()
    baggage_allowance = models.IntegerField(help_text="Baggage allowance in kg")
    
    class Meta:
        unique_together = ['flight', 'class_type']
    
    def get_price(self):
        return self.flight.base_price * self.price_multiplier
    
    def __str__(self):
        return f"{self.flight} - {self.class_type}"

class Seat(models.Model):
    flight = models.ForeignKey(Flight, related_name='seats', on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    seat_class = models.ForeignKey(SeatClass, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    is_window = models.BooleanField(default=False)
    is_aisle = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['flight', 'seat_number']
    
    def __str__(self):
        return f"{self.flight} - Seat {self.seat_number}"
