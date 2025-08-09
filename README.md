# Flight Booking System - Django Backend

A comprehensive Django-based flight booking system with user authentication, flight search, booking management, and dynamic frontend integration.

## 🚀 Features

### User Management

- **User Registration & Authentication**: Custom user model with extended profile information
- **User Dashboard**: Personalized dashboard showing booking history and statistics
- **Profile Management**: Emergency contact information and travel preferences

### Flight Management

- **Flight Search**: Advanced search with filters for departure/arrival cities and dates
- **Dynamic Pricing**: Multiple seat classes (Economy, Premium Economy, Business, First Class)
- **Real-time Availability**: Live seat availability tracking
- **Airline & Airport Management**: Comprehensive database of airlines, airports, and aircraft

### Booking System

- **Multi-passenger Bookings**: Support for group bookings with individual passenger details
- **Seat Selection**: Interactive seat map with availability tracking
- **Payment Processing**: Integrated payment system with multiple payment methods
- **Booking Management**: View, modify, and cancel bookings
- **Baggage Options**: Additional baggage selection with pricing

### Admin Panel

- **Complete Admin Interface**: Django admin for managing all entities
- **Data Management**: Airlines, airports, flights, bookings, and user management
- **Analytics**: Booking statistics and flight performance tracking

## 🛠 Technology Stack

- **Backend**: Django 5.2.4 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: Bootstrap 5 + Custom CSS/JavaScript
- **Authentication**: Django's built-in authentication system with custom user model
- **File Storage**: Django's file handling for media uploads

## 📁 Project Structure

```
backend/
├── flight_booking/          # Main Django project
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── accounts/               # User authentication app
│   ├── models.py          # Custom user and profile models
│   ├── views.py           # Authentication views
│   ├── forms.py           # User forms
│   └── admin.py           # Admin configuration
├── flights/                # Flight management app
│   ├── models.py          # Flight, airline, airport models
│   ├── views.py           # Flight search and listing
│   ├── admin.py           # Flight admin interface
│   └── management/        # Custom management commands
├── bookings/               # Booking management app
│   ├── models.py          # Booking, passenger, payment models
│   ├── views.py           # Booking process views
│   ├── forms.py           # Booking forms
│   └── admin.py           # Booking admin interface
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Homepage
│   ├── dashboard.html     # User dashboard
│   ├── accounts/          # Authentication templates
│   ├── flights/           # Flight templates
│   └── bookings/          # Booking templates
├── static/                 # Static files (CSS, JS, images)
└── manage.py              # Django management script
```

## 🚦 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the backend directory**:

   ```bash
   cd "c:\Users\Asus\Desktop\Desktop\Ass\ariyan\web dev\ass 3\backend"
   ```

2. **Install dependencies**:

   ```bash
   pip install django djangorestframework pillow
   ```

3. **Run database migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

5. **Populate with sample data**:

   ```bash
   python manage.py populate_sample_data
   ```

6. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   - Frontend: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## 🎯 Key URLs

### Frontend URLs

- `/` - Homepage with flight search
- `/flights/list/` - Browse all flights
- `/flights/search/` - Advanced flight search
- `/dashboard/` - User dashboard (requires login)
- `/accounts/login/` - User login
- `/accounts/register/` - User registration
- `/accounts/profile/` - User profile management
- `/bookings/list/` - User's booking history
- `/contact/` - Contact page

### API Endpoints

- Flight search with real-time results
- Booking management APIs
- User authentication endpoints

## 🔧 Configuration

### Database

The project uses SQLite by default for development. For production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'flight_booking_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files

Static files are configured for development. For production:

```bash
python manage.py collectstatic
```

### Media Files

User uploads (profile pictures, airline logos) are stored in the `media/` directory.

## 📊 Sample Data

The project includes a management command to populate the database with realistic sample data:

