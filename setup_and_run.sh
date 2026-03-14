#!/bin/bash
# ============================================================
#  CineVerse Cinema Booking System - Setup Script
# ============================================================

echo ""
echo "  ██████╗██╗███╗   ██╗███████╗██╗   ██╗███████╗██████╗ ███████╗███████╗"
echo " ██╔════╝██║████╗  ██║██╔════╝██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝"
echo " ██║     ██║██╔██╗ ██║█████╗  ██║   ██║█████╗  ██████╔╝███████╗█████╗  "
echo " ██║     ██║██║╚██╗██║██╔══╝  ╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝  "
echo " ╚██████╗██║██║ ╚████║███████╗ ╚████╔╝ ███████╗██║  ██║███████║███████╗"
echo "  ╚═════╝╚═╝╚═╝  ╚═══╝╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝"
echo ""
echo "  Cinema Ticket Booking System"
echo "============================================================"
echo ""

# Install requirements
echo "[1/5] Installing dependencies..."
pip install django pillow

# Make migrations
echo ""
echo "[2/5] Setting up database..."
python manage.py makemigrations cinema
python manage.py migrate

# Seed data
echo ""
echo "[3/5] Loading sample data..."
python seed_data.py

# Create superuser
echo ""
echo "[4/5] Create admin account (for /admin panel):"
python manage.py createsuperuser

# Run server
echo ""
echo "[5/5] Starting development server..."
echo ""
echo "  ✅ Open http://127.0.0.1:8000 in your browser"
echo "  ✅ Admin panel: http://127.0.0.1:8000/admin"
echo ""
python manage.py runserver
