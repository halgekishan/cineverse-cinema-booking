"""
Run this script to populate the database with sample data:
    python manage.py shell < seed_data.py
OR:
    python seed_data.py  (after setting DJANGO_SETTINGS_MODULE)
"""
import os
import django
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_booking.settings')
django.setup()

from cinema.models import Movie, Hall, ShowTime, Feedback

print("Seeding data...")

# Create Halls
hall1, _ = Hall.objects.get_or_create(name="Hall 1 - Gold Class", defaults={'total_seats': 80, 'rows': 8, 'seats_per_row': 10})
hall2, _ = Hall.objects.get_or_create(name="Hall 2 - Silver Class", defaults={'total_seats': 100, 'rows': 10, 'seats_per_row': 10})
hall3, _ = Hall.objects.get_or_create(name="Hall 3 - IMAX", defaults={'total_seats': 120, 'rows': 10, 'seats_per_row': 12})
print("Halls created.")

# Now-showing movies
movies_now = [
    {
        'title': 'Dune: Part Three',
        'description': 'Paul Atreides continues his epic journey across the desert planet Arrakis in this stunning conclusion to the trilogy. A battle for the fate of the universe begins.',
        'genre': 'Sci-Fi',
        'duration': 155,
        'release_date': date.today() - timedelta(days=10),
        'trailer_url': 'https://www.youtube.com/embed/Way9Dexny3w',
        'status': 'now_showing',
        'rating': 'UA',
        'language': 'English',
        'director': 'Denis Villeneuve',
        'cast': 'Timothée Chalamet, Zendaya, Rebecca Ferguson, Josh Brolin',
    },
    {
        'title': 'The Dark Knight Legacy',
        'description': 'Gotham faces its darkest hour as a new masked villain emerges. Batman must confront ghosts from his past to save the city once more.',
        'genre': 'Action',
        'duration': 148,
        'release_date': date.today() - timedelta(days=5),
        'trailer_url': 'https://www.youtube.com/embed/EXeTwQWrcwY',
        'status': 'now_showing',
        'rating': 'UA',
        'language': 'English',
        'director': 'Christopher Nolan',
        'cast': 'Christian Bale, Tom Hardy, Anne Hathaway',
    },
    {
        'title': 'Kalki 2898 AD - Director\'s Cut',
        'description': 'In a post-apocalyptic future, an ancient prophecy foretells the arrival of Kalki. A warrior rises to fulfill his destiny and save humanity.',
        'genre': 'Action',
        'duration': 185,
        'release_date': date.today() - timedelta(days=3),
        'trailer_url': 'https://www.youtube.com/embed/5ynbGEFNARI',
        'status': 'now_showing',
        'rating': 'UA',
        'language': 'Telugu',
        'director': 'Nag Ashwin',
        'cast': 'Prabhas, Deepika Padukone, Amitabh Bachchan, Kamal Haasan',
    },
    {
        'title': 'Interstellar Returns',
        'description': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival. A breathtaking remaster with new scenes.',
        'genre': 'Sci-Fi',
        'duration': 169,
        'release_date': date.today() - timedelta(days=7),
        'trailer_url': 'https://www.youtube.com/embed/zSWdZVtXT7E',
        'status': 'now_showing',
        'rating': 'U',
        'language': 'English',
        'director': 'Christopher Nolan',
        'cast': 'Matthew McConaughey, Anne Hathaway, Jessica Chastain',
    },
]

