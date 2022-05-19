<img src="static/logo.png" width=180px>

<img src="https://github.com/aleen42/badges/blob/master/src/python.svg">
<img src="https://github.com/aleen42/badges/blob/master/src/docker.svg">
<img src="https://img.shields.io/badge/Version-4.0-brightgreen">
<img src="https://img.shields.io/badge/Maintained%3F-yes-blue.svg">

---------

Versión actual: v4.0.0 desarrollada por [@alechilczenko]()

> Nota: Las imágenes de Docker se publicarán en las próximas semanas.

## Tabla de contenidos
* [Guía](#Guia)
  * [Inglés]()
  * [Español]()
* [Introducción](#Introduction)
* [Motor de búsqueda](#Engine)
  * [Hilos](#Threads)
  * [Opciones](#Options)
  * [Ejemplos](#Examples)
  * [Visualización](#Visual)
* [API](#Api)
  * [Rutas](#Routes)
* [Despliegue](#Deployment)
  * [Básico](#Basic)
  * [Avanzado](#Advanced)
* [Aportes](#Contributing)
* [Aviso Legal](#Legal-disclaimer)
* [Contacto](#Contact)
* [Licencia](#License)

## Introducción
Spidex es un escáner de reconocimiento continuo, que da prioridad a demostrar la exposición de la red.
Realiza un escaneo orientado a puertos en gran escala y almacena información de cada dispositivo conectado a Internet.

## Motor de búsqueda
El motor de búsqueda se encarga de analizar masivamente las direcciones IP recibidas como argumentos. Recopila información pública sobre cada objetivo, como por ejemplo: puertos abiertos, ubicación geográfica, tecnologías web y banners.

También almacena un informe por cada ciclo de escaneo, que contiene: Tiempo de ejecución, dispositivos encontrados y fecha de inicio / final.

### Hilos
La implementación de hilos y colas aumenta el rendimiento durante la exploración. De este modo, las peticiones se envían en paralelo y el tiempo de ejecución de cada ciclo se reduce considerablemente.
Actualmente cuenta con un límite de 450/500 hilos.

### Opciones
```
options:
  -h, --help            show this help message and exit
  -r RANGE, --range RANGE
                        Start IPv4 address
  -t THREADS, --threads THREADS
                        Number of threads [Default: 50]
  -f, FILE, --file      File path with IPv4 ranges
  -ti TIMEOUT, --timeout TIMEOUT
                        Socket timeout [Default: 0.5]
  -p, --top-ports       Scan only 20 most used ports
  -a, --all-ports       Scan 1000 most used ports
  -c CUSTOM [CUSTOM ...], --custom-ports CUSTOM [CUSTOM ...]
                        Scan custom ports directly from terminal
  -l, --logs            Add a log file, useful in debugging
```
### Ejemplos
Escanear sólo un rango de direcciones IPv4 con los puertos más usados por defecto:
 ```bash
python3 engine.py -r 192.168.0.0,192.168.0.255 -t 150 --top-ports
 ```
Escanear desde un archivo de texto con rangos de direcciones IPv4, 200 hilos y un tiempo de espera por socket de 5 segundos:
```bash
python3 engine.py -m ranges.csv -t 200 -ti 5 --all-ports
```
Escanear con CIDR, puertos personalizados y opción de registros:
```bash
python3 engine.py -r 192.168.0.0/255 -t 350 -C 80 21 22 --logs
```

### Visualización
<a href="https://asciinema.org/a/goJmDQ9ucUAOmxTeRPUZr4Qxl" target="_blank"><img src="https://asciinema.org/a/goJmDQ9ucUAOmxTeRPUZr4Qxl.svg" width=700px></a>

## API
Consiste en una aplicación Flask, que permite almacenar y realizar cualquier operación sobre los resultados enviados por el motor de búsqueda. Utiliza MongoDB como base de datos, es ideal porque los datos no están estructurados.

### Rutas
| Método  | Ruta                   | Descripción                       |
|---------|------------------------|-----------------------------------|
| POST    | api/submit/device      | Envía un resultado                |
| GET     | api/devices            | Obtiene todos los resultados      |
| GET     | api/device/ip          | Obtiene un resultado por IP       |
| DELETE  | api/delete/device/ip   | Elimina un resultado              |
| POST    | api/submit/report      | Envia el reporte de escaneo       |
| GET     | api/reports            | Obtiene todos los reportes        |

## Despliegue
El despliegue de ambos componentes se realiza con Docker, para facilitar la instalación y evitar contaminar el entorno con dependencias.
Puedes descargar las imágenes desde DockerHub. 
### Básico
Para un despliegue básico, establezca las variables de entorno para cada imagen, en los [archivos de Docker Compose]() e inicie los contenedores en el siguiente orden:

#### MongoDB
```python
MONGO_INITDB_ROOT_USERNAME: USERNAME
MONGO_INITDB_ROOT_PASSWORD: PASSWORD
```
#### API
```
DB_SERVER_NAME: MONGODB_SERVER 
DB_USERNAME: MONGODB_USER
DB_PASSWORD: MONGODB_PASSWORD
```
#### Motor de búsqueda
```
SERVER_ADDRESS: API_SERVER
```

### Avanzado
La integración de Elasticsearch y Kibana permite disponer de una interfaz gráfica para visualizar y manipular los datos de manera eficiente.

Sin embargo, actualmente el proyecto no cuenta con funciones para insertar datos en Elasticsearch de forma automática.
Pero se pueden utilizar herramientas como: Mongo-to-elastic-dump y generar algunos gráficos interesantes en su máquina local, después de completar el ciclo de exploración.

## Aportes
Si tienes ideas o futuras mejoras, no dudes en participar para seguir haciendo genial este proyecto.
 
## Aviso legal
Este proyecto está hecho sólo con fines educativos y de prueba ética. El uso de este software para atacar objetivos sin el consentimiento mutuo previo es ilegal. Es responsabilidad del usuario final obedecer todas las leyes locales, estatales y federales aplicables. Los desarrolladores no asumen ninguna responsabilidad y no son responsables de cualquier mal uso o daño causado por este programa.

## Contacto
alechilczenko@gmail.com

## Licencia
[Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)