from .views import *
from django.urls import path


urlpatterns = [
    path('tracks/<int:course>/', TrackListAPIView.as_view(), name='track-list'),
    path('courses/', CourseListAPIView.as_view(), name='course-list'), 
    path('tags/', TagsListAPIView.as_view(), name='tags-list'), 
]