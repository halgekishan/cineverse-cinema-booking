from django.db import models
from django.utils import timezone


class Movie(models.Model):
    STATUS_CHOICES = [
        ('now_showing', 'Now Showing'),
        ('upcoming', 'Upcoming'),
        ('ended', 'Ended'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True, help_text="YouTube embed URL")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    rating = models.CharField(max_length=10, default='U/A')
    language = models.CharField(max_length=50, default='English')
    director = models.CharField(max_length=100, blank=True)
    cast = models.TextField(blank=True, help_text="Comma separated cast names")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_date']


class Hall(models.Model):
    name = models.CharField(max_length=100)
    total_seats = models.IntegerField(default=100)
    rows = models.IntegerField(default=10)
    seats_per_row = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    show_date = models.DateField()
    show_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, default=150.00)

    def __str__(self):
        return f"{self.movie.title} - {self.show_date} {self.show_time}"

    def booked_seats_count(self):
        return self.bookings.filter(status='confirmed').aggregate(
            total=models.Sum('num_seats')
        )['total'] or 0

    def available_seats(self):
        return self.hall.total_seats - self.booked_seats_count()

    def get_booked_seat_numbers(self):
        booked = []
        for booking in self.bookings.filter(status='confirmed'):
            booked.extend(booking.seat_numbers.split(','))
        return [s.strip() for s in booked if s.strip()]

    class Meta:
        ordering = ['show_date', 'show_time']


class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('card', 'Credit / Debit Card'),
        ('netbanking', 'Net Banking'),
        ('counter', 'Pay at Counter'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    ]
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='bookings')
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    num_seats = models.IntegerField(default=1)
    seat_numbers = models.CharField(max_length=200, help_text="Comma separated seat numbers e.g. A1,A2")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    booking_reference = models.CharField(max_length=20, unique=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='counter')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Booking {self.booking_reference} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import random, string
            self.booking_reference = 'CIN' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)


class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return f"Feedback by {self.customer_name} - {self.rating}★"

    class Meta:
        ordering = ['-created_at']
