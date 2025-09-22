from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from listings.models import Listing, Booking
from listings.serializers import ListingSerializer, BookingSerializer


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('listing').all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]
