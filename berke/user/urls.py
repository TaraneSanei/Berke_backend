from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PreferenceUpdateView, UserCreateAPIView, UserProfileRetrieveUpdateAPIView, generate_and_send_otp, verify_otp


urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name ='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileRetrieveUpdateAPIView.as_view(), name='user_profile'),
    path('preferences/', PreferenceUpdateView.as_view(), name='update_preferences'),
    path('otp/send/', generate_and_send_otp, name='send_otp'),
    path('otp/verify/', verify_otp, name='verify_otp')
]