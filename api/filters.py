from django_filters import FilterSet
from django_filters.filters import CharFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр для модели Title по "name", "year", "genre", "category"."""
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(field_name='name', lookup_expr='startswith')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')
