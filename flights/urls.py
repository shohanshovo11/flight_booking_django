from django.urls import path
from . import views

app_name = 'flights'

urlpatterns = [
    path('search/', views.search_flights, name='search'),
    path('list/', views.flight_list, name='list'),
    path('<int:flight_id>/', views.flight_detail, name='detail'),
]
