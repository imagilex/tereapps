/**
 * APP_REPORTS functions
 */

let idnew = 0;

let Create_FieldRow = () => {
    let tbl = $("#data-tbl");
    let template = Handlebars.compile($("#field-form-line-template").html());
    let html = template({
        posicion: tbl[0].rows.length + 1,
        pk: "new_" + (idnew++),
    });
    tbl.append($(html));
}

let Delete_FieldRow = () => {
    let tbl = $("#data-tbl");
    tbl.find("tr td:first-child input").filter(function(){
        return this.checked}).each(function(idx, ckb) {
            if(ckb.value.indexOf('new_') == -1) {
                let current_fields = $("#deleted_fields").attr(
                    'value').split(',');
                current_fields.push(ckb.value);
                $("#deleted_fields").attr(
                    'value', current_fields.join(','))
            }
            $(ckb).parent().parent().remove();
        });
}

let Add2Tbl_FieldRow = (
    pk, posicion, campo, valor_default, mostrar, es_llave, tipo) => {
    let tbl = $("#data-tbl");
    let template = Handlebars.compile(
        $("#field-form-line-template").html());
    let html = template(
        {pk, posicion, campo, valor_default, mostrar, es_llave});
    tbl.append($(html));
    $(`#tipo_${pk} option`).each(function(idx, opt){
        opt.selected = opt.value == tipo;
    });
}

let App_Reports_load_bootstrapTable = () => {
    $.ajaxSetup({
        cache: true,
        timeout: 10*1000
    });
    $.getScript("https://unpkg.com/bootstrap-table@1.16.0/dist/bootstrap-table.min.js",function( data, textStatus, jqxhr ) {
        console.log(data);
        console.log(textStatus);
        console.log(jqxhr.status);
        console.log("Script Cargado: bootstrap-table.min.js");
        App_Reports_load_bootstrapTableToolbar();
        App_Reports_load_bootstrapTableLocaleAll();
    });
    $.ajaxSetup({
        cache: false,
    });
}

let App_Reports_load_bootstrapTableToolbar = () => {
    $.getScript("https://unpkg.com/bootstrap-table@1.16.0/dist/extensions/toolbar/bootstrap-table-toolbar.min.js",function( data, textStatus, jqxhr ) {
        console.log(data);
        console.log(textStatus);
        console.log(jqxhr.status);
        console.log("Script Cargado: bootstrap-table-toolbar.min.js");
    });
}

let App_Reports_load_bootstrapTableLocaleAll = () => {
    $.getScript("https://unpkg.com/bootstrap-table@1.16.0/dist/bootstrap-table-locale-all.min.js",function( data, textStatus, jqxhr ) {
        console.log(data);
        console.log(textStatus);
        console.log(jqxhr.status);
        console.log("Script Cargado: bootstrap-table-locale-all.min.js");
        let $table = $('#data-tbl-complete')
        $table.bootstrapTable();
        $table.bootstrapTable('refreshOptions', {
            locale: 'es-MX'
        });
    });
}

$(document).ready(()=>{
    try {
        AddRows_Fields();
    } catch (error) {}
    App_Reports_load_bootstrapTable();
});

let OpenFrmDataTypes_4fields = () => {
    let template = Handlebars.compile( $( "#frm-get_data_types-template" ).html() );
    let html = template({});
    App.openPanel(html, "Obtener Campos desde Archivo", true, null, "panel-types-form");
}

let GetDataTypes_4fields = () => {
    var formData = new FormData($("#types-form")[0]);
    $.ajax({
        url: urlGetCampos,
        type: "post",
        dataType: "json",
        data: formData,
        cache: false,
        contentType: false,
        processData: false
    }).done(function(data){
        let tbl = $("#data-tbl");
        data.forEach((element) => {
            let tipo;
            if(element.type.toLowerCase().indexOf('object')>-1) {
                tipo = 'STRING';
            } else if(element.type.toLowerCase().indexOf('float')>-1) {
                tipo = 'DECIMAL';
            } if(element.type.toLowerCase().indexOf('int')>-1) {
                tipo = 'INTEGER';
            } 
            Add2Tbl_FieldRow(
                "new_" + (idnew++),
                tbl[0].rows.length + 1,
                element.col,
                '', true, false,
                tipo
                )
        });
    });


    App.closePanel("panel-types-form");
}
