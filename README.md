# alx_travel_app_0x01

Django REST API for managing Listings and Bookings with Swagger documentation.

## Tech
- Django, Django REST Framework
- drf-yasg for Swagger
- SQLite by default

## Quickstart
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install django djangorestframework drf-yasg
python manage.py migrate
python manage.py runserver
```

- API base: `http://127.0.0.1:8000/api/`
  - Listings: `/api/listings/`
  - Bookings: `/api/bookings/`
- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`

## Endpoints
- `GET /api/listings/`
- `POST /api/listings/`
- `GET /api/listings/{id}/`
- `PUT/PATCH /api/listings/{id}/`
- `DELETE /api/listings/{id}/`

- `GET /api/bookings/`
- `POST /api/bookings/`
- `GET /api/bookings/{id}/`
- `PUT/PATCH /api/bookings/{id}/`
- `DELETE /api/bookings/{id}/`

## Testing
```powershell
python manage.py test
```

## Notes
- `Booking.total_price` is computed: nights × listing.price_per_night.
- Validation ensures `end_date` is after `start_date` and start date is not in the past.
