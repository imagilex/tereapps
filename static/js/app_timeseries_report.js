let multi_select_control = null;

jQuery.ajax({
    url: url_js,
    dataType: 'script',
    success: () => {
        console.log(`Se ha cargado ${url_js}`);
        $.ajax({
            dataType: 'css',
            url: url_css,
            success: (data) => {
                $("<style>").appendTo("head").html(data);
                console.log(`Se ha cargado ${url_css}`);
            },
            error: (jqXHR, textStatus, errorThrown) => {
                if(jqXHR.status == 200) {
                    $("<style>").appendTo("head").html(jqXHR.responseText);
                    console.log(`Se ha cargado ${url_css}`);
                }
                else {
                    console.log(`Error en llamada a ${url_css}`);
                    console.log(jqXHR);
                    console.log(textStatus);
                    console.log(errorThrown);
                }
            },
            cache: false,
            complete: () => {
                multi_select_control = new MultiSelect(
                    document.getElementById('data-concepto'));
            }
        })
    },
    async: true
});
