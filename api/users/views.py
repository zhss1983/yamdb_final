from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdmin
from .serializers import (UserRegistrationSerializer, UserSerializer,
                          YAMDBTokenObtainPairSerializer)


class UserRegistrationViewSet(generics.CreateAPIView):
    """Вьюсет для регистрации новых пользователей."""
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response


class YAMBDTokenObtainPairView(TokenObtainPairView):
    """Вьюсет для получения токена. Наследуется от
    вьюсета из Simple JWT.
    """
    serializer_class = YAMDBTokenObtainPairSerializer
    permission_classes = (permissions.AllowAny, )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для операций CRUD с ролью
    администратора, и для CRU только своих учетных
    записей прочими пользователем.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    queryset = User.objects.all()

    @action(detail=False,
            permission_classes=[permissions.IsAuthenticated],
            methods=['PATCH', 'GET'])
    def me(self, request, *args, **kwargs):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            if (self.request.user.not_admin
                    and 'role' in serializer.validated_data):
                serializer.validated_data.pop('role')
            serializer.save()
        return Response(serializer.data)
