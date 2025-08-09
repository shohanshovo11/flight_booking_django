from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Booking, Passenger, Payment, Baggage
from flights.models import Flight, SeatClass, Seat
from .forms import BookingForm, PassengerForm
import json
import uuid

@login_required
def create_booking(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    seat_classes = SeatClass.objects.filter(flight=flight)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, flight=flight)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.flight = flight
            
            # Get passengers data to calculate total
            passengers_data_str = request.POST.get('passengers_data', '[]')
            try:
                passengers_data = json.loads(passengers_data_str)
            except json.JSONDecodeError:
                passengers_data = []
            
            num_passengers = len(passengers_data) if passengers_data else 1  # Default to 1 passenger
            
            # Calculate total amount
            seat_class = form.cleaned_data['seat_class']
            base_price = flight.base_price
            class_multiplier = getattr(seat_class, 'price_multiplier', 1.0) if seat_class else 1.0
            total_amount = base_price * class_multiplier * num_passengers
            
            booking.total_amount = total_amount
            booking.save()
            
            # Create passengers
            if passengers_data:
                for passenger_data in passengers_data:
                    passenger = Passenger.objects.create(
                        booking=booking,
                        first_name=passenger_data.get('first_name', ''),
                        last_name=passenger_data.get('last_name', ''),
                        date_of_birth=passenger_data.get('date_of_birth', '1990-01-01'),
                        gender=passenger_data.get('gender', 'M'),
                        passport_number=passenger_data.get('passport_number', ''),
                        nationality=passenger_data.get('nationality', '')
                    )
            else:
                # Create a default passenger if no data provided
                passenger = Passenger.objects.create(
                    booking=booking,
                    first_name=request.user.first_name or 'Guest',
                    last_name=request.user.last_name or 'User',
                    date_of_birth='1990-01-01',
                    gender='M',
                    passport_number='',
                    nationality='Unknown'
                )
            
            messages.success(request, f'Booking created successfully! Reference: {booking.booking_reference}')
            return redirect('bookings:detail', booking_id=booking.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookingForm(flight=flight)
    
    return render(request, 'bookings/create.html', {
        'form': form,
        'flight': flight,
        'seat_classes': seat_classes
    })

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    passengers = booking.passengers.all()
    
    try:
        payment = booking.payment
    except Payment.DoesNotExist:
        payment = None
    
    return render(request, 'bookings/detail.html', {
        'booking': booking,
        'passengers': passengers,
        'payment': payment
    })

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/list.html', {'bookings': bookings})

@login_required
@csrf_exempt
def seat_selection(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        data = json.loads(request.body)
        seat_assignments = data.get('seat_assignments', [])
        
        for assignment in seat_assignments:
            passenger_id = assignment['passenger_id']
            seat_id = assignment['seat_id']
            
            passenger = get_object_or_404(Passenger, id=passenger_id, booking=booking)
            seat = get_object_or_404(Seat, id=seat_id, flight=booking.flight, is_available=True)
            
            passenger.seat = seat
            passenger.save()
            
            seat.is_available = False
            seat.save()
        
        return JsonResponse({'success': True, 'message': 'Seats assigned successfully!'})
    
    # GET request - show seat map
    seats = Seat.objects.filter(flight=booking.flight, seat_class=booking.seat_class)
    passengers = booking.passengers.all()
    
    return render(request, 'bookings/seat_selection.html', {
        'booking': booking,
        'seats': seats,
        'passengers': passengers
    })

@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_amount,
            payment_method=payment_method,
            transaction_id=str(uuid.uuid4()),
            status='completed',  # In real app, integrate with payment gateway
            processed_at=timezone.now()
        )
        
        booking.status = 'confirmed'
        booking.save()
        
        messages.success(request, 'Payment processed successfully! Your booking is confirmed.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    return render(request, 'bookings/payment.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        
        # Free up seats
        for passenger in booking.passengers.all():
            if passenger.seat:
                passenger.seat.is_available = True
                passenger.seat.save()
        
        messages.success(request, 'Booking cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    
    return redirect('bookings:list')
