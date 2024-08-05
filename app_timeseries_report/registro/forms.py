from django import forms
from zend_django.hiperforms import HorizontalForm
from zend_django.hiperforms import HorizontalModelForm


class frmUploadUpdateFile(HorizontalForm):
    archivo = forms.FileField(required=True)
