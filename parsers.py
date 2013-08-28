import re
import codecs

def saotome(v):
    verbete = {}
    verbete['lexema'] = v[0]
    if len(verbete['lexema'].split('-')) > 1:
        verbete['_boost'] = 0.5
    verbete['fonetica'] = v[2]
    verbete['gramatical'] = v[3]
    verbete['equivalencia'] = [v[6]]
    verbete['outros'] = v[7]
    return verbete


def portugues(v):
    verbete = {}
    verbete['lexema'] = v[0]
    verbete['fonetica'] = v[1]
    verbete['rubrica'] = v[2]
    verbete['plural'] = v[3]
    verbete['feminino'] = v[4]
    verbete['gramatical'] = v[5]
    verbete['equivalencia'] = [v[6]]
    verbete['separacao'] = v[7]
    verbete['conjugacao'] = v[8]
    if len(verbete['lexema'].split('-')) > 1:
        verbete['_boost'] = 0.5
    return verbete

def portugues_preprocessor(verbetes_raw):
    verbetes_raw = verbetes_raw.replace('"-','-')
    verb = re.compile(r"\\verb{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}")
    bulk = re.findall(verb, verbetes_raw)
    verbetes_clean = ''
    for v in bulk:
        if v[5] != '':
            y = list(v)
            v_buffer = y[5]
        else:
            y = list(v)
            y[5] = v_buffer
        verbetes_clean += "\\verb{%s}{%s}{%s}{%s}{%s}{%s}{%s}{%s}{%s}" % tuple(y)
    return verbetes_clean

def parse(filename='data/saotome/VERBETES.tex', mapping=saotome, preprocessor=None):
    verbetes_raw = codecs.open(filename, 'r', encoding='utf-8').read()

    emph = re.compile(r'\\emph{(.*?)}') 
    italic = re.compile(r'\\textit{(.*?)}')
    bold = re.compile(r'\\textbf{(.*?)}')
    turna = re.compile(r'{\\textturna}')
    verb = re.compile(r"\\verb{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}{(.*?)}")
    tilda = re.compile(r"\\\~[{]{0,1}(.)[}]{0,1}")
    ellipsis = re.compile(r'\\ldots{}')
    verbetes_raw = verbetes_raw.replace("\n", " ")
    verbetes_raw = re.sub(turna, u"\u0250", verbetes_raw)
    verbetes_raw = re.sub(tilda, r'\1'+u"\u0303", verbetes_raw)
    verbetes_raw = re.sub(italic, "*\\1*", verbetes_raw)
    verbetes_raw = re.sub(emph, "*\\1*", verbetes_raw)
    verbetes_raw = re.sub(bold, "*\\1*", verbetes_raw)
    verbetes_raw = re.sub(ellipsis, u"\u2026", verbetes_raw)

    verbetes = []
    if preprocessor:
        verbetes_raw = preprocessor(verbetes_raw)
    for v in re.findall(verb, verbetes_raw):
        verbete = mapping(v)
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