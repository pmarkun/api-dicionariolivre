import re
import json
import pyes, pprint
#from settings import *

def parse_verbetes(filename='data/VERBETES.tex'):
	verbetes_raw = open(filename, 'r').read()

	italic = re.compile(r'\\textit{(.*?)}')
	bold = re.compile(r'\\textbf{(.*?)}')
	turna = re.compile(r'{\\textturna}')
	verb = re.compile(r"\\verb{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}")

	verbetes_raw = verbetes_raw.replace("\n", "")
	verbetes_raw = re.sub(italic, "*\\1*", verbetes_raw)
	verbetes_raw = re.sub(bold, "*\\1*", verbetes_raw)
	verbetes_raw = re.sub(turna, "", verbetes_raw)

	verbetes = []
	for v in re.findall(verb, verbetes_raw):
		verbete = {}
		verbete['lexema'] = v[0]
		verbete['fonetica'] = v[2]
		verbete['gramatical'] = v[3]
		verbete['equivalencia'] = [v[6]]
		verbete['outros'] = v[7]
		verbetes.append(verbete)

	entradas = []
	for v in verbetes:
		bingo = False
		for e in entradas:
			if v['lexema'] == e['lexema'] and v['fonetica'] == e['fonetica'] and v['gramatical'] == e['gramatical']:
				e['equivalencia'].append(v['equivalencia'][0])
				bingo = True
		if not bingo:
			entradas.append(v)
	return entradas

def write_verbetes(entradas, filename):
	arquivo = open(filename, 'w')
	arquivo.write(json.dumps(entradas, sort_keys=True, indent=4, separators=(',', ': ')))
	arquivo.close()


def upa_neguim(verbetes):
	print 'Connecting to ES...'
	conn = pyes.ES('http://127.0.0.1:9200')
	try:
		print 'Creating index...'
		conn.indices.create_index("dicionario")
	except:
		pass

	mapping = {
    	}

	print 'Mapping...'
	conn.indices.put_mapping("verbete", {'properties': mapping}, ["dicionario"])
    
	erros = 0
	print 'Indexing!'
	for p in verbetes:
		#p = verbetes[v]
		try:
			conn.index(p, 'dicionario', 'verbete', bulk=True)
		except:
			print "erro"
			erros = erros + 1
	print erros

verbetes =  parse_verbetes();
upa_neguim(verbetes);