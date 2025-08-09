from django.contrib import admin
from .models import Airport, Airline, Aircraft, Flight, SeatClass, Seat

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city', 'country')
    search_fields = ('code', 'name', 'city')
    list_filter = ('country',)

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = ('manufacturer', 'model', 'capacity')
    search_fields = ('manufacturer', 'model')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline', 'departure_airport', 'arrival_airport', 
                    'departure_time', 'status', 'available_seats')
    list_filter = ('status', 'airline', 'departure_airport', 'arrival_airport')
    search_fields = ('flight_number', 'airline__name')
    date_hierarchy = 'departure_time'

@admin.register(SeatClass)
class SeatClassAdmin(admin.ModelAdmin):
    list_display = ('flight', 'class_type', 'get_price', 'available_seats')
    list_filter = ('class_type',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('flight', 'seat_number', 'seat_class', 'is_available', 'is_window', 'is_aisle')
    list_filter = ('seat_class', 'is_available', 'is_window', 'is_aisle')
    search_fields = ('flight__flight_number', 'seat_number')
