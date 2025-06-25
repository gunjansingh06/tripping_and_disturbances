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
            (print(start_year, end_year))

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
    

class FilterOptionView(APIView):
    def get (self,request):
        try:
            formatted_data = {
                "filters_fields" :[],
            }   

            start_year = request.GET.get('start_year')
            end_year = request.GET.get('end_year')
            site_head = request.GET.get('site_head')
            month = request.GET.get('month')

            filters = {}
             
            start_year = int(start_year)
            end_year  = int(end_year)

            formated_date_fs = (datetime(start_year, 4, 1))
            formated_date_fe = (datetime(end_year, 3, 1))

            if site_head:
                site_head_list = site_head.split(',')
                filters['site_head__in'] = site_head_list
                 

            filters_yearly = filters.copy()
            filters_yearly['incident_date__range'] = (formated_date_fs, formated_date_fe)

            queryset = Incident.objects.filter(**filters_yearly)
            tripping_count =queryset.filter(disturbance_type="Tripping").count()
            

            spv_list = Incident.objects.all().values_list('spv', flat=True)
            line_name_list = Incident.objects.all().values_list('line_name', flat=True)
            criticality = Incident.objects.all().values_list('criticality', flat=True)
            incident_date = Incident.objects.all().values_list('incident_date', flat=True)
            disturbance_type = Incident.objects.all().values_list('disturbance_type', flat=True)
            disturbance_category = Incident.objects.all().values_list('disturbance_category', flat=True)
            outage_hrs = Incident.objects.all().values_list('outage_hrs', flat=True)
            risk_factor = Incident.objects.all().values_list('risk_factor', flat=True)

            formatted_data['filters_fields']= [
                {
                    "name": "SPV",
                    "value" : spv_list,
                },
                {
                    "name": "Line Name",
                    "value" : line_name_list,
                },
                {
                    "name" : "Criticality",
                    "value" : criticality,
                },
                {
                    "name" : "Incident Date",
                    "value" : incident_date,
                },
                {
                    "name" : "Disturbance Type",
                    "value" : disturbance_type,
                },
                {
                    "name" : "Disturbance Category",
                    "value" : disturbance_category,
                },
                {
                    "name" : "Outage Hrs",
                    "value" : outage_hrs,
                },
                {
                    "name" : "Risk Factor",
                    "value" : risk_factor,
                },
                
            ]


            
            return Response(data={"data": formatted_data})
        except Exception as e:
            return Response(data={'message': [str(e)]}) 


                     
