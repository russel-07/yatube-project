from django_filters.rest_framework import FilterSet, DateFilter
from posts.models import Post

class DateRangeFilter(FilterSet):
    date_from = DateFilter(field_name="pub_date", lookup_expr='gte')
    date_to = DateFilter(field_name="pub_date", lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['date_from', 'date_to']