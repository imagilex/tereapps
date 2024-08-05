from zend_django.views import GenericTereAppRootView


class TimeSeriesReportsView(GenericTereAppRootView):
    html_template = "zend_django/idx_empty.html"
    titulo = "Reportes"
    titulo_descripcion = ""
    toolbar = None
    tereapp = 'timeseries_report'
