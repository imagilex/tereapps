"""
Definición de modelos de Puesto

Modelos
-------
- Puesto
- PuestoEvaluacion
"""
from django.db import models

from zend_django.models import ParametroSistema

from .parametrovp_models import ParametroVP
from .tabulador_models import Tabulador


def get_next_posicion_puesto() -> int:
    max = Puesto.objects.aggregate(models.Max('posicion'))
    try:
        return max['posicion__max'] + 1
    except TypeError:
        return 1


class Puesto(models.Model):
    """
    Modelo de Puestos
    """
    puesto = models.CharField(max_length=200, unique=True)
    posicion = models.PositiveSmallIntegerField(
        default=get_next_posicion_puesto)
    estatus = models.BooleanField(default=True)
    tabulador = models.ForeignKey(
        Tabulador, on_delete=models.PROTECT, related_name="+")

    class Meta:
        ordering = ['posicion', 'puesto']
        permissions = [
            ('view_fp_puntos', 'Reporte Factores por Puesto - Puntos'),
            ('view_fp_niveles', 'Reporte Factores por Puesto - Niveles'),
            ('view_vp', 'Reporte Valor por Puesto'),
            ('view_gp', 'Grafica de Puestos'),
            ('view_gp_pesos', 'Grafica de Puestos en pesos'),
        ]

    def __str__(self):
        return self.puesto

    __ponderacion_total__ = None
    __ponderacion_total_en_pesos__ = None
    __tabuladores__ = None

    @property
    def ponderacion_total(self) -> float:
        if not self.__ponderacion_total__:
            total = 0.0
            for nivel in self.niveles_ponderacion.all():
                total += nivel.ponderacion
            self.__ponderacion_total__ = total
        return self.__ponderacion_total__

    @property
    def ponderacion_total_en_pesos(self) -> float:
        if not self.__ponderacion_total_en_pesos__:
            vp = float(ParametroVP.objects.get(parametro='ValorPunto').valor)
            dias = float(ParametroSistema.get(
                'AppValuacionPuestos', 'DiasPorMes'))
            self.__ponderacion_total_en_pesos__ = self.ponderacion_total * \
                vp * dias
        return self.__ponderacion_total_en_pesos__

    @property
    def ponderacion_total_en_pesos_diario(self) -> float:
        return self.ponderacion_total_en_pesos / 30

    @property
    def tabuladores(self) -> list:
        if not self.__tabuladores__:
            tabs = []
            for nivel in self.tabulador.niveles.all():
                tabs.append({
                    'nivel': nivel,
                    'puntos': self.ponderacion_total *
                    float(nivel.porcentaje) / 100,
                    'pesos': self.ponderacion_total_en_pesos *
                    float(nivel.porcentaje) / 100,
                    'pesos_diario': self.ponderacion_total_en_pesos_diario *
                    float(nivel.porcentaje) / 100,
                })
            self.__tabuladores__ = tabs
        return self.__tabuladores__


class PuestoEvaluacion(models.Model):
    """
    Modelo para salvar evaluaciones del puesto
    """
    puesto = models.ForeignKey(
        Puesto, on_delete=models.CASCADE, related_name='evaluaciones')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    data = models.TextField()
    nombre = models.CharField(max_length=200)

    class Meta:
        ordering = ['puesto', '-updated', ]

    def __str__(self):
        return f"{self.puesto} ({self.updated:%Y-%m-%d %H:%M})"
