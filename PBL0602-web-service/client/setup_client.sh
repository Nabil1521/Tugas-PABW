#!/bin/bash
# Django Client Setup Script

echo "Installing Django client dependencies..."
pip install -r req-client.txt

echo ""
echo "Migrating database..."
python manage.py migrate

echo ""
echo "Client setup complete!"
echo "To run the client, execute: python manage.py runserver 0.0.0.0:5011"
