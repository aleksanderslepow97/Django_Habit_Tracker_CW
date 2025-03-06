from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from habit.models import Habit
from habit.paginations import CustomPagination
from habit.serializers import (HabitpublicitySerializer, HabitSerializer,
                               UserHabitSerializer)
from users.permissions import IsOwner


class HabitViewSet(ModelViewSet):
    """Вьюсет для модели Привычка."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = CustomPagination

    """Метод для управления созданием объекта и автом привязки создаваемого объекта к авторизованному пользователю."""

    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()

    def get_permissions(self):
        """Метод определения действий в зависимости является ли пользователь владельцем."""
        if self.action in ["update", "retrieve"]:
            self.permission_classes = (IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner,)
        return super().get_permissions()


class HabitpublicityListAPIView(ListAPIView):
    """Эндпоинт для списка публичных привычек."""

    serializer_class = HabitpublicitySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """Метод фильтрует привычки по статусу публикации"""
        return Habit.objects.filter(publicity="Опубликована", owner=self.request.user)


class UserhabitListAPIView(ListAPIView):
    """Эндпоинт для списка привычек текущего пользователя."""

    serializer_class = UserHabitSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """Метод фильтрует привычки по текущему пользователю."""
        user = self.request.user
        return Habit.objects.filter(owner=user)
