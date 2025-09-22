from django.shortcuts import render
from requests import request
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from meditation.models import Tag
from user.utils import PREFERENCES_MAP
from .serializers import UserSerializer
import pyotp
import datetime
from .models import OTP, User
from kavenegar import *

# Create your views here.


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []
    queryset = User.objects.all()


class UserProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PreferenceUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        experience = request.data.get("experience", "")
        goals = request.data.get("goals", [])
        theme = request.data.get("theme", "")
        username = request.data.get("username", "")
        notification = request.data.get("notifications", False)
        notification_time = request.data.get("notificationTime", None)
        user_experience = PREFERENCES_MAP.get(experience, [])
        user_goals = []
        for g in goals:
            user_goals.extend(PREFERENCES_MAP.get(g, []))
        all_tags = user_experience + user_goals
        tags = [Tag.objects.get_or_create(title=title)[0] for title in all_tags]

        #debug
        print("notifocation time", notification_time)
        if notification:
            user.notification = notification_time
        user.preferences.set(tags)
        user.theme = theme
        user.username = username
        user.save()
        return Response({"detail": "Preferences updated successfully."}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])

def generate_and_send_otp(request):
    user = request.user
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    otp_code = totp.now()
    created_at = datetime.datetime.now()
    expires_at = created_at + datetime.timedelta(minutes=2)
    OTP.objects.create(user=user, otp_secret=secret, otp_code=otp_code, created_at=created_at, expires_at=expires_at)
    success = send_sms_otp(user.phone_number, otp_code)
    if success: 
        print(f"OTP sent to {user.phone_number}: {otp_code}")
        return Response({"detail": "OTP sent successfully."}, status=200)
    return Response({"detail": "Failed to send OTP."}, status=500)


def send_sms_otp(phone_number, otp_code):
    try:
        api = KavenegarAPI('70474179312F2F6C75794F48626A64725035615574364831504743546F48523343364835395367427662673D')
        params = {
            'receptor': phone_number,
            'message': f'برکه کد تایید شما: {otp_code}',
            'type': 'sandbox',
            'sender': "2000660110"

        } 
        # response = api.sms_send(params)
        print(params)
        return True
    except APIException as e: 
        print(e)
        return False
    except HTTPException as e: 
        print(e)
        return False



@api_view(['POST'])
@permission_classes([IsAuthenticated])

def verify_otp(request):
    user = request.user
    entered_otp = request.data.get("otp")
    try:
        otp_instance = OTP.objects.get(user=user, expires_at__gt=datetime.datetime.now())
        totp = pyotp.TOTP(otp_instance.otp_secret)
        if totp.verify(entered_otp, valid_window=1):
            otp_instance.delete()
            user.auth_user()
            print(f"totp.verify result: {totp.verify(entered_otp, valid_window=1)}")
            return Response({"detail": "OTP verified successfully."}, status=200)
        else:
            print(f"totp.verify result: {totp.verify(entered_otp, valid_window=1)}")
            return Response({"detail": "Invalid OTP."}, status=400)
    except OTP.DoesNotExist:
        return Response({"detail": "OTP verification failed."}, status=400)
    
