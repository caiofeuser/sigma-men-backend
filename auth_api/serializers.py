from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUserModel


class CustomRegistration(RegisterSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    def custom_signup(self, request, user):
        first = request.POST.get("first_name")
        last = request.POST.get("last_name")
        user.first_name = first
        user.last_name = last
        user.save()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ('email', 'first_name', 'last_name', 'age',
                  'is_active', 'is_staff', 'date_joined', 'last_login')


class VerificationSerializer(serializers.Serializer):
    is_verified = serializers.BooleanField()
    message = serializers.CharField(required=False)
