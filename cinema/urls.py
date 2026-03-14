from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('upcoming/', views.upcoming_movies, name='upcoming'),
    path('book/<int:showtime_id>/', views.book_ticket, name='book_ticket'),
    path('book/<int:showtime_id>/payment/', views.payment, name='payment'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/check/', views.check_booking, name='check_booking'),
    path('feedback/', views.feedback, name='feedback'),
]
