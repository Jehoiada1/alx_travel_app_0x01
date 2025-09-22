from django.contrib import admin
from .models import Listing, Booking


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'location', 'price_per_night', 'created_at')
	search_fields = ('title', 'location')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
	list_display = ('id', 'listing', 'guest_name', 'start_date', 'end_date', 'total_price', 'created_at')
	list_filter = ('start_date', 'end_date')
	search_fields = ('guest_name', 'guest_email')

# Register your models here.
