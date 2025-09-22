from .views import *
from django.urls import path

urlpatterns = [
    path('new/', JournalCreateAPIView.as_view(), name='new_journal'),
    path("<int:pk>", EditDeleteJournalAPIView.as_view(), name="Delete_edit_journal"),
]