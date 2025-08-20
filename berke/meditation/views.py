from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from meditation.serializers import CourseSerializer, TagSerializer, TrackSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.http import condition
# Create your views here.

class TrackListAPIView(ListAPIView):
    serializer_class = TrackSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Track.objects.all()
    lookup_field = 'course'


def course_list_last_modified(request, *args, **kwargs):
    latest_update = Course.objects.latest('updated_at').updated_at
    return latest_update

@method_decorator(condition(last_modified_func=course_list_last_modified), name='dispatch')    
class CourseListAPIView(ListAPIView):
    serializer_class = CourseSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()


def tags_list_last_modified(request, *args, **kwargs):
    latest_update = Tag.objects.latest('updated_at').updated_at
    return latest_update

@method_decorator(condition(last_modified_func=tags_list_last_modified), name='dispatch')    
class TagsListAPIView(ListAPIView):
    serializer_class = TagSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()