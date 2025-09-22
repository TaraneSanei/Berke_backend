from django.shortcuts import render
from requests import request
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import JourneyListSerializer
from .models import *
from rest_framework.pagination import CursorPagination

# Create your views here.



class JourneyCursorPagination(CursorPagination):
    #this is for th endless scroll pagination
    page_size = 8
    ordering = 'course_id'



class journeyListAPIView(ListAPIView):
    pagination_class = JourneyCursorPagination
    serializer_class = JourneyListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        return meditation_session.objects.filter(owner = user).order_by('track__day_number' , '-dateTime')