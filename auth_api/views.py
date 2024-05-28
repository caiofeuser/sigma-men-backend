from allauth.account.admin import EmailAddress
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.conf import settings
from django.shortcuts import render, redirect
from rest_framework.response import Response
import requests
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import CustomUserModel
from .adapters import CustomGoogleOAuth2Adapter
from .serializers import CustomUserSerializer, VerificationSerializer


class GoogleLoginView(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = "http://localhost:3000/profile/"
    client_class = OAuth2Client

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

# class GoogleLogin(SocialLoginView):  # if you want to use Implicit Grant, use this
#     adapter_class = GoogleOAuth2Adapter


class CustomEmailConfirmView(APIView):
    def get(self, request, key):
        verify_email_url = 'http://localhost:8000/auth_api/registration/verify-email/'

        # make a POST request to the verify-email endpoint with the key
        response = requests.post(verify_email_url, {'key': key})
        if response.status_code == 200:
            return redirect(f"http://localhost:3000/register/verify-email/verified")
        else:
            return Response({'message': 'Email verification failed'}, status=status.HTTP_400_BAD_REQUEST)


def reset_password_confirm(request, uid, token):
    return redirect(f"http://localhost:3000/reset/password/confirm/{uid}/{token}")


class CustomUserInfo(APIView):
    def get(self, request):
        user = request.user
        queryset = CustomUserModel.objects.get(email=user.email)
        serializer = CustomUserSerializer(queryset)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmailUser(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            is_verified = EmailAddress.objects.filter(
                user=request.user, verified=True).exists()
            data = {'is_verified': is_verified}
            serializer = VerificationSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = {'message': 'User is not authenticated', 'is_verified': False}
            serializer = VerificationSerializer(data)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
