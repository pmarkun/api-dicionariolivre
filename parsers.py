import re
import codecs

def saotome(filename='data/saotome/VERBETES.tex'):
    verbetes_raw = codecs.open(filename, 'r', encoding='utf-8').read()

    emph = re.compile(r'\\emph{(.*?)}') 
    italic = re.compile(r'\\textit{(.*?)}')
    bold = re.compile(r'\\textbf{(.*?)}')
    turna = re.compile(r'{\\textturna}')
    verb = re.compile(r"\\verb{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}")
    tilda = re.compile(r"\\\~[{]{0,1}(.)[}]{0,1}")
    verbetes_raw = verbetes_raw.replace("\n", " ")
    verbetes_raw = re.sub(turna, u"\u0250", verbetes_raw)
    verbetes_raw = re.sub(tilda, r'\1'+u"\u0303", verbetes_raw)
    verbetes_raw = re.sub(italic, "*\\1*", verbetes_raw)
    verbetes_raw = re.sub(emph, "*\\1*", verbetes_raw)
    verbetes_raw = re.sub(bold, "*\\1*", verbetes_raw)
    verbetes = []
    for v in re.findall(verb, verbetes_raw):
        verbete = {}
        verbete['lexema'] = v[0]
        if len(verbete['lexema'].split('-')) > 1:
            verbete['_boost'] = 0.5
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