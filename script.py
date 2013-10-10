import json
import pyes
import parsers

def write_verbetes(entradas, filename):
	arquivo = open(filename, 'w')
	arquivo.write(json.dumps(entradas, sort_keys=True, indent=4, separators=(',', ': ')))
	arquivo.close()


def upa_neguim(verbetes, colecao='dicionario', reset=True):
	print 'Connecting to ES...'
	conn = pyes.ES('http://127.0.0.1:9200')
	
	if reset:
		conn.delete_index_if_exists(colecao)

	settings = {
		"analysis": {
			"analyzer": {
				"index_analyzer": {
					"tokenizer": "standard",
					"filter": ["standard", "lowercase", "asciifolding", "porter_stem"]
				},
				"search_analyzer": {
					"tokenizer": "standard",
					"filter": ["standard", "lowercase", "asciifolding", "porter_stem"]
				}
			},
		}
	}

	conn.indices.create_index_if_missing(colecao, settings=settings)

	mapping = {
			"equivalencia" : { 
				"type" : "multi_field",
				"fields" : {
					"clean" : {
						"type" : "string", 
						"index_analyzer" : "index_analyzer",
						"search_analyzer" : "search_analyzer"
					},
					"equivalencia" : {
						"type" : "string",
						"analyzer" : "standard"
					}
				}
			},
			"lexema" : { 
				"type" : "multi_field",
				"fields" : {
					"clean" : {
						"type" : "string", 
						"index_analyzer" : "index_analyzer",
						"search_analyzer" : "search_analyzer"
					},
					"lexema" : {
						"type" : "string",
						"analyzer" : "standard"
					}
				}
			}
    	}

	print 'Mapping...'
	conn.indices.put_mapping("verbete", {'properties': mapping}, [colecao])
	print 'Indexing!'
	for p in verbetes:
		conn.index(p, colecao, 'verbete', bulk=True)
	conn.refresh()

z = ['a', 'b','c','d', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z', 'w']

verbetes = []
for letra in z:
	print 'Verbeting ' + letra
	verbetes = verbetes + parsers.parse('data/portugues/'+letra+'.tex', parsers.portugues, parsers.portugues_preprocessor);

upa_neguim(verbetes, 'portugues', True);