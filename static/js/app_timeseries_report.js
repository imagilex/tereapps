let multi_select_control = null;
const COLORS = [
    // '#0d0887', '#d8576b',
    // '#46039f', '#ed7953',
    // '#7201a8', '#fb9f3a',
    // '#9c179e', '#fdca26',
    // '#bd3786', '#f0f921'
    'rgb(193, 118, 111)',
    'rgb(234, 79, 136)',
    'rgb(92, 83, 165)',
    'rgb(56, 178, 163)',
    'rgb(227,26,28)',
    'rgb(189,189,189)',
    'rgb(78,179,211)',
    'rgb(255,234,0)',
    'rgb(84, 31, 63)',
    'rgb(192, 54, 157)',
    'rgb(159, 130, 206)',
    'rgb(169, 220, 103)',
    'rgb(239,59,44)',
    'rgb(115,115,115)',
    'rgb(0,152,255)',
    '#dd2bfd',
    'rgb(135, 44, 162)',
    'rgb(178,24,43)',
]

$(document).ready(() => {
    if($(`#data-graph-ts_report`).length > 0) {

        jQuery.ajax({
            url: 'https://d3js.org/d3.v7.min.js',
            dataType: 'script',
            async: true,
        });

        jQuery.ajax({
            url: url_js,
            dataType: 'script',
            success: () => {
                $.ajax({
                    dataType: 'css',
                    url: url_css,
                    success: (data) => {
                        $("<style>").appendTo("head").html(data);
                    },
                    error: (jqXHR, textStatus, errorThrown) => {
                        if(jqXHR.status == 200) {
                            $("<style>").appendTo("head").html(jqXHR.responseText);
                        }
                        else {
                            console.log(`Error en llamada a ${url_css}`);
                            console.log(jqXHR);
                            console.log(textStatus);
                            console.log(errorThrown);
                        }
                    },
                    cache: false
                })
            },
            async: true
        });

        let chkReadyState = setInterval(() => {
            if(document.readyState == "complete") {
                multi_select_control = new MultiSelect(
                    document.getElementById('data-concepto'), {
                        onChange: createDataGraphs,
                    });
                clearInterval(chkReadyState);
                init_data();
            }
        }, 100);

    }
});

let createDataTotals = () => {
    let data_totals = Array();
    let dr_totals = d3.rollup(
        data,
        v => d3.sum(v, d => d.valor),
        d => d.concepto, d => d.tipo, d => d.periodo);
    dr_totals.keys().forEach( concepto => {
        let map_concepto = dr_totals.get(concepto);
        map_concepto.keys().forEach( tipo => {
            let map_tipo = map_concepto.get(tipo);
            map_tipo.keys().forEach( periodo => {
                let valor = map_tipo.get(periodo);
                data_totals.push({
                    id: 0, reporte_id: 0, entidad: 'TOTAL',
                    concepto, tipo, periodo,
                    valor
                })
            });
        });
    });
    return data_totals;
}

let init_data = () => {
    data = data.concat(createDataTotals());
    createDataGraphs();
}

let filterData = (entidades, conceptos) => {
    let data_ent = Array();
    let data_conc = Array();
    for(let entidad of entidades) {
        data_ent = data_ent.concat(
            data.filter(d => d.entidad == entidad));
    }
    for(let concepto of conceptos) {
        data_conc = data_conc.concat(
            data_ent.filter(d => d.concepto == concepto));
    }
    return data_conc;
}

let createDataGraphs = () => {
    $(`#data-graph-ts_report`).html('');
    let entidades = Array.from(document.querySelectorAll(
        `input[name="data-entidad[]"]`).entries().filter(
            item => item[1].checked ).map( item => item[1].value ));
    let multiple = document.querySelector(
        `input[name="data-multiple"]`).checked;
    let conceptos = multi_select_control.selectedValues;
    if(conceptos.length == 0 || entidades.length == 0) {
        return
    }
    entidades = ('TOTAL,' + entidades.join(',')).split(',');
    let data_tmp = filterData(entidades, conceptos).map( d => ({
        ...d,
        multi_leyenda: (
            conceptos.length > 1
            ? `${d.concepto} - ${d.tipo}`
            : `${d.tipo}`),
        leyenda: (
            conceptos.length > 1
            ? `${d.entidad} - ${d.concepto} - ${d.tipo}`
            : `${d.entidad} - ${d.tipo}`)
    }));
    let graph_options = {
        scales: {yAxes: [
            {ticks: {beginAtZero: true}}]}};
    let periodos = Array.from(d3.group(data_tmp, d => d.periodo).keys());
    if(multiple) {
        for(let entidad of entidades) {
            $(`
                <div class="col-sm-6">
                    <p class="h6 text-center">${entidad}</p>
                    <canvas id="data-graph-${entidad}"></canvas>
                </div>
            `).appendTo($(`#data-graph-ts_report`));
            let datasets = Array();
            let data_entidad = data_tmp.filter(d => d.entidad == entidad);
            let dr_series = d3.group(
                data_entidad,
                d => d.multi_leyenda, d => d.periodo);
            let series = Array.from(dr_series.keys());
            for(let idx_serie in series) {
                let serie = series[idx_serie];
                let dr_serie = dr_series.get(serie);
                let datos = Array();
                for(let p of periodos) {
                    let valor = dr_serie.get(p);
                    datos.push(valor ? valor[0].valor : 0);
                }
                datasets.push({
                    label: serie,
                    data: datos,
                    fill: false,
                    borderColor: COLORS[idx_serie % COLORS.length],
                    backgroundColor: COLORS[idx_serie % COLORS.length],
                    borderWidth: 2,
                    radius: 0
                });
            }
            let context = document.getElementById(
                `data-graph-${entidad}`).getContext('2d');
            let chart_obj = new Chart(context, {
                "type": "line",
                "data": {
                    "options": graph_options,
                    "labels": periodos,
                    "datasets": datasets
                }
            });
        }
    } else {
        $(`
            <div class="col-sm-12">
                <canvas id="data-graph-unique"></canvas>
            </div>
        `).appendTo($(`#data-graph-ts_report`));
        let datasets = Array();
        let dr_series = d3.group(
            data_tmp,
            d => d.leyenda, d => d.periodo);
        let series = Array.from(dr_series.keys());
        for(let idx_serie in series) {
            let serie = series[idx_serie];
            let dr_serie = dr_series.get(serie);
            let datos = Array();
            for(let p of periodos) {
                let valor = dr_serie.get(p);
                datos.push(valor ? valor[0].valor : 0);
            }
            datasets.push({
                label: serie,
                data: datos,
                fill: false,
                borderColor: COLORS[idx_serie % COLORS.length],
                backgroundColor: COLORS[idx_serie % COLORS.length],
                borderWidth: 2,
                radius: 0
            });
        }
        let context = document.getElementById(
            'data-graph-unique').getContext('2d');
        new Chart(context, {
            "type": "line",
            "data": {
                "options": graph_options,
                "labels": periodos,
                "datasets": datasets
            }
        });
    }
}
