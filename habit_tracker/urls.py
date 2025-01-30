from django.urls import path
from habit_tracker.apps import HabitTrackerConfig
from rest_framework.routers import SimpleRouter

from .views import HabitViewSet, PublicHabitListAPIView

app_name = HabitTrackerConfig.name


router = SimpleRouter()
router.register("", HabitViewSet, basename="habits")

urlpatterns = [
    path("public/", PublicHabitListAPIView.as_view(), name="public_list"),
] + router.urls
