import re
import json
import pymongo
from settings import *

def parse_verbetes(filename='VERBETES.tex'):
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

