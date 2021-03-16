from datetime import datetime
from dataclasses import dataclass
from requests_html import HTMLSession
import requests


@dataclass
class Program:
    start_at: datetime
    end_at: datetime
    title: str
    act: str


def nhk():
    r = requests.get("https://api.nhk.or.jp/r5/pg/list/4/230/all/2021-03-16.json")
    channels = r.json()["list"]
    r1 = channels["r1"]
    r2 = channels["r2"]
    fm = channels["r3"]
    all = r1 + r2 + fm

    def extract(item):
        return Program(
            start_at=datetime.fromisoformat(item["start_time"]),
            end_at=datetime.fromisoformat(item["end_time"]),
            title=item["title"],
            act=item["act"],
        )

    return [extract(item) for item in all]


if __name__ == "__main__":
    print(nhk())
