import csv
import io

from datetime import date
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from openpyxl import load_workbook
from os import remove

from .forms import frmUploadUpdateFile
from .models import RegistroTS
from .models import ReporteTS as main_model


def template_base_path(file):
    return 'app_timeseries_report/registro/' + file + ".html"


MSGS_ALERT = [
    """
        Al realizar la carga del archivo tome en cuenta
        las siguientes consideraciones:
        <ol>
            <li>
                Se actualizarán todos los registros existentes al valor
                contenido en el archivo
            </li>
            <li>
                Si un registro no existe en la base de datos se agregará
                como nuevo
            </li>
            <li>
                No se eliminará ningún registro
            </li>
        </ol>
    """,
    ]


def update_report(reporte, rows):
    headers = [k for k in rows[0].keys() if k and str(k).strip()]
    desc_field = headers[0]
    periodos = headers[1:]
    pers = dict()
    for periodo in periodos:
        pers[periodo] = date(int(periodo[0:4]), int(periodo[5:7]), 1)
    for i, row in enumerate(rows):
        try:
            entidad, concepto, tipo = row[desc_field].replace(
                '--', '-@@').split('-')
        except ValueError as ex:
            print(f"EXCEPCION: {ex} EN {i =} {row =}")
            continue
        concepto = concepto.replace('@@', '-')
        tipo = tipo.upper()
        entidad = entidad.upper()
        for periodo in periodos:
            if row[periodo] is None:
                continue
            db_row = RegistroTS.objects.get_or_create(
                reporte=reporte,
                entidad=entidad,
                concepto=concepto,
                tipo=tipo,
                periodo=pers[periodo]
            )[0]
            db_row.valor = float(row[periodo])
            db_row.save()


class UpdateRecords(View):
    tereapp = 'administrar'
    titulo_descripcion = "Actualizar"
    main_data_model = main_model
    html_template = template_base_path("upd_by_hand")
    model_name = "reportets"

    def base_render(self, request, pk, obj, filters=None):
        data = None
        if filters:
            data = RegistroTS.objects.all()
            if filters['entidad']:
                data = data.filter(entidad=filters['entidad'])
            if filters['concepto']:
                data = data.filter(concepto=filters['concepto'])
            if filters['tipo']:
                data = data.filter(tipo=filters['tipo'])
            if filters['periodo']:
                data = data.filter(
                    periodo=datetime.strptime(filters['periodo'], '%Y/%m/%d'))
        return render(request, self.html_template, {
            'titulo': obj,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': None,
            'tereapp': self.tereapp,
            'object': obj,
            'withoutBtnSave': False,
            'filters': filters,
            'data': data,
        })

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        return self.base_render(request, pk, obj)

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        if request.POST.get('action', '') == "update":
            pks = request.POST.getlist('pk[]')
            entidad = request.POST.getlist('entidad[]')
            concepto = request.POST.getlist('concepto[]')
            tipo = request.POST.getlist('tipo[]')
            periodo = request.POST.getlist('periodo[]')
            valor = request.POST.getlist('valor[]')
            for idx in range(len(pks)):
                row = RegistroTS.objects.get(pk=pks[idx])
                row.entidad = entidad[idx]
                row.concepto = concepto[idx]
                row.tipo = tipo[idx].upper()
                row.valor = float(valor[idx])
                row.periodo = date(
                    int(periodo[idx][0:4]),
                    int(periodo[idx][-2:]),
                    1)
                row.save()
        elif request.POST.get('action', '') == 'delete':
            for pkd in request.POST.getlist('pkdelete[]'):
                RegistroTS.objects.get(pk=pkd).delete()
        return self.base_render(request, pk, obj, {
            'entidad': request.POST.get('filtro-entidad', ''),
            'concepto': request.POST.get('filtro-concepto', ''),
            'tipo': request.POST.get('filtro-tipo', ''),
            'periodo': request.POST.get('filtro-periodo', ''),
        })


class UpdateRecordsTXT(View):
    tereapp = 'administrar'
    titulo_descripcion = "Actualizar con archivo TXT"
    main_data_model = main_model
    html_template = template_base_path("upd_by_txt")
    model_name = "reportets"

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        return render(request, self.html_template, {
            'titulo': obj,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': MSGS_ALERT,
            'req_chart': False,
            'search_value': '',
            'forms': {'top': [{'form': frmUploadUpdateFile()}]},
            'tereapp': self.tereapp,
            'object': obj,
            'withoutBtnSave': False,
        })

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        with open('tmp_file.csv', 'wb+') as dest:
            for c in request.FILES['archivo'].chunks():
                dest.write(c)
        with io.open('tmp_file.csv', 'r', encoding='latin-1') as f:
            rows = [row for row in csv.DictReader(f, delimiter='|')]
        remove('tmp_file.csv')
        keys = list(rows[0].keys())
        for k in keys:
            if k.strip() == "":
                for row in rows:
                    del row[k]
                del k
            elif k != keys[0]:
                for row in rows:
                    row[k] = float(row[k].replace(',', ''))
        update_report(obj, rows)
        return HttpResponseRedirect(reverse(
            f'{self.model_name}_read',
            kwargs={'pk': obj.pk}))


class UpdateRecordsXLSX(View):
    tereapp = 'administrar'
    titulo_descripcion = "Actualizar con archivo XLSX"
    main_data_model = main_model
    html_template = template_base_path("upd_by_xlsx")
    model_name = "reportets"

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        return render(request, self.html_template, {
            'titulo': obj,
            'titulo_descripcion': self.titulo_descripcion,
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': MSGS_ALERT,
            'req_chart': False,
            'search_value': '',
            'forms': {'top': [{'form': frmUploadUpdateFile()}]},
            'tereapp': self.tereapp,
            'object': obj,
            'withoutBtnSave': False,
        })

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        with open('tmp_file.xlsx', 'wb+') as dest:
            for c in request.FILES['archivo'].chunks():
                dest.write(c)
        wb = load_workbook('tmp_file.xlsx', read_only=True, data_only=True)
        ws = wb['Estadistica']
        rows = [list(r) for r in list(ws.values)]
        remove('tmp_file.xlsx')
        keys = rows[3]
        rows = [dict(zip(keys, row)) for row in rows[4:]]
        update_report(obj, rows)
        return HttpResponseRedirect(reverse(
            f'{self.model_name}_read',
            kwargs={'pk': obj.pk}))
