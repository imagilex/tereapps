import requests

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.views import View

from zend_django.parametros_models import ParametroUsuario
from zend_django.templatetags.op_helpers import crud_icon
from zend_django.templatetags.op_helpers import crud_label
from zend_django.templatetags.utils import GenerateReadCRUDToolbar
from zend_django.views import GenericCreate
from zend_django.views import GenericDelete
from zend_django.views import GenericList
from zend_django.views import GenericRead
from zend_django.views import GenericUpdate

from .forms import frmCatalogo
from .forms import frmMain as base_form
from .models import CatalogoRemoto
from .models import CatalogoRemotoConfiguracion as main_model
from .models import Item


def template_base_path(file):
    return 'app_catalogo_remoto/catalogo/' + file + ".html"


class List(GenericList):
    html_template = template_base_path("list")
    titulo = "Catalogos Remotos"
    main_data_model = main_model
    model_name = "catalogoremotoconfiguracion"
    tereapp = 'administrar'

    def get_data(self, search_value=''):
        if '' == search_value:
            return list(
                self.main_data_model.objects.all())
        else:
            return list(self.main_data_model.objects.filter(
                Q(nombre__icontains=search_value) |
                Q(url_script_sitio__icontains=search_value)))


class Read(GenericRead):
    titulo_descripcion = "Catalogo Remoto (Configuración)"
    model_name = "catalogoremotoconfiguracion"
    base_data_form = base_form
    main_data_model = main_model
    tereapp = 'administrar'
    html_template = template_base_path("read")

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj)
        toolbar = GenerateReadCRUDToolbar(
            request, self.model_name, obj, self.main_data_model)
        if request.user.has_perm(
                "catalogoremotoconfiguracion.synchronize_remote_catalogs"):
            toolbar.append({
                'type': 'link_pk',
                'label': '<i class="fas fa-sync"></i>',
                'title': 'Sincronizar Catalogo',
                'view': 'catalogoremotoconfiguracion_sinchronize',
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
    titulo = "Catalogo Remoto (Configuración)"
    model_name = "catalogoremotoconfiguracion"
    base_data_form = base_form
    tereapp = 'administrar'


class Update(GenericUpdate):
    titulo = "Catalogo Remoto (Configuración)"
    model_name = "catalogoremotoconfiguracion"
    base_data_form = base_form
    main_data_model = main_model
    tereapp = 'administrar'


class Delete(GenericDelete):
    model_name = "catalogoremotoconfiguracion"
    main_data_model = main_model
    tereapp = 'administrar'


class Sincronizar(View):
    model_name = "catalogoremotoconfiguracion"
    main_data_model = main_model

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        response = requests.get(obj.url_list)
        if response.status_code == 200:
            json_response = response.json()
            if len(json_response['dirs']) > 0:
                for dir, content in json_response['dirs'].items():
                    catalogo = CatalogoRemoto.objects.get_or_create(
                        nombre=dir.upper(),
                        url_listado_raiz=main_model.check_url_form(
                            obj.url_script_sitio + '?' +
                            obj.comando_mostrar + "&" +
                            obj.raiz_de_listado + '/' + dir),
                        configuracion=obj,
                    )[0]
                    catalogo.create_parametro_usuario()
                    self.generate_items(
                        content, catalogo, catalogo.url_listado_raiz,
                        obj.ruta_movil_de_archivo, obj.elemento_thumbnail)
            if len(json_response['files']) > 0:
                catalogo = CatalogoRemoto.objects.get_or_create(
                    nombre=f"{obj}".upper(),
                    url_listado_raiz=main_model.check_url_form(
                        obj.url_script_sitio + '?' +
                        obj.comando_mostrar + "&" +
                        obj.raiz_de_listado),
                    configuracion=obj,
                )[0]
                catalogo.create_parametro_usuario()
                self.generate_items(
                    {'files': json_response['files'], 'dirs': list()},
                    catalogo, catalogo.url_listado_raiz,
                    obj.ruta_movil_de_archivo, obj.elemento_thumbnail)
        else:
            print(f"{obj} -> {obj.url_list}")
            print(f"Response {response.status_code}: {response.reason}")
            print(response.text)
        return HttpResponseRedirect(reverse(
            f'{self.model_name}_read',
            kwargs={'pk': obj.pk}))

    def generate_items(
            self, dir_obj: dict, catalogo: CatalogoRemoto, rooturl: str,
            ruta_movil: str, thumbnail: str) -> None:
        for file in dir_obj['files']:
            url_file = main_model.check_url_form(
                rooturl + "&" + ruta_movil + file)
            url_file_thumbnail = main_model.check_url_form(
                url_file + "&" + thumbnail)
            response = requests.get(url_file_thumbnail)
            if response.status_code == 200:
                if "image" not in response.headers.get('Content-Type', ''):
                    url_file_thumbnail = url_file
                Item.objects.get_or_create(
                    catalogo=catalogo,
                    nombre=".".join(file.split('.')[:-1]),
                    mimetype=response.headers.get('Content-Type', ''),
                    url=url_file,
                    url_thumbnail=url_file_thumbnail,
                )
        if len(dir_obj['dirs']):
            for dir, content in dir_obj['dirs'].items():
                self.generate_items(
                    content, catalogo,
                    rooturl + "/" + dir, ruta_movil, thumbnail)


class Display(View):
    model_name = "catalogoremotoconfiguracion"
    base_data_form = base_form
    main_data_model = main_model
    tereapp = 'catalogo_remoto'
    html_template = template_base_path("display")

    def get(self, request, pk=None):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj)
        toolbar = None
        return render(request, self.html_template, {
            'titulo': obj,
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


class DisplayItems(View):
    model_name = "catalogoremoto"
    main_data_model = CatalogoRemoto
    tereapp = 'catalogo_remoto'
    html_template = template_base_path("display_items")

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        toolbar = [{'type': 'search'}]
        search_value = ParametroUsuario.get_valor(
            request.user, 'basic_search', f'catalogoremoto_{pk}')
        if '' == search_value:
            items = list(obj.items.all())
        else:
            items = list(obj.items.filter(
                Q(nombre__icontains=search_value) |
                Q(mimetype__icontains=search_value) |
                Q(url__icontains=search_value)))
        return render(request, self.html_template, {
            'titulo': obj,
            'toolbar': toolbar,
            'footer': False,
            'read_only': True,
            'alertas': [],
            'req_chart': False,
            'search_value': search_value,
            'tereapp': self.tereapp,
            'object': obj,
            'withoutBtnSave': True,
            'items': items,
        })

    def post(self, request, pk):
        if "search" == request.POST.get('action', ''):
            search_value = request.POST.get('valor', '')
            ParametroUsuario.set_valor(
                request.user,
                'basic_search', f'catalogoremoto_{pk}', search_value)
        return self.get(request, pk)


class ReadCatalogo(GenericRead):
    titulo_descripcion = "Catalogo Remoto"
    model_name = "catalogoremoto"
    base_data_form = frmCatalogo
    main_data_model = CatalogoRemoto
    tereapp = 'administrar'
    html_template = template_base_path("read_catalogo")

    def get(self, request, pk):
        if not self.main_data_model.objects.filter(pk=pk).exists():
            return HttpResponseRedirect(reverse('item_no_encontrado'))
        obj = self.main_data_model.objects.get(pk=pk)
        form = self.base_data_form(instance=obj)
        toolbar = []
        if request.user.has_perm(
                f"app_catalogo_remoto.view_catalogoremotoconfiguracion"):
            toolbar.append({
                'type': 'link_pk',
                'view': f'catalogoremotoconfiguracion_read',
                'pk': obj.configuracion.pk,
                'label': crud_icon('list'),
                'title': 'Ver configuracion del Catalogo'})
        if request.user.has_perm(
                f"app_catalogo_remoto.delete_catalogoremoto"):
            toolbar.append({
                'type': 'link_pk_del',
                'view': f'catalogoremotoconfiguracion_delete_catalogo',
                'pk': obj.pk,
                'label':  crud_icon('delete'),
                'title': crud_label('delete')})
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


class DeleteCatalogo(GenericDelete):
    model_name = "catalogoremoto"
    main_data_model = CatalogoRemoto
    tereapp = 'administrar'

    def get(self, request, pk):
        cc_pk = self.main_data_model.objects.get(pk=pk).configuracion.pk
        try:
            super().get(request, pk)
        except NoReverseMatch:
            pass
        return HttpResponseRedirect(reverse(
            'catalogoremotoconfiguracion_read', kwargs={'pk': cc_pk}))


class DeleteItem(GenericDelete):
    model_name = "catalogoremoto"
    main_data_model = Item
    tereapp = 'administrar'

    def get(self, request, pk):
        c_pk = self.main_data_model.objects.get(pk=pk).catalogo.pk
        try:
            super().get(request, pk)
        except NoReverseMatch:
            pass
        return HttpResponseRedirect(reverse(
            'catalogoremotoconfiguracion_read_catalogo', kwargs={'pk': c_pk}))
