from .views import *
from django.urls import path



urlpatterns =[
    path('journeys/', journeyListAPIView.as_view(), name='journeys')
]