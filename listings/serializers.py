from rest_framework import serializers
from .models import Listing, Booking
from datetime import date


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'title', 'description', 'location', 'price_per_night', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'listing', 'guest_name', 'guest_email', 'start_date', 'end_date', 'total_price', 'created_at']
        read_only_fields = ['total_price', 'created_at']

    def validate(self, attrs):
        # Handle both create and update (partial) cases
        start = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        end = attrs.get('end_date', getattr(self.instance, 'end_date', None))
        if start and end and start >= end:
            raise serializers.ValidationError({'end_date': 'end_date must be after start_date'})
        if start and start < date.today():
            raise serializers.ValidationError({'start_date': 'start_date cannot be in the past'})
        return attrs
