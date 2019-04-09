from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Property(models.Model):
    property_owner = models.ForeignKey(User, related_name='property_owner', on_delete=models.CASCADE)
    property_title = models.CharField(max_length=50)
    property_address = models.CharField(max_length=200)
    PROPERTY_CITY_CHOICES = (
        ('New Delhi', 'New Delhi'),
        ('Noida', 'Noida'),
        ('Gurugram', 'Gurugram'),
        ('Chandigarh', 'Chandigarh'),
        ('Bangalore', 'Bangalore'),
        ('Pune', 'Pune'),
        ('Mumbai', 'Mumbai'),
        ('Chennai', 'Chennai'),
    )
    PROPERTY_STATE_CHOICES = (
        ('Delhi', 'Delhi'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Haryana', 'Haryana'),
        ('Punjab', 'Punjab'),
        ('Karnataka', 'Karnataka'),
        ('Maharashtra', 'Maharashtra'),
        ('Tamil Nadu', 'Tamil Nadu'),
    )
    property_city = models.CharField(max_length=50, choices=PROPERTY_CITY_CHOICES)
    property_state = models.CharField(max_length=50, choices=PROPERTY_STATE_CHOICES)
    property_pin = models.IntegerField()
    property_price = models.IntegerField()
    property_bedrooms = models.IntegerField()
    property_bathrooms = models.IntegerField()
    property_sqFeet = models.IntegerField()
    property_lotSize = models.IntegerField()
    property_garage = models.IntegerField()
    property_listingDate = models.DateField(auto_now_add=True)
    property_description = models.CharField(max_length=200)


class PropertyImages(models.Model):
    property_name = models.ForeignKey(Property, related_name='property_name', on_delete=models.CASCADE)
    property_image = models.ImageField(upload_to='property/')


class Enquiry(models.Model):
    property = models.ForeignKey(Property, related_name='property', on_delete=models.CASCADE)
    requester = models.ForeignKey(User, related_name='requester', on_delete=models.CASCADE)
    enquiry_text = models.TextField(max_length=200)
    enquiry_date = models.DateField(auto_now_add=True)
