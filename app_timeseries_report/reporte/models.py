from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

from zend_django.models import MenuOpc


class ReporteTS(models.Model):
    nombre = models.CharField(max_length=250)
    concepto_predefinido = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ["nombre"]
        permissions = [
            ('update_report_by_hand', 'Actualizar Reporte Manual'),
            ('update_report_by_txt', 'Actualizar Reporte TXT'),
            ('update_report_by_xlsx', 'Actualizar Reporte XLSX'),
        ]

    def __str__(self) -> str:
        return self.nombre

    def get_distinct_regs(self, field):
        values = self.registros.all().order_by(
            field).distinct().values(field)
        vals = list([val[field] for val in values])
        return vals

    @property
    def entidades(self):
        return self.get_distinct_regs('entidad')

    @property
    def conceptos(self):
        return self.get_distinct_regs('concepto')

    @property
    def periodos(self):
        return self.get_distinct_regs('periodo')

    @property
    def tipos(self):
        return self.get_distinct_regs('tipo')

    def save(self, *args, **kwars):
        res = super().save(*args, **kwars)
        pk = self.pk
        mnu_padre = MenuOpc.objects.get(
            nombre="Nómina", vista="idx_app_timeseries_report")
        mnu_opc = MenuOpc.objects.get_or_create(
            vista=f'reportets_display_{pk}',
            padre=mnu_padre, posicion=1)[0]
        mnu_opc.nombre = self.nombre
        mnu_opc.save()
        perm = Permission.objects.get_or_create(
            content_type=ContentType.objects.get(
                app_label='app_timeseries_report',
                model='reportets'),
            codename=f'view_reportets_{pk}'
            )[0]
        perm.name = f'Ver Reporte {self.nombre}'
        perm.save()
        mnu_opc.permisos_requeridos.add(perm)

        return res

    def delete(self, *args, **kwars):
        pk = self.pk
        res = super().delete(*args, **kwars)
        MenuOpc.objects.get(
            nombre=self.nombre,
            vista=f'reportets_display_{pk}').delete()
        Permission.objects.get(
            codename=f'view_reportets_{pk}'
            ).delete()
        return res
