from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Flight, Airport, SeatClass
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

def search_flights(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        departure_city = data.get('departure_city', '')
        arrival_city = data.get('arrival_city', '')
        departure_date = data.get('departure_date', '')
        return_date = data.get('return_date', '')
        passengers = int(data.get('passengers', 1))
        
        flights = Flight.objects.filter(
            departure_airport__city__icontains=departure_city,
            arrival_airport__city__icontains=arrival_city,
            departure_time__date=departure_date,
            available_seats__gte=passengers,
            status='scheduled'
        ).select_related('airline', 'departure_airport', 'arrival_airport', 'aircraft')
        
        flight_data = []
        for flight in flights:
            seat_classes = SeatClass.objects.filter(flight=flight, available_seats__gte=passengers)
            classes_data = []
            for seat_class in seat_classes:
                classes_data.append({
                    'type': seat_class.class_type,
                    'price': float(seat_class.get_price()),
                    'available_seats': seat_class.available_seats,
                    'baggage_allowance': seat_class.baggage_allowance
                })
            
            flight_data.append({
                'id': flight.id,
                'flight_number': f"{flight.airline.code}{flight.flight_number}",
                'airline': flight.airline.name,
                'departure_airport': f"{flight.departure_airport.code} - {flight.departure_airport.name}",
                'arrival_airport': f"{flight.arrival_airport.code} - {flight.arrival_airport.name}",
                'departure_time': flight.departure_time.strftime('%Y-%m-%d %H:%M'),
                'arrival_time': flight.arrival_time.strftime('%Y-%m-%d %H:%M'),
                'duration': str(flight.duration),
                'available_seats': flight.available_seats,
                'seat_classes': classes_data
            })
        
        return JsonResponse({'flights': flight_data})
    
    # GET request - show search form
    airports = Airport.objects.all().order_by('city')
    cities = airports.values_list('city', flat=True).distinct()
    return render(request, 'flights/search.html', {'cities': cities})

def flight_list(request):
    flights = Flight.objects.filter(
        departure_time__gte=timezone.now(),
        status='scheduled'
    ).select_related('airline', 'departure_airport', 'arrival_airport')
    
    # Search filters
    departure_city = request.GET.get('departure_city')
    arrival_city = request.GET.get('arrival_city')
    departure_date = request.GET.get('departure_date')
    
    if departure_city:
        flights = flights.filter(departure_airport__city__icontains=departure_city)
    if arrival_city:
        flights = flights.filter(arrival_airport__city__icontains=arrival_city)
    if departure_date:
        try:
            date_obj = datetime.strptime(departure_date, '%Y-%m-%d').date()
            flights = flights.filter(departure_time__date=date_obj)
        except ValueError:
            pass
    
    paginator = Paginator(flights, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    airports = Airport.objects.all().order_by('city')
    cities = airports.values_list('city', flat=True).distinct()
    
    return render(request, 'flights/list.html', {
        'page_obj': page_obj,
        'cities': cities,
        'search_params': {
            'departure_city': departure_city or '',
            'arrival_city': arrival_city or '',
            'departure_date': departure_date or ''
        }
    })

def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    seat_classes = SeatClass.objects.filter(flight=flight)
    
    return render(request, 'flights/detail.html', {
        'flight': flight,
        'seat_classes': seat_classes
    })
