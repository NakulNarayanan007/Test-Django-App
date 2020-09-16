from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView
from rest_auth import views
from rest_auth.registration import views as reg_views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password/reset/", views.PasswordResetView.as_view(), name="rest_password_reset"
    ),
    path(
        "password/reset/confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path(
        "password/change/",
        views.PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path("register/", reg_views.RegisterView.as_view(), name="registration"),
    path(
        "account-confirm-email/(?P<key>[-:\w]+)/$",
        TemplateView.as_view(),
        name="account_confirm_email",
    ),
]
