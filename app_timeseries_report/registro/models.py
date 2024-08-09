from django.db import models

from app_timeseries_report.reporte.models import ReporteTS

TIPO_REGISTRO = (
    ('D', 'Detalle'),
    ('P', 'Promedio'),
)


class RegistroTS(models.Model):
    reporte = models.ForeignKey(
        ReporteTS, on_delete=models.CASCADE,
        related_name="registros")
    entidad = models.CharField(max_length=250)
    concepto = models.CharField(max_length=250)
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_REGISTRO, default=TIPO_REGISTRO[0][0])
    periodo = models.DateField()
    valor = models.IntegerField(default=0)

    class Meta:
        ordering = [
            "entidad",
            "concepto",
            "tipo",
            "periodo",
        ]
