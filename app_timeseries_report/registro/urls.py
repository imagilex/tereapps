"""
URL's para el modulo de administración de Catalogos Remotos
Se generan las url para CRUD con los permisos requeridos

obj = 'registrots'
app_label = 'app_timeseries_report'

base_path => registro-ts/

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
from django.contrib.auth.decorators import permission_required
from django.urls import path

import app_timeseries_report.registro.vw as views

obj = 'registrots'
app_label = 'app_timeseries_report'

urlpatterns = [
    path('actualizar-registros/<pk>/', permission_required(
        f'{app_label}.update_{obj}_by_hand')(
            views.UpdateRecords.as_view()),
        name=f"{obj}_update_by_hand"),
    path('actualizar-registros-txt/<pk>/', permission_required(
        f'{app_label}.update_{obj}_by_txt')(
            views.UpdateRecordsTXT.as_view()),
        name=f"{obj}_update_by_txt"),
    path('actualizar-registros-xlsx/<pk>/', permission_required(
        f'{app_label}.update_{obj}_by_xlsx')(
            views.UpdateRecordsXLSX.as_view()),
        name=f"{obj}_update_by_xlsx"),
]
