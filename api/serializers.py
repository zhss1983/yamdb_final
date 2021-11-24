from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        SlugRelatedField)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title

from .getdefault import GetReview, GetTitle


class CommentSerializer(ModelSerializer):
    review = serializers.HiddenField(default=GetReview())
    author = SlugRelatedField(
        slug_field='username', read_only=True, default=CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        model = Comment
        read_only_fields = ('id', )


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class CategorySerializer(GenreSerializer):
    class Meta(GenreSerializer.Meta):
        model = Category


class ReviewSerializer(ModelSerializer):
    SCORE_ERROR = 'Оценка должна быть числом целым в диапазоне от 0 до 10.'

    author = SlugRelatedField(
        slug_field='username', read_only=True, default=CurrentUserDefault())
    title = serializers.HiddenField(default=GetTitle())

    class Meta:
        UNIQUE_ERROR = 'Одно произведение, один отзыв, не более.'
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        read_only_fields = ('id', 'author', )
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message=UNIQUE_ERROR
            ),
        )

    def validate_score(self, value):
        if not (isinstance(value, int) and 0 <= value <= 10):
            raise ValidationError(self.SCORE_ERROR)
        return value


class TitleSerializerEdit(ModelSerializer):
    genre = SlugRelatedField(
        many=True, slug_field='slug', queryset=Genre.objects.all())
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        read_only_fields = ('id',)


class TitleSerializerSafe(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True, many=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'genre', 'category')
        read_only_fields = ('id', 'rating', 'genre', 'category')
