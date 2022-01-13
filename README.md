<h1 align="center">pwndora</h1>
<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/-ElasticSearch-005571?style=for-the-badge&logo=elasticsearch">
<img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
</p>

## Introduction
Pwndora is a massive and fast IPv4 address range scanner, integrated with multi-threading.

Using sockets, it analyzes which ports are open, and collects more information about targets, each result is stored in Elasticsearch. You can integrate with Kibana to be able to visualize and manipulate data, basically it's like having your own IoT search engine at home.

## Features

- Port scanning with different options and retrieve software banner information.
- Detect some web technologies running on servers, using Webtech integration.   
- Retrieves IP geolocation from Maxmind free database, updated periodically. 
- Possibility to take screenshots from hosts with HTTP using [Rendertron](https://github.com/GoogleChrome/rendertron).
- Anonymous login detection on FTP servers

## Visual
<a href="https://asciinema.org/a/n1RmVV8Rq800jQlCih8ROWeaY" target="_blank"><img src="https://asciinema.org/a/n1RmVV8Rq800jQlCih8ROWeaY.svg" width=700px /></a>

## Getting Started
- Install requirements
  ```
  pip install -r requirements.txt
  ```
- Set password for Elasticsearch and Kibana containers in [docker-compose.yml](https://github.com/alechilczenko/pwndora/blob/main/docker-compose.yml)
- Configure connection to database in [connect.py](https://github.com/alechilczenko/pwndora/blob/main/scanner/Connect.py)
- Set paths of Maxmind ASN and city databases in [var.py](https://github.com/alechilczenko/pwndora/blob/main/scanner/var.py)
- Launch containers in background with Docker Compose
  ```shell
  docker-compose up -d
  ```


 
## Usage
```
usage: CLI.py [-h] [-s START] [-e END] [-t THREADS] [--massive FILE] [--timeout TIMEOUT]
              [--screenshot] [--top-ports] [--all-ports] [--update]
options:
  -h, --help         show this help message and exit
  -s START           Start IPv4 address
  -e END             End IPv4 address
  -t THREADS         Number of threads [Default: 50]
  --massive FILE     File path with IPv4 ranges
  --timeout TIMEOUT  Socket timeout [Default: 0.5]
  --screenshot       Take screenshots from hosts with HTTP
  --top-ports        Scan only 20 most used ports [Default]
  --all-ports        Scan 1000 most used ports
  --update           Update database from Wappalyzer
```
### Examples
> If this is your first time running, you should use the --update argument.

Scan only a single IPv4 address range:
```shell
python3 CLI.py -s 192.168.0.0 -e 192.168.0.255 -t 150 --top-ports
```
Scan from a text file with multiple IPv4 address ranges:
```shell
python3 CLI.py --massive-scan Argentina.csv -t 200 --all-ports --screenshot 
```
> If you use an excessive amount of threads, some ISPs may detect suspicious traffic and disconnect you from the network. 

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## Contact
alechilczenko@gmail.com

## License
[Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)
