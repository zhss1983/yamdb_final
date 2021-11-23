from django.shortcuts import get_object_or_404

from reviews.models import Title


class GetDefault:
    """Базовый класс для получения значений по умолчанию"""
    requires_context = True

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class GetTitle(GetDefault):
    """Гарантированно возвращает Title по id из URL или 404 код"""
    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)


class GetReview(GetDefault):
    """Гарантированно возвращает Review по id из URL или 404 код"""
    def __call__(self, serializer_field):
        title = GetTitle()(serializer_field)
        review_id = serializer_field.context['view'].kwargs.get('review_id')
        return get_object_or_404(title.reviews, pk=review_id)
