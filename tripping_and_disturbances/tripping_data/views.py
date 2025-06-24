from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Incident
from .serializers import IncidentSerializer
from datetime import datetime
from django.db.models import Count

class IncidentListAPIView(generics.ListCreateAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer

def dashboard(request):
    context = {}
    return render(request, 'tripping_data/dashboard.html', context)

class TrippingCountView(APIView):
    def get(self, request):
        try:
            formatted_data = {
                    "top_four_kpi" : [], 
            }
            start_year = request.GET.get('start_year')
            end_year = request.GET.get('end_year')

            start_year_string = int(start_year)
            end_year_string = int(end_year)

            formated_date_fs = (datetime(start_year_string, 4, 1))
            formated_date_fe = (datetime(end_year_string, 3, 1))
            

            if formated_date_fs and formated_date_fe:
                incidents = Incident.objects.filter(incident_date__range=[formated_date_fs, formated_date_fe])

            forced_outage_count = incidents.filter(disturbance_type='Forced outage').count()
            ar_success_count = incidents.filter(disturbance_type='AR successful').count()
            lfl_count = incidents.filter(disturbance_type='LFL').count()
            tripping_count = incidents.filter(disturbance_type='Tripping').count()
        
            formatted_data['top_four_kpi'] = [
                {
                    "name" : "Tripping Count",
                    "value" : tripping_count,
                },
                {
                    "name" : "Forced Outage Count",
                    "value" : forced_outage_count,
                },
                {
                    "name" : "AR Successful Count",
                    "value" : ar_success_count,
                },
                {
                    "name": "LFL Count",
                    "value" : lfl_count,
                }
                    
                    
            ]

            return Response(data={"data": formatted_data})
        except Exception as e:
            return Response(data={'message': [str(e)]}) 
    
    

    
