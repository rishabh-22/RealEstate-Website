from django.db import models

# Create your models here.


class Property(models.Model):
    property_title = models.CharField(max_length=50, required=True)
    property_address = models.CharField(max_length=200)
    property_city = (
        ('New Delhi', 'New Delhi'),
        ('Noida', 'Noida'),
        ('Gurugram', 'Gurugram'),
        ('Chandigarh', 'Chandigarh'),
        ('Bangalore', 'Bangalore'),
        ('Pune', 'Pune'),
        ('Mumbai', 'Mumbai'),
        ('Chennai', 'Chennai'),
    )
    property_state = (
        ('Delhi', 'Delhi'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Haryana', 'Haryana'),
        ('Punjab', 'Punjab'),
        ('Karnataka', 'Karnataka'),
        ('Maharashtra', 'Maharashtra'),
        ('Tamil Nadu', 'Tamil Nadu'),
    )
    property_pin = models.IntegerField()
    property_price = models.IntegerField()
    property_bedrooms = models.IntegerField()
    property_bathrooms = models.IntegerField()
    property_sqFeet = models.IntegerField()
    property_lotSize = models.IntegerField()
    property_garage = models.IntegerField()
    property_listingDate = models.DateField(auto_now_add=True)
    property_description = models.CharField(max_length=200)