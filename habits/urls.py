from django.urls import path
from rest_framework.routers import SimpleRouter

from habit.apps import HabitConfig
from habit.views import (HabitpublicityListAPIView, HabitViewSet,
                         UserhabitListAPIView)

app_name = HabitConfig.name

router = SimpleRouter()
router.register("", HabitViewSet)

urlpatterns = [
    path("habitpublicity/", HabitpublicityListAPIView.as_view(), name="habitpublicity"),
    path("userhabit/", UserhabitListAPIView.as_view(), name="userhabit"),
]

urlpatterns += router.urls
