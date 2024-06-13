from zend_django.hiperforms import HorizontalModelForm

from .models import CatalogoRemotoConfiguracion

class frmMain(HorizontalModelForm):

    class Meta:
        model = CatalogoRemotoConfiguracion
        fields = [
            'nombre',
            'url_script_sitio',
            'comando_listar',
            'comando_mostrar',
            'raiz_de_listado',
            'ruta_movil_de_archivo',
            'elemento_thumbnail',
            'elementos_por_fila',
        ]