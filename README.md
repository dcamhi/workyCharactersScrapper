# Python Scrapper using Selenuim and mongoDB


## API para conexión con base de datos y respuestas de chat

El scrapper está construido en Python utilizando Flask. La base de datos es una basada en documentos, actualmente mongoDB. El scrapper se desarrolló utilizando Selenium.


##### Instalación

```powershell
git clone https://github.com/dcamhi/workyCharactersScrapper.git
virtualenv envScrapper

source ../envResponses/bin/activate
pip3 install -r requirements.txt
python3 manage.py runserver
```

## Se tienen las siguientes funcionalidades con sus respectivos endpoints:

### 1. NODOS

##### Obtener todos los nodos y repsuestas

```powershell
GET /api/textResponses/ 
```

##### Obtener el nodo con el nid especificado

```powershell
GET /api/textResponses/<nid>
```

##### Insertar un nuevo registro

```powershell
POST /api/textResponses/ 
{
    "nid": "nid",
    "response":"respuesta"
}
```

##### Actualizar el nodo especificado

```powershell
PATCH /api/textResponses/nid 
{
    "nid": "nid",
    "response":"respuesta"
}
```

##### Eliminar el nodo especificado

```powershell
DELETE /api/textResponses/nid 
```

Para dudas contactar a [dcamhi@nearshoremx.com](mailto:dcamhi@nearshoremx.com)
