#!/bin/bash

echo "=== Flight Booking Site - MySQL Database Setup ==="
echo "This script will help you set up the MySQL database for the Django project."
echo

# Check if MySQL is running
echo "Checking MySQL service status..."
if net start | findstr -i mysql > /dev/null; then
    echo "✓ MySQL service is running"
else
    echo "✗ MySQL service is not running. Please start MySQL service first."
    echo "  You can start it with: net start MySQL80"
    exit 1
fi

echo
echo "Next steps:"
echo "1. Update the MySQL password in flight_booking/settings.py"
echo "   Change 'PASSWORD': 'password123' to your actual MySQL root password"
echo
echo "2. Create the database by running:"
echo "   python manage.py shell -c \"from django.db import connection; cursor = connection.cursor(); cursor.execute('CREATE DATABASE IF NOT EXISTS flight_booking_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'); print('Database created successfully!')\""
echo
echo "3. Run Django migrations:"
echo "   python manage.py migrate"
echo
echo "4. Create a superuser:"
echo "   python manage.py createsuperuser"
echo
echo "5. Populate sample data:"
echo "   python manage.py populate_sample_data"
echo
echo "6. Start the development server:"
echo "   python manage.py runserver"
echo
echo "=== Database Connection Test ==="
echo "You can test the database connection with:"
echo "python manage.py dbshell"
echo
echo "If you get 'Access denied' errors, please:"
echo "1. Check your MySQL root password"
echo "2. Update the password in settings.py"
echo "3. Or create a new MySQL user for this project"
