from django.core.management.base import BaseCommand
import mysql.connector
from mysql.connector import Error
from django.conf import settings

class Command(BaseCommand):
    help = 'Create MySQL database for the project'

    def add_arguments(self, parser):
        parser.add_argument('--password', type=str, help='MySQL root password', default='')
        parser.add_argument('--user', type=str, help='MySQL username', default='root')
        parser.add_argument('--host', type=str, help='MySQL host', default='localhost')
        parser.add_argument('--port', type=str, help='MySQL port', default='3306')

    def handle(self, *args, **options):
        password = options['password']
        user = options['user']
        host = options['host']
        port = options['port']
        
        db_config = settings.DATABASES['default']
        database_name = db_config['NAME']
        
        try:
            # Connect to MySQL server
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                
                # Create database
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created database: {database_name}')
                )
                
                # Grant privileges (optional)
                cursor.execute(f"GRANT ALL PRIVILEGES ON {database_name}.* TO '{user}'@'{host}'")
                cursor.execute("FLUSH PRIVILEGES")
                
                cursor.close()
                connection.close()
                
                self.stdout.write(
                    self.style.SUCCESS('Database setup completed successfully!')
                )
                self.stdout.write(
                    self.style.WARNING('Next steps:')
                )
                self.stdout.write('1. Update your MySQL password in settings.py')
                self.stdout.write('2. Run: python manage.py migrate')
                self.stdout.write('3. Run: python manage.py createsuperuser')
                self.stdout.write('4. Run: python manage.py populate_sample_data')
                
        except Error as e:
            self.stdout.write(
                self.style.ERROR(f'Error connecting to MySQL: {e}')
            )
            self.stdout.write(
                self.style.WARNING('Make sure MySQL server is running and credentials are correct')
            )
