#!.venv/bin/python

from server import serve
from scraper import scrape

if __name__ == "__main__":
    scrape()
    serve()
