import csv
import io
import requests

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.views import View
from openpyxl import load_workbook
from os import remove
from sys import modules
import importlib

from zend_django.parametros_models import ParametroUsuario
from zend_django.templatetags.op_helpers import crud_icon
from zend_django.templatetags.op_helpers import crud_label
from zend_django.templatetags.utils import GenerateReadCRUDToolbar
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate

from .forms import frmMain as base_form
from .models import ReporteTS as main_model

import app_timeseries_report.reporte.dp_config as dp_config


def template_base_path(file):
    return 'app_timeseries_report/reporte/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Reporte TS"
    main_data_model = main_model
    model_name = "reportets"
    tereapp = 'administrar'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(nombre__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Reporte TS"
    model_name = "reportets"
    base_data_form = base_form
    main_data_model = main_model
    tereapp = 'administrar'
    html_template = template_base_path("see")

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj)
        toolbar = GenerateReadCRUDToolbar(
            request, self.model_name, obj, self.main_data_model)
        if request.user.has_perm(
                "app_timeseries_report.update_report_by_hand"):
            toolbar.append({
                'type': 'link_pk',
                'label': '<i class="fas fa-edit"></i>',
                'title': 'Actualizacion Manual',
                'view': 'registrots_update_by_hand',
                'pk': obj.pk,
            })
        if request.user.has_perm(
                "app_timeseries_report.update_report_by_txt"):
            toolbar.append({
                'type': 'link_pk',
                'label': '<i class="fas fa-file-alt"></i>',
                'title': 'Actualizacion TXT',
                'view': 'registrots_update_by_txt',
                'pk': obj.pk,
            })
        if request.user.has_perm(
                "app_timeseries_report.update_report_by_xlsx"):
            toolbar.append({
                'type': 'link_pk',
                'label': '<i class="fas fa-file-excel"></i>',
                'title': 'Actualizacion XLSX',
                'view': 'registrots_update_by_xlsx',
                'pk': obj.pk,
            })
        return render(request, self.html_template, {
            'titulo': obj,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': toolbar,
            'footer': False,
            'read_only': True,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {'top': [{'form': form}]},
            'tereapp': self.tereapp,
            'object': obj,
            'withoutBtnSave': True,
        })


class Create(GenericCreate):
    titulo = "Reporte TS"
    model_name = "reportets"
    base_data_form = base_form
    tereapp = 'administrar'


class Update(GenericUpdate):
    titulo = "Reporte TS"
    model_name = "reportets"
    base_data_form = base_form
    main_data_model = main_model
    tereapp = 'administrar'


class Delete(GenericDelete):
    model_name = "reportets"
    main_data_model = main_model
    tereapp = 'administrar'


class Display(View):
    main_data_model = main_model
    tereapp = 'timeseries_report'
    html_template = template_base_path("display")

    def get(self, request, pk=None):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)

        dp_config.pk_reportets = pk
        from . import dp_display_report

        return render(request, self.html_template, {
            'titulo': obj,
            'toolbar': None,
            'footer': False,
            'read_only': True,
            'alertas': [],
            'req_chart': True,
            'search_value': None,
            'tereapp': self.tereapp,
            'object': obj,
            'withoutBtnSave': True,
            'dp_name': 'DP_Display_ReporteTS',
        })
