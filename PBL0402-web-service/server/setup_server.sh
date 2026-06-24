#!/bin/bash
# Django Server Setup Script

echo "Installing Django server dependencies..."
pip install -r req-server.txt

echo ""
echo "Migrating database..."
python manage.py migrate

echo ""
echo "Server setup complete!"
echo "To run the server, execute: python manage.py runserver 0.0.0.0:5012"
