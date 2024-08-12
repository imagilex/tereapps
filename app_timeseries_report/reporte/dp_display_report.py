import pandas as pd
import plotly.express as px

from dash import Input
from dash import Output
from dash import dcc
from dash import html
from django_plotly_dash import DjangoDash
from plotly.subplots import make_subplots

from .models import ReporteTS

import app_timeseries_report.reporte.dp_config as dp_config

pk_reportets = dp_config.pk_reportets
reportets = ReporteTS.objects.get(pk=pk_reportets)
df = pd.DataFrame(list(reportets.registros.all().values()))

app = DjangoDash('DP_Display_ReporteTS', update_title='Actualizando gráfica')

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Label("Concepto:"),
                dcc.Dropdown(
                    reportets.conceptos, multi=True,
                    id="filter-concepto",
                    value=[reportets.concepto_predefinido, ],
                    placeholder="Seleccionar uno o varios conceptos")
            ], className="form-group"),
        ], className="col-sm-8"),
        html.Div([
            html.Div([
                html.Label("Entidades:"),
                dcc.Checklist([
                    {'label': f' {ent}', 'value': ent}
                    for ent in reportets.entidades
                    ], id="mostar-entidades", value=[
                        ent for ent in reportets.entidades]),
                html.Hr(),
                dcc.Checklist([{
                    'label': ' Gráficas independientes',
                    'value': 'independiente'
                }], id="multi-graph", value='independiente')
            ], className="form-group"),
        ], className="col-sm-4"),
    ], className="row"),
    html.Div([
        html.Div([
            dcc.Graph(id="graph", config={'displaylogo': False}, figure={}),
            ], className="col-sm-12"),
    ], className="row"),
])


@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='filter-concepto', component_property='value'),
    Input(component_id='mostar-entidades', component_property='value'),
    Input(component_id='multi-graph', component_property='value'),
    background=True
)
def update_mostar_entidades_value(conceptos, entidades, multiple):
    if conceptos is None or entidades is None:
        return {}
    if len(conceptos) == 0 or len(entidades) == 0:
        return {}
    entidades = ['TOTAL', ] + entidades
    df_totals = df.groupby(
        ['concepto', 'tipo', 'periodo', ]
        ).aggregate('sum').reset_index()[
            ['concepto', 'tipo', 'periodo', 'valor', ]]
    df_totals['id'] = 0
    df_totals['reporte_id'] = 0
    df_totals['entidad'] = 'TOTAL'
    df_totals = df_totals[list(df.columns)]
    df_tmp = pd.concat([df, df_totals])
    df_tmp = df_tmp[df_tmp['concepto'].isin(conceptos)]
    df_tmp = df_tmp[df_tmp['entidad'].isin(entidades)]
    df_tmp['Leyenda'] = df_tmp['concepto'] + ' - ' + df_tmp['tipo']
    if multiple and len(multiple) > 0 and "independiente" in multiple:
        cols = 2
        dims_amt = len(entidades) - 1
        rows = int((dims_amt - dims_amt % 2) / 2 + 1)
        num_series = len(conceptos) * len(df['tipo'].unique())
        fig = make_subplots(
            cols=cols, rows=rows,
            subplot_titles=[ent for ent in entidades])
        for idx, ent in enumerate(entidades):
            df_ent = df_tmp[df_tmp['entidad'] == ent]
            fig.add_traces(
                px.line(
                    df_ent, x='periodo', y='valor',
                    color='Leyenda'
                    )['data'],
                rows=[int((idx - idx % 2) / 2 + 1), ] * num_series,
                cols=[idx % 2 + 1, ] * num_series)
    else:
        df_tmp['Leyenda'] = df_tmp['entidad'] + ' - ' + df_tmp['Leyenda']
        fig = px.line(
            df_tmp, x='periodo', y='valor',
            color='Leyenda'
            )
    return fig
