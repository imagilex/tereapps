"""
Formularios para modelo MenuOpc

Formularios
-----------
frmMenuOpc
    Formulario Completo
    - nombre
    - padre
    - posicion
    - vista
    - permisos_requeridos
"""
from django import forms

from .hiperforms import HorizontalModelForm
from .menuopc_models import MenuOpc


class frmMenuOpc(HorizontalModelForm):
    """
    Formulario principal del modelo MenuOpc

    Campos
    ------
    - nombre
    - padre
    - posicion
    - vista
    - permisos_requeridos
    """

    class Meta:
        model = MenuOpc
        fields = [
            'nombre',
            'padre',
            'posicion',
            'vista',
            'permisos_requeridos',
        ]
        widgets = {
            'permisos_requeridos': forms.CheckboxSelectMultiple()
        }
