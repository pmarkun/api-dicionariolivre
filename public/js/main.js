q = {
        "query" : {
            "query_string" : { 
                "query" : '',
                "fields" : ["lexema^5", "lexema.clean^5", "equivalencia", "equivalencia.clean"],
                "default_operator" : "AND"
            }
        },
        "size": 3,
        "from" : 0
    }

var paginacao = function(direcao, q) {
    if (direcao == 'mais') { 
        q['from'] = q['from'] + q['size'];
    }
    else if (direcao == 'menos') {
        if (q['from']-q['size'] >= 0) {
            q['from'] = q['from'] - q['size'];
        }
    }
    return q;
}

function render(q) {
        $.getJSON(SETTINGS['SERVER'] + SETTINGS['COLECOES'].join(',') + '/_search?source=' + JSON.stringify(q), function (data){
        $('.verbetes').fadeOut();
        if (q['from']+q['size'] >= data.hits.total) {
            $("#paginate .mais").hide();
        }
        else {
            $("#paginate").show();
            $("#paginate .mais").show();   
        }

        if (q['from'] == 0) {
            $("#paginate .menos").hide();
        }
        else {
            $("#paginate .menos").show();
        }

        tempo.clear();
        if (data.hits.hits.length == 0) {
            tempo.append({ "lexema" : "Verbete não encontrado."});
        }
        $.each(data.hits.hits, function (index, t) {
            console.log(t);
            tempo.append(t['_source'])
        });
    });
}
function procurar(palavra) {
    $(".resultados").attr("id", palavra);
    $("#hash").attr("href", "#"+palavra);
    window.location.hash = palavra;
    q['from'] = 0;
    q['query']['query_string']['query'] = palavra;
    render(q);
}
 
$(document).ready(function () {
    $("#titulo").text(SETTINGS['TITULO']);
    $("title").text(SETTINGS['TITULO']);
    tempo = Tempo.prepare("verbetes");
    if (window.location.hash) {
        var palavra = window.location.hash.slice(1);
        $("#buscar input").val(palavra);
        procurar(palavra);
    }

    $("#buscar button").click(function () {
        var palavra = $("#buscar input").val();
        procurar(palavra);
        return false;
    });

});
