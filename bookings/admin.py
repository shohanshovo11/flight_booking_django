from django.contrib import admin
from .models import Booking, Passenger, Payment, Baggage

class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 1

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'user', 'flight', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('booking_reference', 'user__username', 'flight__flight_number')
    inlines = [PassengerInline]
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'booking', 'nationality', 'seat')
    search_fields = ('first_name', 'last_name', 'passport_number')
    list_filter = ('gender', 'nationality')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('booking__booking_reference', 'transaction_id')
    readonly_fields = ('created_at', 'processed_at')

@admin.register(Baggage)
class BaggageAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'weight', 'additional_fee')
    search_fields = ('passenger__first_name', 'passenger__last_name')
