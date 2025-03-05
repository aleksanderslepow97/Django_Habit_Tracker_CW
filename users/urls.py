from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .apps import UsersConfig
from .views import UserViewSet

app_name = UsersConfig.name

router_user = SimpleRouter()
router_user.register(r"user", UserViewSet, basename='user')

urlpatterns = (
    router_user.urls
    + [
        path("login/", TokenObtainPairView.as_view(), name="login"),
        path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ]
)
