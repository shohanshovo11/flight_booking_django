from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from flights.models import Airport, Airline, Aircraft, Flight, SeatClass, Seat
import random

class Command(BaseCommand):
    help = 'Populate the database with sample flight data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create Airports
        airports_data = [
            {'code': 'NYC', 'name': 'John F. Kennedy International Airport', 'city': 'New York', 'country': 'USA', 'timezone': 'America/New_York'},
            {'code': 'LAX', 'name': 'Los Angeles International Airport', 'city': 'Los Angeles', 'country': 'USA', 'timezone': 'America/Los_Angeles'},
            {'code': 'LHR', 'name': 'London Heathrow Airport', 'city': 'London', 'country': 'UK', 'timezone': 'Europe/London'},
            {'code': 'DXB', 'name': 'Dubai International Airport', 'city': 'Dubai', 'country': 'UAE', 'timezone': 'Asia/Dubai'},
            {'code': 'BOM', 'name': 'Chhatrapati Shivaji International Airport', 'city': 'Mumbai', 'country': 'India', 'timezone': 'Asia/Kolkata'},
            {'code': 'SYD', 'name': 'Kingsford Smith Airport', 'city': 'Sydney', 'country': 'Australia', 'timezone': 'Australia/Sydney'},
            {'code': 'NRT', 'name': 'Narita International Airport', 'city': 'Tokyo', 'country': 'Japan', 'timezone': 'Asia/Tokyo'},
            {'code': 'CDG', 'name': 'Charles de Gaulle Airport', 'city': 'Paris', 'country': 'France', 'timezone': 'Europe/Paris'},
        ]
        
        for airport_data in airports_data:
            airport, created = Airport.objects.get_or_create(
                code=airport_data['code'],
                defaults=airport_data
            )
            if created:
                self.stdout.write(f'Created airport: {airport.code}')

        # Create Airlines
        airlines_data = [
            {'code': 'AA', 'name': 'American Airlines'},
            {'code': 'UA', 'name': 'United Airlines'},
            {'code': 'DL', 'name': 'Delta Airlines'},
            {'code': 'BA', 'name': 'British Airways'},
            {'code': 'EK', 'name': 'Emirates'},
            {'code': 'AI', 'name': 'Air India'},
            {'code': 'QF', 'name': 'Qantas'},
            {'code': 'AF', 'name': 'Air France'},
        ]
        
        for airline_data in airlines_data:
            airline, created = Airline.objects.get_or_create(
                code=airline_data['code'],
                defaults=airline_data
            )
            if created:
                self.stdout.write(f'Created airline: {airline.code}')

        # Create Aircraft
        aircraft_data = [
            {'manufacturer': 'Boeing', 'model': '737-800', 'capacity': 180},
            {'manufacturer': 'Boeing', 'model': '777-300ER', 'capacity': 350},
            {'manufacturer': 'Airbus', 'model': 'A320', 'capacity': 180},
            {'manufacturer': 'Airbus', 'model': 'A380', 'capacity': 550},
            {'manufacturer': 'Boeing', 'model': '787-9', 'capacity': 290},
        ]
        
        for aircraft_info in aircraft_data:
            aircraft, created = Aircraft.objects.get_or_create(
                manufacturer=aircraft_info['manufacturer'],
                model=aircraft_info['model'],
                defaults=aircraft_info
            )
            if created:
                self.stdout.write(f'Created aircraft: {aircraft.manufacturer} {aircraft.model}')

        # Create Flights
        airports = list(Airport.objects.all())
        airlines = list(Airline.objects.all())
        aircrafts = list(Aircraft.objects.all())
        
        # Generate flights for the next 30 days
        for day in range(30):
            date = timezone.now().date() + timedelta(days=day)
            
            for _ in range(random.randint(5, 15)):  # 5-15 flights per day
                departure_airport = random.choice(airports)
                arrival_airport = random.choice([a for a in airports if a != departure_airport])
                
                # Random departure time
                hour = random.randint(6, 22)
                minute = random.choice([0, 15, 30, 45])
                departure_time = timezone.make_aware(
                    datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute))
                )
                
                # Flight duration (2-12 hours)
                duration_hours = random.randint(2, 12)
                duration = timedelta(hours=duration_hours, minutes=random.randint(0, 59))
                arrival_time = departure_time + duration
                
                flight = Flight.objects.create(
                    flight_number=str(random.randint(100, 9999)),
                    airline=random.choice(airlines),
                    aircraft=random.choice(aircrafts),
                    departure_airport=departure_airport,
                    arrival_airport=arrival_airport,
                    departure_time=departure_time,
                    arrival_time=arrival_time,
                    duration=duration,
                    base_price=Decimal(str(random.randint(200, 1500))),
                    available_seats=random.randint(50, 200)
                )
                
                # Create seat classes
                seat_classes_data = [
                    {'class_type': 'economy', 'price_multiplier': Decimal('1.0'), 'available_seats': int(flight.available_seats * 0.7), 'baggage_allowance': 23},
                    {'class_type': 'premium_economy', 'price_multiplier': Decimal('1.5'), 'available_seats': int(flight.available_seats * 0.2), 'baggage_allowance': 32},
                    {'class_type': 'business', 'price_multiplier': Decimal('3.0'), 'available_seats': int(flight.available_seats * 0.08), 'baggage_allowance': 32},
                    {'class_type': 'first', 'price_multiplier': Decimal('5.0'), 'available_seats': int(flight.available_seats * 0.02), 'baggage_allowance': 32},
                ]
                
                for class_data in seat_classes_data:
                    if class_data['available_seats'] > 0:
                        seat_class = SeatClass.objects.create(
                            flight=flight,
                            **class_data
                        )
                        
                        # Create seats for this class
                        seat_counter = 0
                        for i in range(class_data['available_seats']):
                            row = (seat_counter // 6) + 1
                            seat_letter = chr(65 + (seat_counter % 6))  # A, B, C, D, E, F
                            seat_number = f"{class_data['class_type'][0].upper()}{row}{seat_letter}"
                            
                            Seat.objects.create(
                                flight=flight,
                                seat_number=seat_number,
                                seat_class=seat_class,
                                is_window=(seat_letter in ['A', 'F']),
                                is_aisle=(seat_letter in ['C', 'D'])
                            )
                            seat_counter += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created sample data with {Flight.objects.count()} flights')
        )
