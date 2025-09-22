from datetime import date, timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Listing


class ListingsApiTests(APITestCase):
	def setUp(self):
		self.listing = Listing.objects.create(
			title="Cozy Cabin",
			description="A nice place",
			location="Lakeview",
			price_per_night=100
		)

	def test_listings_crud(self):
		# List
		url = reverse('listing-list')
		res = self.client.get(url)
		self.assertEqual(res.status_code, status.HTTP_200_OK)

		# Create
		payload = {
			"title": "City Loft",
			"description": "Modern loft",
			"location": "Downtown",
			"price_per_night": "150.00"
		}
		res = self.client.post(url, payload, format='json')
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		listing_id = res.data['id']

		# Retrieve
		res = self.client.get(reverse('listing-detail', args=[listing_id]))
		self.assertEqual(res.status_code, status.HTTP_200_OK)

		# Update
		res = self.client.patch(reverse('listing-detail', args=[listing_id]), {"location": "Uptown"}, format='json')
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(res.data['location'], "Uptown")

		# Delete
		res = self.client.delete(reverse('listing-detail', args=[listing_id]))
		self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

	def test_bookings_crud_and_validation(self):
		# Create a booking
		url = reverse('booking-list')
		start = date.today() + timedelta(days=2)
		end = start + timedelta(days=3)
		payload = {
			"listing": self.listing.id,
			"guest_name": "Alice",
			"guest_email": "alice@example.com",
			"start_date": start.isoformat(),
			"end_date": end.isoformat()
		}
		res = self.client.post(url, payload, format='json')
		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		booking_id = res.data['id']
		self.assertEqual(str(res.data['total_price']), "300.00")

		# Retrieve
		res = self.client.get(reverse('booking-detail', args=[booking_id]))
		self.assertEqual(res.status_code, status.HTTP_200_OK)

		# Update dates
		new_end = end + timedelta(days=1)
		res = self.client.patch(reverse('booking-detail', args=[booking_id]), {"end_date": new_end.isoformat()}, format='json')
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(str(res.data['total_price']), "400.00")

		# Delete
		res = self.client.delete(reverse('booking-detail', args=[booking_id]))
		self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

		# Invalid booking: same day
		invalid_payload = {
			"listing": self.listing.id,
			"guest_name": "Bob",
			"guest_email": "bob@example.com",
			"start_date": start.isoformat(),
			"end_date": start.isoformat()
		}
		res = self.client.post(url, invalid_payload, format='json')
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

# Create your tests here.
