from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
# Create your views here.

class JournalCreateAPIView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JournalSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class EditDeleteJournalAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JournalSerializer
    def get_queryset(self):
        user = self.request.user
        return Journal.objects.filter(Owner = user)
    