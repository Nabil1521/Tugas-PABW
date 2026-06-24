# Django Migration to Complete Guide

## What Changed

Your web service has been successfully converted from **Flask** to **Django**:

### Server Changes

- **Framework**: Flask → Django
- **Database ORM**: Peewee → Django ORM
- **API Framework**: Flask-RESTful → Django REST Framework (DRF)
- **Project Structure**:
  - New: `manage.py` (Django management script)
  - New: `carsweb_project/` (Django project settings)
  - New: `api/` (Django app for REST API)
  - Removed: `carsweb-server.py` (Old Flask file)

### Client Changes

- **Framework**: Flask → Django
- **Project Structure**:
  - New: `manage.py` (Django management script)
  - New: `carsweb_client_project/` (Django project settings)
  - New: `web/` (Django app for web interface)
  - Updated: Templates remain the same (mostly compatible)
  - Updated: Static files configuration
  - Removed: `carsweb-client.py` (Old Flask file)

### API Endpoints (Unchanged)

All API endpoints remain the same:

- `GET /` - Server status
- `GET /read` - Read all cars
- `GET /cars/` - List all cars (same as `/read`)
- `POST /cars/` - Create a car
- `PUT /cars/` - Update a car
- `DELETE /cars/` - Delete a car
- `GET /search/<searchkey>` - Search cars

## Setup Instructions

### Prerequisites

- Python 3.8+
- Virtual environment activated (if not, run: `python -m venv .venv && .venv\Scripts\activate`)

### Server Setup

1. Navigate to the server directory:

   ```bash
   cd server
   ```

2. Install dependencies:

   ```bash
   pip install -r req-server.txt
   ```

3. Create database tables:

   ```bash
   python manage.py migrate
   ```

4. Run the server:

   ```bash
   python manage.py runserver 0.0.0.0:5012
   ```

   Server will be available at: `http://localhost:5012`

### Client Setup

1. Open a new terminal and navigate to the client directory:

   ```bash
   cd client
   ```

2. Install dependencies:

   ```bash
   pip install -r req-client.txt
   ```

3. Create database tables (if needed):

   ```bash
   python manage.py migrate
   ```

4. Run the client:

   ```bash
   python manage.py runserver 0.0.0.0:5011
   ```

   Client will be available at: `http://localhost:5011`

## Running Both Services

### Option 1: Two Terminal Windows

- Terminal 1 (Server): `cd server && python manage.py runserver 0.0.0.0:5012`
- Terminal 2 (Client): `cd client && python manage.py runserver 0.0.0.0:5011`

### Option 2: Using Setup Scripts (Windows)

- Server: `cd server && setup_server.bat` then `python manage.py runserver 0.0.0.0:5012`
- Client: `cd client && setup_client.bat` then `python manage.py runserver 0.0.0.0:5011`

### Option 3: Using Setup Scripts (Linux/Mac)

- Server: `cd server && bash setup_server.sh` then `python manage.py runserver 0.0.0.0:5012`
- Client: `cd client && bash setup_client.sh` then `python manage.py runserver 0.0.0.0:5011`

## Key Improvements with Django

1. **Better ORM**: Django ORM is more powerful and integrated with the framework
2. **Built-in Admin**: Django admin panel available at `/admin` (set up superuser with `python manage.py createsuperuser`)
3. **Better Security**: CSRF protection, SQL injection prevention, etc.
4. **Scalability**: Django is better suited for larger applications
5. **Documentation**: Extensive Django documentation and community support
6. **Testing**: Built-in testing framework
7. **Migrations**: Proper database migration system

## Troubleshooting

### Issue: "No module named 'django'"

- Solution: Run `pip install -r req-server.txt` (for server) or `pip install -r req-client.txt` (for client)

### Issue: Database errors

- Solution: Run `python manage.py migrate` to create tables

### Issue: Port already in use

- Change the port number in the run command, e.g.: `python manage.py runserver 0.0.0.0:8000`

### Issue: CORS errors (client can't reach server)

- Ensure the server is running on port 5012
- Check `carsweb_client_project/settings.py` has correct `API_SERVER_URL`
- Ensure server's `carsweb_project/settings.py` has CORS enabled for client port

## Old Files

The old Flask files have been preserved in the repository. You can safely delete them if you don't need them:

- `server/carsweb-server.py`
- `client/carsweb-client.py`
