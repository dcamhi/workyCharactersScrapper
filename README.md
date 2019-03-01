# Python Scrapper using Selenuim and mongoDB


## Scrapper de información y almacenamiento en base de datos

El scrapper está construido en Python utilizando Flask. La base de datos es una basada en documentos, actualmente mongoDB. El scrapper se desarrolló utilizando Selenium.

##### Requerimentos

```powershell
- Git
- Python 3
- Virtualenv
- Google ChromeDriver
```

##### Instalación

```powershell
git clone https://github.com/dcamhi/workyCharactersScrapper.git
cd workyCharactersScrapper
virtualenv envScrapper
source ../envScrapper/bin/activate
pip install -r requirements.txt
touch .env
python manage.py runserver
```


## A continuación se describen los archivos del proyecto.

### /config.py

##### Configuración de variables de ambiente, se necesitan las siguientes variables en el .env:

```powershell
DEBUG_VAR = os.environ.get("DEBUG_VAR")
dbName = os.environ.get("dbName")
dbUrl = os.environ.get("dbUrl")
```

### /settings.py
##### Configuración de flask

### /manage.py
##### Creación de la aplicación de flask y encendido de el servidor con el ambiente predefinido

```powershell
debug = config.DEBUG
host = os.getenv('IP', '0.0.0.0')
port = int(os.getenv('PORT', 8080))

app = create_app(debug)
manager = Manager(app)

manager.add_command("ci", CICommand(settings))
manager.add_command("runserver", Server(
    use_debugger=debug,
    use_reloader=debug,
    host=host,
    port=port
))
```
### /application.py
##### Definición de la aplicación, los blueprints y las rutas

### characters/api.py

##### Aquí se encuentra el código del scrapper como tal.

```powershell
Ver el código (todo está comentado y documentado)
```

Para dudas contactar a [david.camhi26@gmail.com](mailto:david.camhi26@gmail.com)
