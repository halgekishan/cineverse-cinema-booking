# 🎬 CineVerse - Cinema Ticket Booking System

A full-featured cinema ticket booking web application built with **Python**, **Django**, **SQLite**, **HTML** and **CSS**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎟️ **Ticket Booking** | Select movie, showtime, seats and book tickets |
| 📅 **Upcoming Cinema** | Browse movies releasing soon with trailers |
| 💺 **Seat Map** | Interactive visual seat selector — see booked & available seats live |
| 🎬 **Movie Trailers** | Watch embedded YouTube trailers on the movie detail page |
| ⭐ **Customer Feedback** | Star-rating system with reviews per movie |
| 🔍 **Booking Lookup** | Retrieve booking by reference number |
| 🛠️ **Admin Panel** | Full Django admin for managing movies, halls, bookings |

---

## 🚀 Quick Setup

### Step 1 — Install Python
Make sure Python 3.9+ is installed: https://www.python.org/downloads/

### Step 2 — Install dependencies
```bash
cd cinema_project
pip install -r requirements.txt
```

### Step 3 — Set up the database
```bash
python manage.py makemigrations cinema
python manage.py migrate
```

### Step 4 — Load sample data (movies, halls, showtimes, feedback)
```bash
python seed_data.py
```

### Step 5 — Create admin account
```bash
python manage.py createsuperuser
```

### Step 6 — Run the server
```bash
python manage.py runserver
```

### Step 7 — Open in browser
- **Website:** http://127.0.0.1:8000
- **Admin Panel:** http://127.0.0.1:8000/admin

---

## 📁 Project Structure

```
cinema_project/
├── cinema_booking/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── cinema/                  # Main application
│   ├── models.py            # Movie, Hall, ShowTime, Booking, Feedback
│   ├── views.py             # All page views
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin panel config
│   └── templates/cinema/    # HTML templates
│       ├── base.html        # Base layout
│       ├── home.html        # Homepage
│       ├── movie_list.html  # Movie listing
│       ├── movie_detail.html # Movie detail + trailer + showtimes
│       ├── book_ticket.html  # Interactive seat booking
│       ├── booking_confirmation.html
│       ├── upcoming.html    # Upcoming movies
│       ├── feedback.html    # Customer reviews
│       └── check_booking.html
├── media/                   # Uploaded poster images
├── seed_data.py             # Sample data loader
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🎭 Database Models

- **Movie** — title, description, genre, duration, poster, trailer_url, status, language, cast
- **Hall** — name, total_seats, rows, seats_per_row
- **ShowTime** — movie + hall + date + time + price
- **Booking** — customer info, seat numbers, reference code, status
- **Feedback** — customer rating (1–5 stars) + comment + movie link

---

## 🖼️ Adding Movie Posters

1. Go to Admin Panel → Movies → Edit Movie
2. Upload a poster image (JPG/PNG, 2:3 aspect ratio recommended)
3. Add a YouTube embed URL for the trailer (format: `https://www.youtube.com/embed/VIDEO_ID`)

---

## 🛠️ Tech Stack

| Technology | Usage |
|---|---|
| Python 3.9+ | Backend language |
| Django 4.2 | Web framework |
| SQLite | Database |
| HTML5 + CSS3 | Templates |
| JavaScript | Interactive seat map |
| Font Awesome | Icons |
| Google Fonts | Typography (Bebas Neue, Rajdhani) |
