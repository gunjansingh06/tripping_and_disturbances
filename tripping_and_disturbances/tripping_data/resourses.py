from import_export import resources
from . import models as tripping_models

class TrippingDataResources(resources.ModelResource):

    class Meta:
        model = tripping_models.Incident
        fields = (
                'id', 'spv', 'voltage_level', 'line_name', 'criticality', 'financial_year',
                'tower_span_no', 'site_head', 'month', 'incident_date', 'incident_time',
                'restoration_date', 'restoration_time', 'total_time_hrs', 'outage_hrs',
                'disturbance_type', 'disturbance_category', 'risk_factor',
                'total_line_length_kms', 'zone', 'scope', 'tripping_per_100ckt_km',
                'fy_atl_ckt_km', 'per_100ckt_km', 'fy_atl_elements_count',
                'per_100ckt_km_elements_performance', 'remarks', 'line_criticality',
                'state', 'season', 'region', 'asset_consideration_date',
                'asset_ageing_at_event', 'asset_age_years', 'business_unit', 'event_count',
                'ptw_availed', 'ptw_returned', 'net_outage_hours', 'man_on_job',
                'manhours', 'vehicle_km', 'vehicle_cost', 'rm_cost',
                'transportation_cost', 'breakdown_cost', 'fy_week_no', 'created_at'
                )