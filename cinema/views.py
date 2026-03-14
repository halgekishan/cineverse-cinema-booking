from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Q
from .models import Movie, ShowTime, Booking, Feedback, Hall
import json
import random
import string


def home(request):
    now_showing = Movie.objects.filter(status='now_showing')[:6]
    upcoming = Movie.objects.filter(status='upcoming')[:6]
    feedbacks = Feedback.objects.filter(is_approved=True)[:6]
    avg_rating = Feedback.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg']
    context = {
        'now_showing': now_showing,
        'upcoming': upcoming,
        'feedbacks': feedbacks,
        'avg_rating': avg_rating,
    }
    return render(request, 'cinema/home.html', context)


def movie_list(request):
    status = request.GET.get('status', 'now_showing')
    genre = request.GET.get('genre', '')
    movies = Movie.objects.filter(status=status)
    if genre:
        movies = movies.filter(genre__icontains=genre)
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    context = {'movies': movies, 'status': status, 'genres': genres, 'selected_genre': genre}
    return render(request, 'cinema/movie_list.html', context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    showtimes = movie.showtimes.filter(show_date__gte=timezone.now().date()).order_by('show_date', 'show_time')
    feedbacks = movie.feedbacks.filter(is_approved=True)
    avg_rating = feedbacks.aggregate(avg=Avg('rating'))['avg']
    context = {
        'movie': movie,
        'showtimes': showtimes,
        'feedbacks': feedbacks,
        'avg_rating': avg_rating,
        'cast_list': [c.strip() for c in movie.cast.split(',')] if movie.cast else [],
    }
    return render(request, 'cinema/movie_detail.html', context)


def book_ticket(request, showtime_id):
    showtime = get_object_or_404(ShowTime, pk=showtime_id)
    booked_seats = showtime.get_booked_seat_numbers()
    all_seats = []
    rows = 'ABCDEFGHIJ'[:showtime.hall.rows]
    for row in rows:
        for num in range(1, showtime.hall.seats_per_row + 1):
            seat = f"{row}{num}"
            all_seats.append({'seat': seat, 'booked': seat in booked_seats})

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        selected_seats = request.POST.getlist('seats')

        if not selected_seats:
            messages.error(request, 'Please select at least one seat.')
            return render(request, 'cinema/book_ticket.html', {
                'showtime': showtime, 'all_seats': all_seats, 'booked_seats': booked_seats,
                'available_count': showtime.available_seats(), 'booked_count': showtime.booked_seats_count(),
            })

        for seat in selected_seats:
            if seat in booked_seats:
                messages.error(request, f'Seat {seat} is already booked. Please select another.')
                return render(request, 'cinema/book_ticket.html', {
                    'showtime': showtime, 'all_seats': all_seats, 'booked_seats': booked_seats,
                    'available_count': showtime.available_seats(), 'booked_count': showtime.booked_seats_count(),
                })

        total = float(showtime.ticket_price) * len(selected_seats)

        # Save booking details in session, redirect to payment
        request.session['pending_booking'] = {
            'showtime_id': showtime_id,
            'customer_name': customer_name,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'selected_seats': selected_seats,
            'total_amount': total,
        }
        return redirect('payment', showtime_id=showtime_id)

    context = {
        'showtime': showtime,
        'all_seats': all_seats,
        'booked_seats': booked_seats,
        'available_count': showtime.available_seats(),
        'booked_count': showtime.booked_seats_count(),
    }
    return render(request, 'cinema/book_ticket.html', context)


def payment(request, showtime_id):
    showtime = get_object_or_404(ShowTime, pk=showtime_id)
    pending = request.session.get('pending_booking')

    if not pending or pending.get('showtime_id') != showtime_id:
        messages.error(request, 'Session expired. Please start your booking again.')
        return redirect('book_ticket', showtime_id=showtime_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'counter')

        # Simulate payment processing
        payment_status = 'paid'
        transaction_id = None

        if payment_method == 'upi':
            upi_id = request.POST.get('upi_id', '').strip()
            if not upi_id:
                messages.error(request, 'Please enter your UPI ID.')
                return render(request, 'cinema/payment.html', {'showtime': showtime, 'pending': pending})
            transaction_id = 'UPI' + ''.join(random.choices(string.digits, k=10))

        elif payment_method == 'card':
            card_number = request.POST.get('card_number', '').replace(' ', '')
            card_expiry = request.POST.get('card_expiry', '')
            card_cvv = request.POST.get('card_cvv', '')
            card_name = request.POST.get('card_name', '')
            if not all([card_number, card_expiry, card_cvv, card_name]):
                messages.error(request, 'Please fill in all card details.')
                return render(request, 'cinema/payment.html', {'showtime': showtime, 'pending': pending})
            if len(card_number) < 16:
                messages.error(request, 'Invalid card number.')
                return render(request, 'cinema/payment.html', {'showtime': showtime, 'pending': pending})
            transaction_id = 'CARD' + ''.join(random.choices(string.digits, k=10))

        elif payment_method == 'netbanking':
            bank = request.POST.get('bank', '')
            if not bank:
                messages.error(request, 'Please select your bank.')
                return render(request, 'cinema/payment.html', {'showtime': showtime, 'pending': pending})
            transaction_id = 'NET' + ''.join(random.choices(string.digits, k=10))

        elif payment_method == 'counter':
            payment_status = 'pending'
            transaction_id = None

        # Create the booking
        booking = Booking.objects.create(
            showtime=showtime,
            customer_name=pending['customer_name'],
            customer_email=pending['customer_email'],
            customer_phone=pending['customer_phone'],
            num_seats=len(pending['selected_seats']),
            seat_numbers=','.join(pending['selected_seats']),
            total_amount=pending['total_amount'],
            payment_method=payment_method,
            payment_status=payment_status,
            transaction_id=transaction_id,
            status='confirmed',
        )

        # Clear session
        del request.session['pending_booking']

        messages.success(request, f'Booking confirmed! Reference: {booking.booking_reference}')
        return redirect('booking_confirmation', booking_id=booking.pk)

    return render(request, 'cinema/payment.html', {'showtime': showtime, 'pending': pending})


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    seats = [s.strip() for s in booking.seat_numbers.split(',')]
    context = {'booking': booking, 'seats': seats}
    return render(request, 'cinema/booking_confirmation.html', context)


def check_booking(request):
    booking = None
    if request.method == 'POST':
        ref = request.POST.get('reference', '').strip()
        try:
            booking = Booking.objects.get(booking_reference=ref)
        except Booking.DoesNotExist:
            messages.error(request, 'No booking found with that reference number.')
    return render(request, 'cinema/check_booking.html', {'booking': booking})


def upcoming_movies(request):
    movies = Movie.objects.filter(status='upcoming').order_by('release_date')
    return render(request, 'cinema/upcoming.html', {'movies': movies})


def feedback(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        movie = Movie.objects.filter(pk=movie_id).first() if movie_id else None
        Feedback.objects.create(
            movie=movie,
            customer_name=request.POST.get('customer_name'),
            customer_email=request.POST.get('customer_email'),
            rating=request.POST.get('rating', 5),
            comment=request.POST.get('comment'),
        )
        messages.success(request, 'Thank you for your feedback!')
        return redirect('feedback')

    movies = Movie.objects.filter(status='now_showing')
    feedbacks = Feedback.objects.filter(is_approved=True)
    avg_rating = feedbacks.aggregate(avg=Avg('rating'))['avg']
    context = {'movies': movies, 'feedbacks': feedbacks, 'avg_rating': avg_rating}
    return render(request, 'cinema/feedback.html', context)

    now_showing = Movie.objects.filter(status='now_showing')[:6]
    upcoming = Movie.objects.filter(status='upcoming')[:6]
    feedbacks = Feedback.objects.filter(is_approved=True)[:6]
    avg_rating = Feedback.objects.filter(is_approved=True).aggregate(avg=Avg('rating'))['avg']
    context = {
        'now_showing': now_showing,
        'upcoming': upcoming,
        'feedbacks': feedbacks,
        'avg_rating': avg_rating,
    }
    return render(request, 'cinema/home.html', context)


def movie_list(request):
    status = request.GET.get('status', 'now_showing')
    genre = request.GET.get('genre', '')
    movies = Movie.objects.filter(status=status)
    if genre:
        movies = movies.filter(genre__icontains=genre)
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    context = {'movies': movies, 'status': status, 'genres': genres, 'selected_genre': genre}
    return render(request, 'cinema/movie_list.html', context)


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    showtimes = movie.showtimes.filter(show_date__gte=timezone.now().date()).order_by('show_date', 'show_time')
    feedbacks = movie.feedbacks.filter(is_approved=True)
    avg_rating = feedbacks.aggregate(avg=Avg('rating'))['avg']
    context = {
        'movie': movie,
        'showtimes': showtimes,
        'feedbacks': feedbacks,
        'avg_rating': avg_rating,
        'cast_list': [c.strip() for c in movie.cast.split(',')] if movie.cast else [],
    }
    return render(request, 'cinema/movie_detail.html', context)


def book_ticket(request, showtime_id):
    showtime = get_object_or_404(ShowTime, pk=showtime_id)
    booked_seats = showtime.get_booked_seat_numbers()
    all_seats = []
    rows = 'ABCDEFGHIJ'[:showtime.hall.rows]
    for row in rows:
        for num in range(1, showtime.hall.seats_per_row + 1):
            seat = f"{row}{num}"
            all_seats.append({'seat': seat, 'booked': seat in booked_seats})

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        selected_seats = request.POST.getlist('seats')

        if not selected_seats:
            messages.error(request, 'Please select at least one seat.')
            return render(request, 'cinema/book_ticket.html', {
                'showtime': showtime, 'all_seats': all_seats, 'booked_seats': booked_seats
            })

        # Check if seats are still available
        for seat in selected_seats:
            if seat in booked_seats:
                messages.error(request, f'Seat {seat} is already booked. Please select another seat.')
                return render(request, 'cinema/book_ticket.html', {
                    'showtime': showtime, 'all_seats': all_seats, 'booked_seats': booked_seats
                })

        total = showtime.ticket_price * len(selected_seats)
        booking = Booking.objects.create(
            showtime=showtime,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            num_seats=len(selected_seats),
            seat_numbers=','.join(selected_seats),
            total_amount=total,
        )
        messages.success(request, f'Booking confirmed! Reference: {booking.booking_reference}')
        return redirect('booking_confirmation', booking_id=booking.pk)

    context = {
        'showtime': showtime,
        'all_seats': all_seats,
        'booked_seats': booked_seats,
        'available_count': showtime.available_seats(),
        'booked_count': showtime.booked_seats_count(),
    }
    return render(request, 'cinema/book_ticket.html', context)


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    seats = [s.strip() for s in booking.seat_numbers.split(',')]
    context = {'booking': booking, 'seats': seats}
    return render(request, 'cinema/booking_confirmation.html', context)


def check_booking(request):
    booking = None
    if request.method == 'POST':
        ref = request.POST.get('reference', '').strip()
        try:
            booking = Booking.objects.get(booking_reference=ref)
        except Booking.DoesNotExist:
            messages.error(request, 'No booking found with that reference number.')
    return render(request, 'cinema/check_booking.html', {'booking': booking})


def upcoming_movies(request):
    movies = Movie.objects.filter(status='upcoming').order_by('release_date')
    return render(request, 'cinema/upcoming.html', {'movies': movies})


def feedback(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie')
        movie = Movie.objects.filter(pk=movie_id).first() if movie_id else None
        Feedback.objects.create(
            movie=movie,
            customer_name=request.POST.get('customer_name'),
            customer_email=request.POST.get('customer_email'),
            rating=request.POST.get('rating', 5),
            comment=request.POST.get('comment'),
        )
        messages.success(request, 'Thank you for your feedback!')
        return redirect('feedback')

    movies = Movie.objects.filter(status='now_showing')
    feedbacks = Feedback.objects.filter(is_approved=True)
    avg_rating = feedbacks.aggregate(avg=Avg('rating'))['avg']
    context = {'movies': movies, 'feedbacks': feedbacks, 'avg_rating': avg_rating}
    return render(request, 'cinema/feedback.html', context)
