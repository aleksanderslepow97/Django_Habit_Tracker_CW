from django.utils import timezone
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomsUser
from users.serializers import CustomsUserSerializer


class CustomsUserViewSet(viewsets.ModelViewSet):
    queryset = CustomsUser.objects.all()
    serializer_class = CustomsUserSerializer


class CustomsUserCreateAPIView(CreateAPIView):
    serializer_class = CustomsUserSerializer
    queryset = CustomsUser.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Сохранение пользователя с активным статусом
        user = serializer.save(is_active=True)
        user.set_password(user.password)  # Хеширование пароля
        user.save()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if request.user.is_authenticated:
            request.user.last_login = timezone.now()  # Обновление времени последнего входа
            request.user.save()
        return response
