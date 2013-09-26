$(document).ready(function () {
if (SETTINGS['SPEAK']) {
    var lq = {
        "query" : {
            "query_string" : { 
                "query" : '',
                "fields" : ["lexema^5", "lexema.clean^5"],
                "default_operator" : "AND"
            }
        },
        "size": 1,
        "from" : 0
    }

    meSpeak.loadConfig("/js/speak/mespeak_config.json");
    meSpeak.loadVoice('/js/speak/pt.json');

    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    //recognition.interimResults = true;
    recognition.lang = "pt-br";
    recognition.onresult = function (r) {
        console.log(r);
        var resultado = r.results[r.results.length-1][0].transcript;
        var defina_pos = resultado.indexOf('defina');
        if (defina_pos >= 0) {
            var busca = resultado.slice(defina_pos+6).trim();
            //console.log(resultado);
            //console.log(resultado.slice(defina_pos+6));
            lq['query']['query_string']['query'] = busca;
            $.getJSON(SETTINGS['SERVER'] + SETTINGS['COLECOES'].join(',') + '/_search?source=' + JSON.stringify(lq), function (data) {
                //console.log(data.hits.hits[0]['_source']['equivalencia'][0]);
                meSpeak.speak(data.hits.hits[0]['_source']['equivalencia'][0], { "lang" : "pt" });
            });
            procurar(busca);
            $("#buscar input").val(busca);
        }
    }
    recognition.onend = function() {
        recognition.start();
    }
    recognition.start();
}
});