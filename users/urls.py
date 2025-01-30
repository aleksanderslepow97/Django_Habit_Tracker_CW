from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.apps import UsersConfig
from users.views import CustomsUserCreateAPIView, CustomsUserViewSet, CustomTokenObtainPairView

router = SimpleRouter()


router.register("", CustomsUserViewSet, basename="users")

app_name = UsersConfig.name

urlpatterns = [
    path("register/", CustomsUserCreateAPIView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
]

urlpatterns += router.urls
