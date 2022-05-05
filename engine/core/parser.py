import argparse
import pathlib

def get_flags():
    parser = argparse.ArgumentParser(
        description="Automatic scanner for Internet-connected devices")
    parser.add_argument("-s",
                        "--start",
                        type=str,
                        help="Start IPv4 address",
                        dest="start")

    parser.add_argument("-e",
                        "--end",
                        type=str,
                        help="End IPv4 address",
                        dest="end")

    parser.add_argument("-t",
                        "--threads",
                        type=int,
                        dest="threads",
                        help="Number of threads [Default: 50]",
                        default=50)

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
                        default=0.5)

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

    parser.add_argument("-sl",
                        "--slack",
                        action="store_true",
                        help="Send notifications by Slack with results",
                        dest="slack")

    parser.add_argument("-sv",
                        "--save",
                        choices=['json','mongodb'],
                        help="Methods of data storage",
                        dest="save")

    parser.add_argument("-l",
                        "--logs",
                        action="store_true",
                        help="Add a log file, useful in debugging",
                        dest="logs")

    flags = parser.parse_args()
    return flags.start, flags.end, flags.threads,flags.file, flags.timeout, flags.top, flags.all, flags.custom, flags.slack, flags.save, flags.logs
