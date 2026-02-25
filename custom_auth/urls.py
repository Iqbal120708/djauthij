from django.urls import path
from .views import *

urlpatterns = [
    path("register/", register, name="register"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("profile/", profile, name="profile")
]