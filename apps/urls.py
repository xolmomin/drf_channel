from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', TokenObtainPairView.as_view(), name='login'),
]