- **8 Major Airports**: NYC, LAX, LHR, DXB, BOM, SYD, NRT, CDG
- **8 Airlines**: American Airlines, United, Delta, British Airways, Emirates, Air India, Qantas, Air France
- **5 Aircraft Types**: Boeing 737-800, 777-300ER, Airbus A320, A380, Boeing 787-9
- **300+ Flights**: Automatically generated for the next 30 days
- **Multiple Seat Classes**: Economy, Premium Economy, Business, First Class
- **Realistic Pricing**: Dynamic pricing based on seat class and route

## 🔐 Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **User Authentication**: Secure login/logout functionality
- **Permission Controls**: User-specific data access
- **Input Validation**: Form validation and sanitization
- **Password Security**: Django's built-in password hashing

## 🎨 Frontend Features

### Responsive Design

- **Mobile-First**: Responsive design that works on all devices
- **Bootstrap 5**: Modern UI components and styling
- **Custom CSS**: Brand-specific styling with CSS variables

### Interactive Elements

- **Dynamic Search**: Real-time flight search with AJAX
- **Form Validation**: Client-side and server-side validation
- **Progress Indicators**: Booking process with clear steps
- **Interactive Seat Maps**: Visual seat selection interface

### User Experience

- **Intuitive Navigation**: Clear navigation structure
- **Loading States**: User feedback during async operations
- **Error Handling**: Graceful error messages and fallbacks
- **Accessibility**: ARIA labels and keyboard navigation support

## 🚀 Deployment

### Development

```bash
python manage.py runserver
```

### Production

1. **Set DEBUG = False** in settings.py
2. **Configure ALLOWED_HOSTS**
3. **Set up static file serving**
4. **Configure database**
5. **Set up HTTPS**
6. **Use production WSGI server** (e.g., Gunicorn)

## 🤝 Admin Interface

Access the Django admin at `/admin/` with superuser credentials:

### Available Models

- **Users**: Manage user accounts and profiles
- **Airports**: Add/edit airport information
- **Airlines**: Manage airline details and logos
- **Aircraft**: Configure aircraft types and capacities
- **Flights**: Create and manage flight schedules
- **Bookings**: View and manage customer bookings
- **Payments**: Track payment transactions

## 📱 API Documentation

### Flight Search API

```javascript
POST /
  flights /
  search /
  {
    departure_city: "New York",
    arrival_city: "Los Angeles",
    departure_date: "2024-12-25",
    passengers: 2,
  };
```

### Booking Creation

```javascript
POST /
  bookings /
  create /
  { flight_id } /
  {
    seat_class: 1,
    passengers_data: [
      {
        first_name: "John",
        last_name: "Doe",
        date_of_birth: "1990-01-01",
        gender: "M",
        nationality: "USA",
      },
    ],
  };
```

## 🎯 Future Enhancements

- **Payment Gateway Integration**: Stripe, PayPal integration
- **Email Notifications**: Booking confirmations and reminders
- **Mobile App**: React Native mobile application
- **Advanced Search**: Filters for stops, duration, price range
- **Loyalty Program**: Points and rewards system
- **Multi-language Support**: Internationalization
- **Real-time Updates**: WebSocket integration for live updates
- **Social Authentication**: Google, Facebook login
- **Travel Insurance**: Optional insurance offerings
- **Group Bookings**: Corporate booking management

## 🐛 Troubleshooting

### Common Issues

1. **Migration Errors**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Static Files Not Loading**:

   ```bash
   python manage.py collectstatic
   ```

3. **Import Errors**:
   Check that all dependencies are installed:

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Issues**:
   Reset database:
   ```bash
   python manage.py flush
   python manage.py migrate
   python manage.py populate_sample_data
   ```

## 📞 Support

For support and questions:

- Create an issue in the project repository
- Contact the development team
- Check the Django documentation for framework-specific issues

## 📄 License

This project is developed for educational and demonstration purposes. Please ensure compliance with all relevant licensing requirements for production use.

---

**Happy Flying! ✈️**
