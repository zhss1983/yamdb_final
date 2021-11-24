from django.shortcuts import get_object_or_404

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from reviews.models import Title

from .permissions import EditAccessOrReadOnly


class GetTitleBaseViewSet(ModelViewSet):
    permission_classes = (EditAccessOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)


class GetReviewBaseViewSet(GetTitleBaseViewSet):

    def get_review(self):
        title = self.get_title()
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(title.reviews, pk=review_id)
