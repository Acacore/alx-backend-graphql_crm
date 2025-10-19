# crm/filters.py

import django_filters
from django.db.models import Q
from .models import Customer, Product, Order


# -----------------------------
# Customer Filter
# -----------------------------
class CustomerFilter(django_filters.FilterSet):
    # Case-insensitive partial match for name
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # Case-insensitive partial match for email
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')

    # Date range filters
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    # Custom filter for phone numbers that start with a specific pattern (e.g., "+1")
    phone_starts_with = django_filters.CharFilter(method='filter_phone_starts_with')

    def filter_phone_starts_with(self, queryset, name, value):
        # This method filters phone numbers that start with the given value (like "+1")
        return queryset.filter(phone__startswith=value)

    class Meta:
        model = Customer
        # Only fields explicitly declared will be used
        fields = []


# -----------------------------
# Product Filter
# -----------------------------
class ProductFilter(django_filters.FilterSet):
    # Case-insensitive partial match for name
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # Range filter for price
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # Exact or range filters for stock
    stock = django_filters.NumberFilter(field_name='stock', lookup_expr='exact')
    stock__gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock__lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')

    # Custom filter: products with low stock (e.g., stock < 10)
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')

    def filter_low_stock(self, queryset, name, value):
        # If true, filter products where stock is less than 10
        if value:
            return queryset.filter(stock__lt=10)
        return queryset

    class Meta:
        model = Product
        fields = []


# -----------------------------
# Order Filter
# -----------------------------
class OrderFilter(django_filters.FilterSet):
    # Range filter for total amount
    total_amount__gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount__lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')

    # Date range filter for order_date
    order_date__gte = django_filters.DateFilter(field_name='order_date', lookup_expr='gte')
    order_date__lte = django_filters.DateFilter(field_name='order_date', lookup_expr='lte')

    # Filter by customer's name (case-insensitive partial match using related field)
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')

    # Filter by product's name (case-insensitive partial match using related field)
    product_name = django_filters.CharFilter(method='filter_product_name')

    def filter_product_name(self, queryset, name, value):
        # Join through the related products and filter using icontains
        return queryset.filter(products__name__icontains=value).distinct()

    # Challenge: Filter orders that include a specific product ID
    product_id = django_filters.NumberFilter(method='filter_by_product_id')

    def filter_by_product_id(self, queryset, name, value):
        return queryset.filter(products__id=value).distinct()

    class Meta:
        model = Order
        fields = []
