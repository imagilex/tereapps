from django.contrib.auth.models import Permission

from zend_django.models import MenuOpc
from zend_django.models import ParametroUsuario
from zend_django.parametros_models import PARAM_TYPES

from .utils import update_permisos


def migration():
    update_permisos()

    opc = MenuOpc.objects.get_or_create(
        nombre="Reportes TS",
        vista="reportets_list",
        posicion=10,
        padre=MenuOpc.objects.get(
            nombre='Administrar', vista='idx_tereapp_administracion')
    )[0]
    opc.permisos_requeridos.set([
        Permission.objects.get(codename='add_reportets'),
        Permission.objects.get(codename='change_reportets'),
        Permission.objects.get(codename='delete_reportets'),
        Permission.objects.get(codename='view_reportets'),
    ])

    ParametroUsuario.objects.get_or_create(
        seccion='basic_search', nombre='reportets',
        tipo=PARAM_TYPES['CADENA'], es_multiple=False)

    opc = MenuOpc.objects.get_or_create(
        nombre="Nómina",
        vista="idx_app_timeseries_report",
        posicion=4
    )[0]
