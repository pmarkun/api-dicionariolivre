SETTINGS = {};
SETTINGS['SERVER'] = 'http://127.0.0.1:9200/' 
q = {
        "query" : {
            "query_string" : { 
                "query" : '',
                "fields" : ["lexema"],
                "default_operator" : "AND"
            },
        "size":10
        }
    }

function procurar(palavra) {
    $(".resultados").attr("id", palavra);
    $("#hash").attr("href", "#"+palavra);
    window.location.hash = palavra;
    q['query']['query_string']['query'] = palavra;
    $.getJSON(SETTINGS['SERVER'] + 'dicionario/_search?source=' + JSON.stringify(q), function (data){
        $('.verbetes').fadeOut();
        tempo.clear();
        $.each(data.hits.hits, function (index, t) {
            console.log(t);
            tempo.append(t['_source'])
            

        });
    });
}
    
$(document).ready(function () {
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
