"""
URL's para acceso a vista de la aplicacion app_timeseries_report

base_path => '/'

"""
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path

from .views import TimeSeriesReportsView

urlpatterns = [
     path(
          'reportes-ts/',
          login_required(TimeSeriesReportsView.as_view()),
          name="idx_app_timeseries_report"),
     path('reporte-ts/',
          include('app_timeseries_report.reporte.urls')),
     path('registro-ts/',
          include('app_timeseries_report.registro.urls')),
]