# Upcoming movies
movies_upcoming = [
    {
        'title': 'Avatar 3: Fire and Ash',
        'description': 'Jake and Neytiri must explore new regions of Pandora while facing threats from both old enemies and mysterious new forces from the fire clans.',
        'genre': 'Fantasy',
        'duration': 170,
        'release_date': date.today() + timedelta(days=30),
        'trailer_url': 'https://www.youtube.com/embed/placeholder',
        'status': 'upcoming',
        'rating': 'UA',
        'language': 'English',
        'director': 'James Cameron',
        'cast': 'Sam Worthington, Zoe Saldana, Sigourney Weaver',
    },
    {
        'title': 'Pushpa 3: The Wildfire',
        'description': 'Pushpa Raj returns with an even bigger empire and fiercer enemies. The red sandalwood smuggler faces his most dangerous challenge yet.',
        'genre': 'Action',
        'duration': 175,
        'release_date': date.today() + timedelta(days=45),
        'trailer_url': '',
        'status': 'upcoming',
        'rating': 'A',
        'language': 'Telugu',
        'director': 'Sukumar',
        'cast': 'Allu Arjun, Rashmika Mandanna, Fahadh Faasil',
    },
    {
        'title': 'Mission Impossible 9',
        'description': 'Ethan Hunt faces an impossible mission that will test the limits of human endurance and trust. The world hangs in the balance.',
        'genre': 'Thriller',
        'duration': 145,
        'release_date': date.today() + timedelta(days=60),
        'trailer_url': '',
        'status': 'upcoming',
        'rating': 'UA',
        'language': 'English',
        'director': 'Christopher McQuarrie',
        'cast': 'Tom Cruise, Hayley Atwell, Ving Rhames',
    },
]

created_movies = []
for m_data in movies_now + movies_upcoming:
    movie, created = Movie.objects.get_or_create(title=m_data['title'], defaults=m_data)
    if created:
        print(f"  Created movie: {movie.title}")
    created_movies.append(movie)

# Create showtimes for now_showing movies
today = date.today()
show_times = [time(10, 0), time(13, 30), time(17, 0), time(20, 30)]
now_showing_movies = Movie.objects.filter(status='now_showing')

for movie in now_showing_movies:
    for day_offset in range(5):
        show_date = today + timedelta(days=day_offset)
        for t in show_times[:3]:
            hall = hall1 if t == time(20, 30) else hall2
            ShowTime.objects.get_or_create(
                movie=movie,
                show_date=show_date,
                show_time=t,
                defaults={'hall': hall, 'ticket_price': 180.00 if hall == hall1 else 150.00}
            )

print("Showtimes created.")

# Sample feedback
sample_feedbacks = [
    {'customer_name': 'Rahul Sharma', 'customer_email': 'rahul@example.com', 'rating': 5, 'comment': 'Amazing experience! The IMAX screen was breathtaking and the sound was incredible. Will definitely come back!'},
    {'customer_name': 'Priya Patel', 'customer_email': 'priya@example.com', 'rating': 4, 'comment': 'Great movie and comfortable seats. The booking process was very smooth. Loved the popcorn too!'},
    {'customer_name': 'Arun Kumar', 'customer_email': 'arun@example.com', 'rating': 5, 'comment': 'Best cinema in the city! The staff was very helpful and the screen quality is top notch.'},
    {'customer_name': 'Sneha Desai', 'customer_email': 'sneha@example.com', 'rating': 4, 'comment': 'Very clean theatre with excellent facilities. Online seat booking worked perfectly!'},
    {'customer_name': 'Vikram Singh', 'customer_email': 'vikram@example.com', 'rating': 5, 'comment': 'Had a wonderful time watching Dune here. The seats are so comfortable and the picture quality is stunning!'},
]

movie_list = list(Movie.objects.filter(status='now_showing'))
for i, fb_data in enumerate(sample_feedbacks):
    fb_data['movie'] = movie_list[i % len(movie_list)] if movie_list else None
    fb, created = Feedback.objects.get_or_create(
        customer_email=fb_data['customer_email'],
        defaults=fb_data
    )
    if created:
        print(f"  Created feedback from: {fb.customer_name}")

print("\n✅ Seed data created successfully!")
print("📌 Now run: python manage.py createsuperuser")
print("🚀 Then run: python manage.py runserver")
print("🌐 Open: http://127.0.0.1:8000")
