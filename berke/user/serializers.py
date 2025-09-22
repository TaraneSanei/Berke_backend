from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from meditation.serializers import TagSerializer
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], required=False)
    phoneNumber = serializers.CharField(source='phone_number', required=False)
    minutesListened = serializers.IntegerField(source='minutes_listened', required=False, read_only=True)
    isSubscribed = serializers.BooleanField(source='is_subscribed', required=False, read_only=True)
    subscribedAt = serializers.DateField(source='subscribed_at', required=False, read_only=True)
    subscriptionEnd = serializers.DateField(source='subscription_end', required=False, read_only=True)
    preferences = TagSerializer(many=True, required=False)
    theme = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'phoneNumber',
            'password',
            'username',
            'authenticated',
            'minutesListened',
            'isSubscribed',
            'subscribedAt',
            'subscriptionEnd',
            'preferences',
            'theme'
        ]
    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
        )
        return user