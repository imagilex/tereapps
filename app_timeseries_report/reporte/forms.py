from zend_django.hiperforms import HorizontalModelForm

from .models import ReporteTS


class frmMain(HorizontalModelForm):

    class Meta:
        model = ReporteTS
        fields = [
            'nombre',
            'concepto_predefinido',
        ]
