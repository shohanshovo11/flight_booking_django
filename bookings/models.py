from django.db import models
from django.conf import settings
from flights.models import Flight, Seat, SeatClass

class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_reference = models.CharField(max_length=10, unique=True)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat_class = models.ForeignKey(SeatClass, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import random
            import string
            self.booking_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Booking {self.booking_reference} - {self.user.username}"

class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    booking = models.ForeignKey(Booking, related_name='passengers', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    passport_number = models.CharField(max_length=20, blank=True)
    nationality = models.CharField(max_length=50)
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Payment for {self.booking.booking_reference}"

class Baggage(models.Model):
    passenger = models.ForeignKey(Passenger, related_name='baggage', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    additional_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Baggage for {self.passenger}"
