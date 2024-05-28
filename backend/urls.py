"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from auth_api.views import reset_password_confirm
from auth_api.views import CustomEmailConfirmView, CustomUserInfo, VerifyEmailUser, GoogleLoginView

# Ensure that this is imported correctly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth_api/', include("dj_rest_auth.urls")),
    path('auth_api/registration/', include("dj_rest_auth.registration.urls")),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        CustomEmailConfirmView.as_view(),
        name='account_confirm_email',
    ),
    path('auth_api/user/info/', CustomUserInfo.as_view(), name='user_info'),
    path('auth_api/user/is-verified/',
         VerifyEmailUser.as_view(), name='verify-email'),
    path('auth_api/reset/password/confirm/<int:uid>/<str:token>/',
         reset_password_confirm, name="password_reset_confirm"),
    path('auth_api/google/', GoogleLoginView.as_view(), name='google_login'),
    path('api/', include('api.urls')),
]
