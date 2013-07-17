# Api :: Minidicionario Hedra

## Pré-requisitos
* MongoDB
* Python
    * Flask
    * Flask-PyMongo

## Instalando
* Clone o repositorio
* Arrume as configurações do arquivo `settings.py-local` e salve-o como `settings.py`
* Rode o `script.py` para gerar o json.
* Rode o 'mongoimport -d hedra -c saotome --jsonArray --file saotome.json' para importar os verbetes
* Rode o `server.py`
