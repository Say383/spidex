<h1 align="center">pwndora</h1>
<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/-ElasticSearch-005571?style=for-the-badge&logo=elasticsearch">
<img src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
</p>

## Introduction
Pwndora is a massive and fast IPv4 address range scanner, integrated with multi-threading.

Using sockets, it analyzes which ports are open, and collects more information about the devices, Each result is stored in Elasticsearch. 
## Features

- ### Port Scanning
  Is a method of determining which ports on a network are open and could be receiving or sending data. It is also a process for sending packets to specific ports on a host and     analyzing responses to identify vulnerabilities.
  
- ### Banner Grabbing
  Banner grabbing is the act of getting software banner information (name and version), whether it’s done manually, or by using any OSINT   tools that can do it for you           automatically.

  FTP servers, web servers, SSH servers and other system daemons often expose critical information about not only the software name, but also about the exact versions and         operating systems they’re running.
  
  For example, following is a FTP banner:
  ```
  "220 CONICET La Plata FTP Server ready."
  ```

- ### IP Geolocation
  IP Geolocation is the identification of the geographic location of a device, such as a mobile phone, gadget, laptop, server and so on, by using an IP address.
  This scanner retrieves geolocation from Maxmind database, updated periodically. 
  ```
  "country" : "Argentina",
  "region_name" : "Buenos Aires",
  "city" : "La Plata",
  "country_code" : "AR",
  "zip_code" : "1900",
  "time_zone" : "America/Argentina/Buenos_Aires",
  "latitude" : -34.9314,
  "longitude" : -57.9489,
  ```
- ### Screenshot
  Possibility to take screenshots from hosts with HTTP using [Rendertron](https://github.com/GoogleChrome/rendertron) and unnauthenticated VNC servers, using [VNC Snapshot](https://github.com/IDNT/vncsnapshot)

### CLI Usage
```
usage: CLI.py [-h] [-s START_IP] [-e END_IP] [-t THREADS] [-m FILE] [--timeout TIMEOUT] [--screenshot] [--top-ports] [--all-ports]

Scanner for Internet-connected devices

optional arguments:
  -h, --help            show this help message and exit
  -s START_IP, --start START_IP
  -e END_IP, --end END_IP
  -t THREADS, --threads THREADS
                        Number of threads [Default: 100]
  -m FILE, --massive-scan FILE
                        File path with IP blocks
  --timeout TIMEOUT     Socket timeout [Default: 0.5]
  --screenshot          Take screenshots from hosts with HTTP
  --top-ports           Scan only 20 most used ports
  --all-ports           Scan 1000 most used ports
```
### Examples
Scan only a single IPv4 address range:
```shell
python3 CLI.py --start 192.168.0.0 --end 192.168.0.255 -t 500 --top-ports
```
Scan from a text file with multiple IPv4 address ranges:
```shell
python3 CLI.py --massive-scan Argentina.csv -t 200 --all-ports --screenshot 
```
## To-do list

- [x] [Command-line interface](https://github.com/alechilczenko/Night-Crawler/blob/main/scanner/CLI.py)
- [x] [Backend API with Flask](https://github.com/alechilczenko/Night-Crawler/tree/main/flask)
- [x] Execution time in terminal
- [x] Logging module implementation, for exception handling
- [x] Massive and automatic scanning
- [x] [Default FTP login detection](https://github.com/alechilczenko/Night-Crawler/blob/main/scanner/login.py)
- [x] [Automatic download of IP ranges by country](https://github.com/alechilczenko/Night-Crawler/blob/main/ranges/ranges.py)
- [x] [Screenshot of unnauthenticated VNC servers](https://github.com/alechilczenko/Night-Crawler/blob/main/scanner/vnc.py) 
- [ ] Frontend with React
- [ ] Web application vulnerability scan
- [ ] Search filter by tags
- [ ] Web technologies detection
- [ ] Find domain name associated with IP
- [ ] Build image with Docker and deployment
- [ ] Honeypot detection
- [ ] RDP Screenshot


## Requirements
 ```
 pip install -r requirements.txt
 ```
## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## Contact

alechilczenko@gmail.com

## License

[Apache 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)
