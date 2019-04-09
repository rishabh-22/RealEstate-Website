from django import forms
from django.forms import ModelForm
from .models import PropertyImages, Property


class PropertyImagesForm(ModelForm):

    Property_Images = forms.ImageField()

    class Meta:
        model = PropertyImages
        fields = []


class PropertyForm(ModelForm):

    class Meta:
        model = Property
        fields = [
            'property_title',
            'property_address',
            'property_city',
            'property_state',
            'property_pin',
            'property_price',
            'property_bedrooms',
            'property_bathrooms',
            'property_sqFeet',
            'property_lotSize',
            'property_garage',
            'property_description',
        ]
