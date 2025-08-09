from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:flight_id>/', views.create_booking, name='create'),
    path('<int:booking_id>/', views.booking_detail, name='detail'),
    path('list/', views.booking_list, name='list'),
    path('<int:booking_id>/seats/', views.seat_selection, name='seat_selection'),
    path('<int:booking_id>/payment/', views.payment_view, name='payment'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel'),
]
