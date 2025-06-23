from django.shortcuts import render
from rest_framework import generics
from .models import Incident
from .serializers import IncidentSerializer
from django.db.models import Count

class IncidentListAPIView(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

def dashboard(request):
    context = {}
    return render(request, 'tripping_data/dashboard.html', context)