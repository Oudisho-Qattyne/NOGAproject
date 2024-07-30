import django_filters
from .models import *
class WholesalePrice(django_filters.FilterSet):
    wholesale_price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = ['wholesale_price']