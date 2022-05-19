<img src="static/logo.png" width=180px>

<img src="https://github.com/aleen42/badges/blob/master/src/python.svg">
<img src="https://github.com/aleen42/badges/blob/master/src/docker.svg">
<img src="https://img.shields.io/badge/Version-4.0-brightgreen">
<img src="https://img.shields.io/badge/Maintained%3F-yes-blue.svg">

---------

Current release: v4.0.0 developed by @alechilczenko

> Note: Docker images will be released in the coming weeks.

## Table of contents
* [Guide](#Guide)
  * [English]()
  * [Spanish]()
* [Introduction](#Introduction)
* [Engine](#Engine)
  * [Threads](#Threads)
  * [Options](#Options)
  * [Examples](#Examples)
  * [Visual](#Visual)
* [API](#Api)
  * [Routes](#Routes)
* [Deployment](#Deployment)
  * [Basic](#Basic)
  * [Advanced](#Advanced)
* [Contributing](#Contributing)
* [Legal Disclaimer](#Legal-disclaimer)
* [Contact](#Contact)
* [License](#License)

## Introduction
Spidex is a continuous reconnaissance scanner, which gives priority to proving network exposure.
It performs large-scale port-oriented scanning and collects information from every device connected to the Internet.

## Engine
The engine is responsible for massively analyzing IP addresses received as arguments. It collects public information about each target, such as: open ports, geographic location, web technologies and banners.

Also stores a report for every scan cycle, containing:
Execution time, devices found and start/end date.

### Threads
The implementation of threads and queues increases performance during scanning. In this way, requests are sent in parallel and the execution time for each cycle is significantly reduced.
It currently has a limit of 450/500 threads.

### Options
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
### Examples
Scan only a single IPv4 address range with most used ports by default:
 ```bash
python3 engine.py -r 192.168.0.0,192.168.0.255 -t 150 --top-ports
 ```
Scan from a text file with multiple IPv4 address ranges and socket timeout of seconds:
```bash
python3 engine.py -m ranges.csv -t 200 -ti 5 --all-ports
```
Scan with CIDR, custom ports and logs option:
```bash
python3 engine.py -r 192.168.0.0/255 -t 350 -C 80 21 22 --logs
```

### Visual
<a href="https://asciinema.org/a/goJmDQ9ucUAOmxTeRPUZr4Qxl" target="_blank"><img src="https://asciinema.org/a/goJmDQ9ucUAOmxTeRPUZr4Qxl.svg" width=700px></a>

## API
It consists of a Flask application, which allows to store and perform any operation on the results sent by the search engine. It uses MongoDB as a database, it is ideal because the data is not structured.

### Routes
| Method  | Route                  | Description                       |
|---------|------------------------|-----------------------------------|
| POST    | api/submit/device      | Submit single result              |
| GET     | api/devices            | Get all results                   |
| GET     | api/device/ip          | Get single result by IP address   |
| DELETE  | api/delete/device/ip   | Delete one                        |
| POST    | api/submit/report      | Submit report scan                |
| GET     | api/reports            | Get all reports

## Deployment
The deployment of both components is performed with Docker, for easier installation and to avoid contaminating the environment with dependencies.
You can download the images from DockerHub. 
### Basic
For a basic deployment, set the environment variables for each image, in the [Docker Compose files]()
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
#### Engine
```
SERVER_ADDRESS: API_SERVER
```

### Advanced
The integration of Elasticsearch and Kibana allows to have a graphical interface to visualize and manipulate data in an efficient way.
Currently the project does not have a way to insert data automatically.
But you can use tools such as: Mongo-to-elastic-dump, and generate some interesting graphs in your local machine after complete scan cycle.

## Contributing
If you have ideas or future features, feel free to participate to continue making this project great. 
## Legal Disclaimer
This project is made for educational and ethical testing purposes only. Usage of this software for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program.

## Contact
alechilczenko@gmail.com

## License
[Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)