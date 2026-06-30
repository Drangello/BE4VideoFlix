from django.urls import path

from auth_app.api.views import (
    ActivateView,
    LoginView,
    RegisterView,
    TokenRefreshView,
    LogoutView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "activate/<uidb64>/<token>/",
        ActivateView.as_view(),
        name="activate",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]