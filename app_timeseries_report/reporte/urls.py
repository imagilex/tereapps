"""
URL's para el modulo de administración de Catalogos Remotos
Se generan las url para CRUD con los permisos requeridos

obj = 'reportets'
app_label = 'app_timeseries_report'

base_path => reporte-ts/

Perm => View => Path
--------------------
- view   => list   =>
- add    => create => nuevo/
- change => update => actualizar/<pk>/
- delete => delete => eliminar/<pk>/
- view   => read   => <pk>/

permiso_requerido = {app_label}.{Perm}_{obj}
vista = {obj}_{View}

"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.urls import path

import app_timeseries_report.reporte.vw as views

from .models import ReporteTS

obj = 'reportets'
app_label = 'app_timeseries_report'

urlpatterns = [
    path('', permission_required(
        f'{app_label}.view_{obj}')(views.List.as_view()),
        name=f"{obj}_list"),
    path('nuevo/', permission_required(
        f'{app_label}.add_{obj}')(views.Create.as_view()),
        name=f"{obj}_create"),
    path('actualizar/<pk>/', permission_required(
        f'{app_label}.change_{obj}')(views.Update.as_view()),
        name=f"{obj}_update"),
    path('eliminar/<pk>/', permission_required(
        f'{app_label}.delete_{obj}')(views.Delete.as_view()),
        name=f"{obj}_delete"),
    path(f'mostrar-reporte/<pk>/', login_required()(
        views.Display.as_view()),
        name=f"reportets_display"),
    path('<pk>/', permission_required(
        f'{app_label}.view_{obj}')(views.Read.as_view()),
        name=f"{obj}_read"),
] + [
    path(f'mostrar-reporte/{reporte.pk}/', permission_required(
        f'{app_label}.view_reportets_{reporte.pk}')(views.Display.as_view()),
        name=f"reportets_display_{reporte.pk}")
    for reporte in ReporteTS.objects.all()
    ]
