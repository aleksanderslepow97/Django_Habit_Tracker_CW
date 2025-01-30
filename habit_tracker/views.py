from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from habit_tracker.models import Habit
from habit_tracker.paginators import HabitPaginator
from habit_tracker.serializers import HabitSerializer
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(operation_description="Контроллер для получения списка всех привычек"),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(operation_description="Контроллер для получения конкретной привычки"),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(operation_description="Контроллер для создания привычки"),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(operation_description="Контроллер для обновления информации о привычке"),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(operation_description="Контроллер для частичного изменения информации о привычке"),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(operation_description="Контроллер для удаления привычки"),
)
class HabitViewSet(viewsets.ModelViewSet):
    """CRUD привычек."""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = HabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        habit = serializer.save(owner=self.request.user)
        habit.save()

    def get_permissions(self):
        if self.action != "create":
            self.permission_classes = [IsOwner]
        return super().get_permissions()


class PublicHabitListAPIView(generics.ListAPIView):
    """Контроллер для вывода списка публичных привычек."""

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPaginator
