from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Listing(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	location = models.CharField(max_length=200)
	price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.title} - {self.location}"


class Booking(models.Model):
	listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
	guest_name = models.CharField(max_length=200)
	guest_email = models.EmailField()
	start_date = models.DateField()
	end_date = models.DateField()
	total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def clean(self):
		if self.start_date >= self.end_date:
			raise ValidationError("end_date must be after start_date")
		if self.start_date < timezone.now().date():
			# Prevent past bookings (adjust as needed)
			raise ValidationError("start_date cannot be in the past")

	def save(self, *args, **kwargs):
		self.clean()
		nights = (self.end_date - self.start_date).days
		self.total_price = self.listing.price_per_night * nights
		super().save(*args, **kwargs)

	def __str__(self):
		return f"Booking for {self.listing} ({self.start_date} to {self.end_date})"

# Create your models here.
