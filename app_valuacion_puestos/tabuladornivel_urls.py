"""
URL's para el modulo de administración de niveles de tabuladores
Se generan las url para CRUD con los permisos requeridos

obj = 'tabuladornivel'
app_label = 'app_valuacion_puestos'

base_path => nivel-de-tabulador/

Perm     => View   => Path
--------------------------
- add    => create => nuevo/
- change => update => actualizar/<pk>/
- delete => delete => eliminar/<pk>/
- view   => read   => <pk>/

permiso_requerido = {app_label}.{Perm}_{obj}
vista = {obj}_{View}

"""
from django.contrib.auth.decorators import permission_required
from django.urls import path

import app_valuacion_puestos.tabuladornivel_vw as views

obj = 'tabuladornivel'
app_label = 'app_valuacion_puestos'

urlpatterns = [
    path('nuevo/<pk_padre>/', permission_required(
        f'{app_label}.add_{obj}')(views.Create.as_view()),
        name=f"{obj}_create"),
    path('actualizar/<pk>/', permission_required(
        f'{app_label}.change_{obj}')(views.Update.as_view()),
        name=f"{obj}_update"),
    path('eliminar/<pk>/', permission_required(
        f'{app_label}.delete_{obj}')(views.Delete.as_view()),
        name=f"{obj}_delete"),
    path('<pk>/', permission_required(
        f'{app_label}.view_{obj}')(views.Read.as_view()),
        name=f"{obj}_read"),
]
