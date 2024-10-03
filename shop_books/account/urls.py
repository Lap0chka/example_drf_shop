from django.shortcuts import render
from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from . import views

router = routers.DefaultRouter()
router.register(r'profile', views.UserDetailView)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', views.UserCreateView.as_view(), name='register'),
    path('email-verification-sent/',
         lambda request: render(request, 'account/email/email-verification-sent.html'),
         name='email_verification_sent'
         ),
    path('api/', include(router.urls))
]
