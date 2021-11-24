from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title

from .filters import TitleFilter
from .mixins import CategoryGenreViewSet
from .permissions import AdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializerEdit, TitleSerializerSafe)
from .viewsets import GetReviewBaseViewSet, GetTitleBaseViewSet


class ReviewViewSet(GetTitleBaseViewSet):
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()


class CommentViewSet(GetReviewBaseViewSet):
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action in ['post', 'create', 'partial_update']:
            return TitleSerializerEdit
        return TitleSerializerSafe


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
