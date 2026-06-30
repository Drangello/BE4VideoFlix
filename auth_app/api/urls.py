from django.urls import path

from auth_app.api.views import ActivateView, LoginView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "activate/<uidb64>/<token>/",
        ActivateView.as_view(),
        name="activate",
    ),
]