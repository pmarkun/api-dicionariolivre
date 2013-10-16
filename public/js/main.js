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
var edita = function(id, value, settings) { 
        $("#"+id+ " .save").click(function (e) {
            console.log(id);
            save_modal(id);
        });
        $("#"+id+ " .save").show();
        return(value);   
    }

var save_modal = function(id) {
    var url_get = SETTINGS['SERVER'] + SETTINGS['COLECOES'].join(',') + '/verbete/';
    $.getJSON(url_get+id, function (data) {
        var palavra = data['_source'];
        palavra['equivalencia'] = [];
        $("#"+id +" .equivalencia").each(function (index, item) {
            if (item.textContent != 'Click to edit') {
                palavra['equivalencia'].push(item.textContent);
            }
            else {
                $(item).remove();
            }
        });
        SETTINGS['buffer'] = {
            'id' : id,
            'palavra' : palavra
        };
    
        if (SETTINGS['buffer']) {

            var url = SETTINGS['SERVER'] + SETTINGS['COLECOES'].join(',') + '/verbete/';
            /*
            $.post(url+id+"/", JSON.stringify(palavra), function (result) {
                console.log(result);
            });
            */
            sugestao.render(SETTINGS['buffer']['palavra']);
            console.log(SETTINGS['buffer']['palavra']);
            $("#save_form").modal('show');
            $("#save").click(function (e) {
                save()
            });
            Recaptcha.create(SETTINGS['RECAPTCHA_PUBLIC'], "recaptcha_div", {
                theme: "red",
                callback: Recaptcha.focus_response_field
            });
            $("#"+id+ " .save").hide();
        }
    });
}

var save = function() {
    var url = SETTINGS['SERVER'] + SETTINGS['COLECOES'].join(',') + '/verbete/';
    var id = SETTINGS['buffer']['id'];
    var palavra = SETTINGS['buffer']['palavra'];
    var post_ops = {
        'id' : id,
        'palavra' : palavra,
        'recaptcha_challenge_field' : Recaptcha.get_challenge(),
        'recaptcha_response_field' : Recaptcha.get_response(),
        'colecoes' : SETTINGS['COLECOES'].join(',')
    }
    $.post("/s/server.php", post_ops, function (result) {
        var r = jQuery.parseJSON(result);
        if (r["ok"]) {
        SETTINGS['buffer'] = {};
        $("#save_form").modal('hide');
        $("#complete").modal('show');
        }
        else {
            console.log(r);
        }
    });
}

var refreshedit = function () {
    $('.editable').editable(function (value, settings) {
        var id = $(this.parentElement.parentElement)[0].id;
        return edita(id, value, settings)
    },
    {
        style   : 'display: inline;width:80%'
    });

    $(".add").click(function (e) {
            var equiv = $(e.target.parentElement).find("ol");
            equiv.append('<li class="equivalencia editable"></li>');
            $('.editable').editable(function (value, settings) {
                var id = $(this.parentElement.parentElement)[0].id;
                return edita(id, value, settings)
            },
            {
                style   : 'display: inline;width:80%'
            });

    });
    $(".add").toggleClass("empty");
    }

function render(q) {
        $.getJSON(SETTINGS['SERVER'] + SETTINGS['COLECOES'].join(',') + '/_search?source=' + JSON.stringify(q), function (data){
        $('.verbetes').fadeOut();
        if (data.hits.hits) {
            console.log(data);
            $("#verbetes").toggleClass("empty");
            $("#paginate").toggleClass("empty");
        }
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
            t['_source']['id'] = t['_id'];
            tempo.append(t['_source'])
        });
        if (SETTINGS['edit']) {
            refreshedit();
        }
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
    sugestao = Tempo.prepare("sugestao");
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

    $("#edit").click(function (e) {
        if (SETTINGS['edit']) {
            $("#edit").text("edit off");
            SETTINGS['edit'] = false;
        }
        else {
            $("#edit").text("edit on");
            SETTINGS['edit'] = true;
            refreshedit();
        }
    });
});
