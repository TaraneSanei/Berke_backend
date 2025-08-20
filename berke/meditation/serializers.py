from rest_framework import serializers
from .models import *


class TrackSerializer(serializers.ModelSerializer):
    audioUrl = serializers.URLField(source='audio_url', read_only=True)
    dayNumber = serializers.IntegerField(source='day_number', read_only=True)

    class Meta:
        model = Track
        fields = ['id', 'title', 'audioUrl', 'duration', 'course', 'dayNumber']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'tags']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']