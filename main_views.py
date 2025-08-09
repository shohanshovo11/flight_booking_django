from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from flights.models import Flight, Airport
from bookings.models import Booking

def home(request):
    # Get popular destinations
    popular_destinations = Airport.objects.annotate(
        flight_count=Count('arriving_flights')
    ).order_by('-flight_count')[:6]
    
    # Get upcoming flights
    upcoming_flights = Flight.objects.filter(
        departure_time__gte=timezone.now(),
        departure_time__lte=timezone.now() + timedelta(days=7),
        status='scheduled'
    ).select_related('airline', 'departure_airport', 'arrival_airport')[:6]
    
    return render(request, 'home.html', {
        'popular_destinations': popular_destinations,
        'upcoming_flights': upcoming_flights
    })

@login_required
def dashboard(request):
    # Get all user bookings (without slicing first)
    all_user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    # Statistics
    total_bookings = all_user_bookings.count()
    upcoming_trips = all_user_bookings.filter(
        flight__departure_time__gte=timezone.now(),
        status='confirmed'
    ).count()
    
    # Get recent bookings for display (slice at the end)
    user_bookings = all_user_bookings[:5]
    
    return render(request, 'dashboard.html', {
        'user_bookings': user_bookings,
        'total_bookings': total_bookings,
        'upcoming_trips': upcoming_trips
    })

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Here you would typically save to database or send email
        # For now, just show success message
        return render(request, 'contact.html', {
            'success': True,
            'message': 'Thank you for your message! We will get back to you soon.'
        })
    
    return render(request, 'contact.html')
