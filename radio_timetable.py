#!.venv/bin/python

import argparse
from server import serve
from scraper import scrape

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-c",
        "--command",
        type=str,
        help="scrape or serve. Omit to do both.",
    )
    args = parser.parse_args()
    if args.command == "scrape":
        scrape()
    elif args.command == "serve":
        serve()
    else:
        scrape()
        serve()
