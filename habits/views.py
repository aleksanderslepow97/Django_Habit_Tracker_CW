from rest_framework import generics
from .models import Habit
from .serializers import HabitSerializer
from .pagination import FiveItemsPaginator
from users.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from .services import send_telegram_message


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание"""
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Редактирование"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Одна привычка"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        print(response.data.get('action'))
        print(request.user.tg_chat_id)
        send_telegram_message(request.user.tg_chat_id, response.data.get('action'))
        return response


class HabitListAPIView(generics.ListAPIView):
    """Список привычек"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = FiveItemsPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user)


class HabitPublicListAPIView(generics.ListAPIView):
    """Список публичных привычек"""

    serializer_class = HabitSerializer
    pagination_class = FiveItemsPaginator
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
