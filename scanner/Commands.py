import argparse
import pathlib

def get_flags():
    parser = argparse.ArgumentParser(
        description="Automatic scanner for Internet-connected devices")
    parser.add_argument("-s",
                        type=str,
                        help="Start IPv4 address",
                        dest="start")

    parser.add_argument("-e",
                        type=str,
                        help="End IPv4 address",
                        dest="end")

    parser.add_argument("-t",
                        type=int,
                        dest="threads",
                        help="Number of threads [Default: 50]",
                        default=50)

    parser.add_argument("--massive",
                        type=pathlib.Path,
                        help="File path with IPv4 ranges",
                        dest="file")

    parser.add_argument("--timeout",
                        type=int,
                        help="Socket timeout [Default: 0.5]",
                        dest="timeout",
                        default=0.5)

    parser.add_argument("--screenshot",
                        action="store_true",
                        help="Take screenshots from hosts with HTTP")
        
    parser.add_argument("--top-ports",
                        action="store_true",
                        help="Scan only 20 most used ports [Default]",
                        dest="top")

    parser.add_argument("--all-ports",
                        action="store_true",
                        help="Scan 1000 most used ports",
                        dest="all")

    parser.add_argument("--update",
                        action="store_true",
                        help="Update database from Wappalyzer",
                        dest="update")

    flags = parser.parse_args()
    return flags.start, flags.end, flags.threads,flags.file, flags.timeout, flags.screenshot, flags.top, flags.all, flags.update
