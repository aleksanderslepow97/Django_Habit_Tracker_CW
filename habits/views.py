from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsOwnerOrReadOnly

from .models import Habit
from .paginations import HabitPagination
from .serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        if self.request.query_params.get("public"):
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"all": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"], url_path="public")
    def list_public(self, request):
        """Вывод только публичных привычек."""
        public_habits = Habit.objects.filter(is_public=True)
        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
