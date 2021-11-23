from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from .permissions import AdminOrReadOnly


class CategoryGenreViewSet(CreateModelMixin, DestroyModelMixin,
                           ListModelMixin, GenericViewSet):
    """Базовый ViewSet класс для GenreViewSet и CategoryViewSet"""
    permission_classes = (AdminOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('=name',)
    lookup_field = 'slug'
