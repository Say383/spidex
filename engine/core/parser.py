import argparse
import config
import pathlib

#A basic function to return all arguments in the main program
def get_flags():

    settings = config.Config()

    parser = argparse.ArgumentParser(
        description="Automatic scanner for Internet-connected devices")
    parser.add_argument("-r",
                        "--range",
                        type=str,
                        help="Start IPv4 address",
                        dest="range")

    parser.add_argument("-t",
                        "--threads",
                        type=int,
                        dest="threads",
                        help="Number of threads [Default: 50]",
                        default=settings.max_threads)

    parser.add_argument("-m",
                        "--massive-scan",
                        type=pathlib.Path,
                        help="File path with IPv4 ranges",
                        dest="file")

    parser.add_argument("-ti",
                        "--timeout",
                        type=int,
                        help="Socket timeout [Default: 0.5]",
                        dest="timeout",
                        default=settings.request_timeout)

    parser.add_argument("-p",
                        "--top-ports",
                        action="store_true",
                        help="Scan only 20 most used ports",
                        dest="top")

    parser.add_argument("-a",
                        "--all-ports",
                        action="store_true",
                        help="Scan 1000 most used ports",
                        dest="all")

    parser.add_argument("-c",
                        '--custom-ports',
                        nargs='+',
                        type=int,
                        help='Scan custom ports directly from terminal',
                        dest="custom")

    parser.add_argument("-l",
                        "--logs",
                        action="store_true",
                        help="Add a log file, useful in debugging",
                        dest="logs")

    flags = parser.parse_args()
    return flags.range, flags.threads,flags.file, flags.timeout, flags.top, flags.all, flags.custom, flags.logs
