"""
Formularios para modelo Factor

Formularios
-----------
frmFactor
    Formulario de Captura y Actualización
    - factor
    - posicion
    - ponderacion_nivel_1
    - exponente

frmFactorRead
    Formulario de Lectura
    - factor
    - posicion
    - ponderacion_nivel_1
    - exponente
    - cantidad_de_niveles
"""
from django import forms

from .factor_models import Factor

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from crispy_forms.bootstrap import InlineField, FormActions, StrictButton, Div
from crispy_forms.layout import Layout
from crispy_forms import bootstrap, layout

class frmFactor(forms.ModelForm):
    """
    Formulario principal del modelo Factor

    Campos
    ------
    - factor
    - posicion
    - ponderacion_nivel_1
    - exponente
    """

    class Meta:
        model = Factor
        fields = [
            'factor',
            'posicion',
            'ponderacion_nivel_1',
        ]


class frmFactorRead(forms.ModelForm):
    """
    Formulario para mostrar el modelo Factor

    Campos
    ------
    - factor
    - posicion
    - ponderacion_nivel_1
    - exponente
    - cantidad_de_niveles
    """

    class Meta:
        model = Factor
        fields = [
            'factor',
            'ponderacion_nivel_1',
        ]

    field_order = [
        'factor',
        'ponderacion_nivel_1',]
