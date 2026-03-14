from django.contrib import admin
from .models import Movie, Hall, ShowTime, Booking, Feedback


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'status', 'release_date', 'language']
    list_filter = ['status', 'genre', 'language']
    search_fields = ['title', 'director', 'cast']
    list_editable = ['status']


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_seats', 'rows', 'seats_per_row']


@admin.register(ShowTime)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ['movie', 'hall', 'show_date', 'show_time', 'ticket_price', 'available_seats']
    list_filter = ['show_date', 'movie']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'customer_name', 'showtime', 'num_seats', 'total_amount', 'payment_method', 'payment_status', 'status', 'booking_date']
    list_filter = ['status', 'payment_method', 'payment_status', 'booking_date']
    search_fields = ['booking_reference', 'customer_name', 'customer_email', 'transaction_id']
    readonly_fields = ['booking_reference', 'booking_date']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'movie', 'rating', 'created_at', 'is_approved']
    list_filter = ['rating', 'is_approved']
    list_editable = ['is_approved']
