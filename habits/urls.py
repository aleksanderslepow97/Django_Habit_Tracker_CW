from django.urls import path
from .views import (HabitPublicListAPIView, HabitCreateAPIView, HabitDestroyAPIView, HabitListAPIView,
                    HabitUpdateAPIView, HabitRetrieveAPIView)

app_name = 'habits'


urlpatterns = [
    path("", HabitListAPIView.as_view(), name="habit_list"),
    path("habit/<int:pk>", HabitRetrieveAPIView.as_view(), name="habit_retrieve"),
    path("habit/create", HabitCreateAPIView.as_view(), name="habit_create"),
    path("habit/<int:pk>/update", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("habit/<int:pk>/delete", HabitDestroyAPIView.as_view(), name="habit_delete"),
    path("habit/public/", HabitPublicListAPIView.as_view(), name="habit_public_list"),
]
