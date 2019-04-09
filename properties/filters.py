import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    # price = django_filters.NumberFilter()
    # price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    # price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Property
        fields = {
            'property_title': ['icontains', ],
            'property_city': ['exact', ],
            # 'property_state': ['exact', ],
            'property_bedrooms': ['exact', ],
            'property_bathrooms': ['exact', ],
            'property_garage': ['exact', ],
        }
