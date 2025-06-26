"""
Vistas relacionadas con el modelo Puesto

Vistas
------
- List
- Read
- Create
- Update
- Delete
"""
import json

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from zend_django.templatetags.op_helpers import crud_label
from zend_django.templatetags.utils import GenerateReadCRUDToolbar
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate

from .models import Factor
from .models import Nivel
from .models import Ponderacion
from .models import Tabulador
from .puesto_forms import frmPuesto as base_form
from .puesto_forms import frmPuestoRead
from .puesto_models import Puesto as main_model
from .puesto_models import PuestoEvaluacion


def template_base_path(file):
    return 'app_valuacion_puestos/puesto/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Puesto"
    titulo_descripcion = ""
    main_data_model = main_model
    model_name = "puesto"
    tereapp = 'valuacion_de_puestos'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(puesto__icontains=search_value)))


class Read(GenericRead):
    html_template = template_base_path('see')
    titulo_descripcion = "Puesto"
    model_name = "puesto"
    base_data_form = frmPuestoRead
    main_data_model = main_model
    tereapp = 'valuacion_de_puestos'

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(
            instance=obj, initial={'ponderacion_total': obj.ponderacion_total})
        toolbar = GenerateReadCRUDToolbar(
            request, self.model_name, obj, self.main_data_model)
        toolbar.append({
            'type': 'button',
            'label': '<i class="far fa-edit" aria-hidden="true"></i> Calificación',
            'title': 'Actualizar Calificación de Factores', 'onclick': 'abre_edicion_calificaciones()',
        })
        autosaved = None
        if obj.evaluaciones.all().count() > 0:
            autosaved = obj.evaluaciones.filter(nombre="autosave").first()
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
            'factores': list(Factor.objects.all()),
            'last_ev': autosaved,
            'tabuladores': list(Tabulador.objects.all()),
            'factores_json': json.dumps([
                factor.as_dict() for factor in list(Factor.objects.all())]),
        })

    def post(self, request, pk):
        califaction = request.POST.get('califaction', '')
        obj = self.main_data_model.objects.get(pk=pk)
        if "autosave" == califaction:
            data = {
                'puesto': {
                    'pk': obj.pk,
                    'puesto': obj.puesto,
                },
                'factores': [{
                    'pk': factor.pk,
                    'factor': factor.factor,
                    'exponente': float(factor.exponente),
                    'pond_lvl1': float(factor.ponderacion_nivel_1),
                    'nivel_selected': factor.niveles.get(
                        nivel_multiplicador=int(
                            request.POST.get(
                                f'txt_factor_{factor.pk}', ''))).pk,
                    'niveles': [{
                        'pk': nivel.pk,
                        'nivel': nivel.nivel,
                        'multiplicador': nivel.nivel_multiplicador,
                        'ponderacion': float(nivel.ponderacion),
                        'ponderacion_en_pesos': float(
                            nivel.ponderacion_en_pesos),
                        'selected': str(nivel.nivel_multiplicador) ==
                        request.POST.get(
                            f'txt_factor_{factor.pk}', ''),
                    } for nivel in factor.niveles.all()],
                } for factor in Factor.objects.all()],
            }
            evaluacion = PuestoEvaluacion.objects.get_or_create(
                puesto=obj,
                nombre='autosave'
            )[0]
            evaluacion.data = json.dumps(data)
            evaluacion.save()
        elif "change-tab" == califaction:
            obj.tabulador = Tabulador.objects.get(
                pk=int("0" + request.POST.get('tabulador')))
            obj.save()
        return self.get(request, pk)


class Create(GenericCreate):
    html_template = template_base_path('form')
    titulo = "Puesto"
    model_name = "puesto"
    base_data_form = base_form
    tereapp = 'valuacion_de_puestos'

    def base_render(self, request, forms):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': crud_label('create'),
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': forms,
            'tereapp': self.tereapp,
            'factores': list(Factor.objects.all()),
        })

    def post(self, request):
        form = self.base_data_form(request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save()
            for factor in Factor.objects.all():
                Ponderacion.objects.create(
                    puesto=obj,
                    nivel=Nivel.objects.get(
                        pk=request.POST.get(f"factor_{factor.pk}"))
                )
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, {'top': [{'form': form}]})


class Update(GenericUpdate):
    html_template = template_base_path('form')
    titulo = "Puesto"
    model_name = "puesto"
    base_data_form = base_form
    main_data_model = main_model
    tereapp = 'valuacion_de_puestos'

    def base_render(self, request, form, obj):
        return render(request, self.html_template, {
            'titulo': self.titulo,
            'titulo_descripcion': crud_label('update'),
            'toolbar': None,
            'footer': False,
            'read_only': False,
            'alertas': [],
            'req_chart': False,
            'search_value': '',
            'forms': {'top': [{'form': form}]},
            'tereapp': self.tereapp,
            'object': obj,
            'factores': list(Factor.objects.all()),
        })

    def post(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(
            instance=obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save()
            obj.niveles_ponderacion.all().delete()
            for factor in Factor.objects.all():
                Ponderacion.objects.create(
                    puesto=obj,
                    nivel=Nivel.objects.get(
                        pk=request.POST.get(f"factor_{factor.pk}"))
                )
            return HttpResponseRedirect(reverse(
                f'{self.model_name}_read',
                kwargs={'pk': obj.pk}))
        return self.base_render(request, form, obj)


class Delete(GenericDelete):
    model_name = "puesto"
    main_data_model = main_model
